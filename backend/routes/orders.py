from typing import List, Optional, Dict, Any
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import HTMLResponse
from ..models import Order, OrderCreate, OrderCancellationRequest, OrderRefundRequest
from ..services.firestore_service import FirestoreService
from ..security import get_optional_current_user, require_customer, require_admin

router = APIRouter(prefix="/orders", tags=["Orders"])

USD_TO_INR_RATE = 86.50
COMPANY_INFO = {
    "name": "ATELIER COUTURE & STREETWEAR LTD.",
    "brand": "ATELIER LUXURY STUDIO",
    "address": "Atelier High Street Flagship, Block C, Connaught Place, New Delhi 110001",
    "gstin": "07AABCA1234F1Z5",
    "cin": "U17120DL2026PLC123456",
    "email": "concierge@atelier.luxury",
    "phone": "+91 1800 283 5437"
}

@router.post("", response_model=Order, status_code=201)
def place_order(order_data: OrderCreate, current_user: Optional[Dict[str, Any]] = Depends(get_optional_current_user)):
    """Place a checkout order and save it directly into the Firestore orders collection."""
    if not order_data.items:
        raise HTTPException(status_code=400, detail="Cannot place an order with zero items.")
    
    payload = order_data.model_dump()
    if current_user:
        payload["customer_id"] = current_user.get("user_id")
        payload["customer_email"] = current_user.get("email", payload.get("customer_email"))
        if not payload.get("customer_name") or payload.get("customer_name") == "Anonymous":
            payload["customer_name"] = current_user.get("name", "Member")
    
    try:
        return FirestoreService.create_order(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my-orders", response_model=List[Order])
def get_my_orders(current_user: Dict[str, Any] = Depends(require_customer)):
    """Retrieve all orders placed by the authenticated customer."""
    return FirestoreService.get_orders_for_customer(current_user["email"])

@router.get("/{order_id}", response_model=Order)
def get_order(order_id: str, current_user: Optional[Dict[str, Any]] = Depends(get_optional_current_user)):
    """Retrieve an existing order by ID. Customers can only view their own orders."""
    order = FirestoreService.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order '{order_id}' not found.")
    
    if current_user:
        role = current_user.get("role", "").upper()
        if role != "ADMIN" and current_user.get("email", "").lower() != order.customer_email.lower():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You do not have permission to view another customer's order."
            )
    return order

@router.post("/{order_id}/cancel", response_model=Order)
def cancel_order(order_id: str, payload: OrderCancellationRequest, current_user: Dict[str, Any] = Depends(require_customer)):
    """Customer request to cancel an order."""
    try:
        order = FirestoreService.request_order_cancellation(order_id, current_user["email"], payload.reason)
        if not order:
            raise HTTPException(status_code=404, detail=f"Order '{order_id}' not found or does not belong to you.")
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{order_id}/refund", response_model=Order)
def request_refund(order_id: str, payload: OrderRefundRequest, current_user: Dict[str, Any] = Depends(require_customer)):
    """Customer request for order refund."""
    order = FirestoreService.request_order_refund(order_id, current_user["email"], payload.reason)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order '{order_id}' not found or does not belong to you.")
    return order

@router.get("", response_model=List[Order])
def list_orders(current_user: Dict[str, Any] = Depends(require_admin)):
    """List recent orders saved in Firestore (Admin access only)."""
    return FirestoreService.list_orders()

@router.get("/{order_id}/invoice")
def get_order_invoice(order_id: str):
    """Generate structured Tax Invoice data for an existing order."""
    order = FirestoreService.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order '{order_id}' not found.")
    
    is_inr = float(order.total) >= 500 or any(float(i.price) >= 500 for i in order.items)
    if is_inr:
        total_inr = round(float(order.total), 2)
        total_usd = round(total_inr / USD_TO_INR_RATE, 2)
        subtotal_inr = round(float(order.subtotal), 2)
        subtotal_usd = round(subtotal_inr / USD_TO_INR_RATE, 2)
    else:
        total_usd = float(order.total)
        total_inr = round(total_usd * USD_TO_INR_RATE, 2)
        subtotal_usd = float(order.subtotal)
        subtotal_inr = round(subtotal_usd * USD_TO_INR_RATE, 2)

    tax_inr = round(total_inr * 0.18 / 1.18, 2) # 18% GST inclusive
    cgst_inr = round(tax_inr / 2, 2)
    sgst_inr = round(tax_inr / 2, 2)

    invoice_number = f"INV-{datetime.utcnow().year}-{order.id}"
    
    formatted_items = []
    for item in order.items:
        if is_inr:
            p_inr = round(float(item.price), 2)
            p_usd = round(p_inr / USD_TO_INR_RATE, 2)
            lt_inr = round(p_inr * item.quantity, 2)
            lt_usd = round(lt_inr / USD_TO_INR_RATE, 2)
        else:
            p_usd = round(float(item.price), 2)
            p_inr = round(p_usd * USD_TO_INR_RATE, 2)
            lt_usd = round(p_usd * item.quantity, 2)
            lt_inr = round(p_usd * item.quantity * USD_TO_INR_RATE, 2)
        formatted_items.append({
            "product_id": item.product_id,
            "title": item.title,
            "size": item.size,
            "quantity": item.quantity,
            "price_usd": p_usd,
            "price_inr": p_inr,
            "line_total_usd": lt_usd,
            "line_total_inr": lt_inr
        })

    return {
        "invoice_number": invoice_number,
        "invoice_date": order.created_at.strftime("%d %b %Y, %H:%M:%S UTC") if isinstance(order.created_at, datetime) else str(order.created_at),
        "company": COMPANY_INFO,
        "customer": {
            "name": order.customer_name,
            "email": order.customer_email,
            "shipping_address": order.shipping_address
        },
        "payment": {
            "method": order.payment_method,
            "status": "PAID & VERIFIED",
            "currency_rate": f"1 USD = ₹{USD_TO_INR_RATE:.2f} INR"
        },
        "items": formatted_items,
        "financials": {
            "subtotal_usd": subtotal_usd,
            "subtotal_inr": subtotal_inr,
            "shipping_usd": 0.0,
            "shipping_inr": 0.0,
            "gst_rate": "18% (Inclusive)",
            "cgst_inr": cgst_inr,
            "sgst_inr": sgst_inr,
            "total_usd": total_usd,
            "total_inr": total_inr,
            "formatted_inr": f"₹{total_inr:,.2f}"
        }
    }

