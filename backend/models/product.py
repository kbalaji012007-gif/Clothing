from typing import List, Optional
from pydantic import BaseModel, Field

class Product(BaseModel):
    id: str
    title: str
    name: Optional[str] = None
    subtitle: Optional[str] = None
    category: str = "apparel"  # "sneakers", "rack", "runway"
    price: str = "$149.00"
    numericPrice: float = 149.0
    image: Optional[str] = None
    frontImage: Optional[str] = None
    sideImage: Optional[str] = None
    tag: Optional[str] = None
    desc: Optional[str] = None
    sizes: List[str] = Field(default_factory=lambda: ["S", "M", "L", "XL"])
    in_stock: bool = True

class ProductCreate(BaseModel):
    id: str
    title: str
    name: Optional[str] = None
    subtitle: Optional[str] = None
    category: str = "apparel"
    price: str
    numericPrice: float
    image: Optional[str] = None
    frontImage: Optional[str] = None
    sideImage: Optional[str] = None
    tag: Optional[str] = None
    desc: Optional[str] = None
    sizes: List[str] = Field(default_factory=lambda: ["S", "M", "L", "XL"])
    in_stock: bool = True

class ProductUpdateRequest(BaseModel):
    title: Optional[str] = None
    name: Optional[str] = None
    subtitle: Optional[str] = None
    category: Optional[str] = None
    price: Optional[str] = None
    numericPrice: Optional[float] = None
    image: Optional[str] = None
    frontImage: Optional[str] = None
    sideImage: Optional[str] = None
    tag: Optional[str] = None
    desc: Optional[str] = None
    sizes: Optional[List[str]] = None
    in_stock: Optional[bool] = None
