from uuid import UUID,uuid4
from enum import Enum
import random
from pydantic import BaseModel, Field


def random_warehouse() -> int:
    return random.randint(1, 5)

class ProductStatus(str, Enum):
    active = "active"
    low_stock = "low_stock"
    out_of_stock = "out_of_stock"
    ACTIVE = "active"
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"


class BaseProduct(BaseModel):
    name: str = Field(
        description="Product Title",
        min_length=3,
        max_length=100,
    )
    price: float = Field(
        description="Price in USD",
        gt=0,
        le=1000,
    )
    stock: int = Field(
        description="Unit Available in Warehouse",
        ge=0,
    )

class ProductCreate(BaseProduct):
    id:UUID=Field(default_factory=uuid4)

class ProductRead(BaseProduct):
    id:UUID=Field(default_factory=uuid4)

class ProductUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        description="Product Title",
        min_length=3,
        max_length=100,
    )
    price: float | None = Field(
        default=None,
        description="Price in USD",
        gt=0,
        le=1000,
    )
    stock: int | None = Field(
        default=None,
        description="Unit Available in Warehouse",
        ge=0,
    )
    