@router.get("/{order_id}/invoice/html", response_class=HTMLResponse)
def get_order_invoice_html(order_id: str):
    """Return an official, beautifully styled, printable Tax Invoice & Bill HTML page."""
    data = get_order_invoice(order_id)
    
    item_rows = ""
    for idx, item in enumerate(data["items"], start=1):
        item_rows += f"""
        <tr>
          <td style="padding: 12px 14px; border-bottom: 1px solid #eeeeee; font-size: 13px; color: #666;">{idx}</td>
          <td style="padding: 12px 14px; border-bottom: 1px solid #eeeeee; font-size: 13px; font-weight: 600; color: #111;">
            {item['title']}
            <div style="font-size: 11px; font-weight: 400; color: #777;">Size: {item['size']} · SKU: {item['product_id']}</div>
          </td>
          <td style="padding: 12px 14px; border-bottom: 1px solid #eeeeee; font-size: 13px; text-align: center;">{item['quantity']}</td>
          <td style="padding: 12px 14px; border-bottom: 1px solid #eeeeee; font-size: 13px; text-align: right;">${item['price_usd']:.2f} <div style="font-size:11px; color:#888;">₹{item['price_inr']:,.2f}</div></td>
          <td style="padding: 12px 14px; border-bottom: 1px solid #eeeeee; font-size: 13px; text-align: right; font-weight: 700;">${item['line_total_usd']:.2f} <div style="font-size:11px; color:#166534;">₹{item['line_total_inr']:,.2f}</div></td>
        </tr>
        """

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Tax Invoice #{data['invoice_number']} — {data['company']['brand']}</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: #f4f4f5;
      color: #111111;
      padding: 30px 15px;
      -webkit-font-smoothing: antialiased;
    }}
    .invoice-card {{
      max-width: 820px;
      margin: 0 auto;
      background: #ffffff;
      border: 1px solid #e5e5e5;
      border-radius: 12px;
      padding: 44px 48px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    }}
    .invoice-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      padding-bottom: 24px;
      border-bottom: 2px solid #111111;
      margin-bottom: 28px;
    }}
    .brand-title {{
      font-size: 24px;
      font-weight: 800;
      letter-spacing: -0.5px;
      text-transform: uppercase;
      margin-bottom: 4px;
    }}
    .brand-meta {{
      font-size: 12px;
      color: #666;
      line-height: 1.5;
    }}
    .invoice-badge-group {{
      text-align: right;
    }}
    .invoice-title {{
      font-size: 20px;
      font-weight: 800;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      color: #111;
      margin-bottom: 4px;
    }}
    .paid-stamp {{
      display: inline-block;
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 1px;
      padding: 4px 10px;
      border-radius: 4px;
      background: #dcfce7;
      color: #166534;
      border: 1px solid #86efac;
      margin-top: 6px;
    }}
    .meta-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      margin-bottom: 30px;
    }}
    .meta-box {{
      background: #fafafa;
      border: 1px solid #eeeeee;
      border-radius: 8px;
      padding: 16px 20px;
      font-size: 13px;
      line-height: 1.6;
    }}
    .meta-label {{
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: #888;
      margin-bottom: 6px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 28px;
    }}
    th {{
      background: #f7f7f7;
      padding: 11px 14px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: #555;
      border-bottom: 1.5px solid #111;
    }}
    .totals-area {{
      display: flex;
      justify-content: flex-end;
      margin-bottom: 30px;
    }}
    .totals-table {{
      width: 340px;
      border-collapse: collapse;
    }}
    .totals-table td {{
      padding: 8px 12px;
      font-size: 13px;
    }}
    .totals-table tr.grand-total td {{
      border-top: 2px solid #111;
      border-bottom: 2px solid #111;
      padding: 12px 12px;
      font-size: 16px;
      font-weight: 800;
      color: #111;
    }}
    .action-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 24px;
      border-top: 1px solid #eeeeee;
    }}
    .btn {{
      padding: 11px 22px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s;
    }}
    .btn-primary {{
      background: #111;
      color: #fff;
      border: none;
    }}
    .btn-primary:hover {{
      background: #333;
    }}
    .btn-outline {{
      background: #fff;
      color: #111;
      border: 1px solid #ccc;
    }}
    .btn-outline:hover {{
      border-color: #111;
    }}
    @media print {{
      body {{ background: #ffffff; padding: 0; }}
      .invoice-card {{ border: none; box-shadow: none; padding: 0; max-width: 100%; }}
      .action-bar {{ display: none !important; }}
    }}
  </style>
</head>
<body>
  <div class="invoice-card">
    <div class="invoice-header">
      <div>
        <div class="brand-title">{data['company']['name']}</div>
        <div class="brand-meta">
          {data['company']['address']}<br/>
          <strong>GSTIN:</strong> {data['company']['gstin']} · <strong>CIN:</strong> {data['company']['cin']}<br/>
          Concierge: {data['company']['email']} · {data['company']['phone']}
        </div>
      </div>
      <div class="invoice-badge-group">
        <div class="invoice-title">Tax Invoice</div>
        <div style="font-family: monospace; font-size: 13px; font-weight: 600; color: #555;">{data['invoice_number']}</div>
        <div style="font-size: 12px; color: #888; margin-top: 2px;">{data['invoice_date']}</div>
        <div class="paid-stamp">✓ {data['payment']['status']}</div>
      </div>
    </div>

    <div class="meta-grid">
      <div class="meta-box">
        <div class="meta-label">Billed & Shipped To</div>
        <strong style="font-size: 14px; color: #111;">{data['customer']['name']}</strong><br/>
        <span>{data['customer']['email']}</span><br/>
        <span style="color: #666;">{data['customer']['shipping_address']}</span>
      </div>
      <div class="meta-box">
        <div class="meta-label">Payment & Order Details</div>
        <div><strong>Order ID:</strong> <span style="font-family: monospace;">{order_id}</span></div>
        <div><strong>Payment Method:</strong> {data['payment']['method']}</div>
        <div><strong>Currency Conversion:</strong> {data['payment']['currency_rate']}</div>
        <div><strong>Delivery:</strong> Express Courier (Complimentary)</div>
      </div>
    </div>

    <table>
      <thead>
        <tr>
          <th style="text-align: left; width: 40px;">#</th>
          <th style="text-align: left;">Item Description</th>
          <th style="text-align: center; width: 60px;">Qty</th>
          <th style="text-align: right; width: 130px;">Unit Price</th>
          <th style="text-align: right; width: 140px;">Line Total</th>
        </tr>
      </thead>
      <tbody>
        {item_rows}
      </tbody>
    </table>

    <div class="totals-area">
      <table class="totals-table">
        <tr>
          <td style="color: #666;">Items Subtotal:</td>
          <td style="text-align: right; font-weight: 600;">${data['financials']['subtotal_usd']:.2f} <span style="font-size:11px; color:#888;">(₹{data['financials']['subtotal_inr']:,.2f})</span></td>
        </tr>
        <tr>
          <td style="color: #666;">CGST (9.0% included):</td>
          <td style="text-align: right; color: #666;">₹{data['financials']['cgst_inr']:,.2f}</td>
        </tr>
        <tr>
          <td style="color: #666;">SGST (9.0% included):</td>
          <td style="text-align: right; color: #666;">₹{data['financials']['sgst_inr']:,.2f}</td>
        </tr>
        <tr>
          <td style="color: #666;">Express Delivery:</td>
          <td style="text-align: right; color: #166534; font-weight: 600;">FREE</td>
        </tr>
        <tr class="grand-total">
          <td>Grand Total:</td>
          <td style="text-align: right;">${data['financials']['total_usd']:.2f} <div style="font-size: 13px; font-weight: 700; color: #166534;">{data['financials']['formatted_inr']}</div></td>
        </tr>
      </table>
    </div>

    <div style="background: #fafafa; border: 1px dashed #cccccc; border-radius: 8px; padding: 14px 18px; margin-bottom: 24px; font-size: 12px; color: #666; display: flex; align-items: center; justify-content: space-between;">
      <div>
        <strong>Official Electronic Receipt</strong><br/>
        This document is an authenticated digital tax invoice generated for Order {order_id}. No physical signature required.
      </div>
      <div style="font-family: monospace; font-size: 11px; background: #eee; padding: 4px 8px; border-radius: 4px;">AUTHENTICATED ✓</div>
    </div>

    <div class="action-bar">
      <a href="javascript:window.close();" class="btn btn-outline">← Close Invoice</a>
      <div style="display: flex; gap: 10px;">
        <button type="button" class="btn btn-outline" onclick="window.print()">🖨️ Print Tax Invoice</button>
        <button type="button" class="btn btn-primary" onclick="window.print()">📥 Download PDF / Print</button>
      </div>
    </div>
  </div>
</body>
</html>"""
    return html
