from sqlalchemy.dialects import postgresql
from sqlalchemy import Column
from typing import List
from pydantic import EmailStr
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from uuid import uuid4,UUID

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
    id:UUID = Field(sa_column=Column(postgresql.UUID,primary_key=True,default=uuid4))
    name:str = Field(max_length=100)
    price:float=Field(gt=0)
    stock:int=Field(ge=0)
    category: ProductCategory = Field(default=ProductCategory.Other)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    seller_id : UUID = Field(foreign_key="seller.id")
    seller:"Seller" = Relationship(back_populates="product",sa_relationship_kwargs={'lazy':"selectin"})

class Seller(SQLModel,table=True):
    id:UUID = Field(sa_column=Column(postgresql.UUID,primary_key=True,default=uuid4))
    name: str
    email:EmailStr
    password_hash : str
    product:List[Product] = Relationship(back_populates="seller",sa_relationship_kwargs={'lazy':"selectin"})
    address : str




