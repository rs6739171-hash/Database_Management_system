from pydantic import EmailStr
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from enum import Enum

class ProductCategory(str,Enum):
    Electronics = "Electronics"
    Clothing = "Clothing"
    Books = "Books"
    Groceries = "Groceries"
    Beauty = "Beauty"
    Toys = "Toys"
    Sports = "Sports"
    Other = "Other"


class Product(SQLModel, table=True):
    __tablename__ = "products"
    id:int = Field(default=None,primary_key=True)
    name:str = Field(max_length=100)
    price:float=Field(gt=0)
    stock:int=Field(ge=0)
    category: ProductCategory = Field(default=ProductCategory.Other)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Seller(SQLModel,table=True):
    id : int = Field(default=None,primary_key=True)
    name: str
    email:EmailStr
    password_hash : str




