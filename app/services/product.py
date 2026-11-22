from typing import Annotated
from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Product
from app.schema.models import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Product | None:
        return await self.session.get(Product, id)

    async def add(self, data: ProductCreate) -> Product:
        product = Product(**data.model_dump())
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def update(self, id: int, body: dict) -> Product | None:
        product = await self.session.get(Product,id)
        if product is None:
            return None
        product.sqlmodel_update(body)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete(self,id: int) -> bool:
        product = await self.get(id)
        if not product:
            return False

        await self.session.delete(product)
        await self.session.commit()
        return True
