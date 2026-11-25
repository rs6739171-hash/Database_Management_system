from app.services.product import ProductService
from app.config import settings
from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel

engine = create_async_engine(settings.POSTGRES_URL, echo=False, pool_pre_ping=True)

async_session = async_sessionmaker(bind = engine,class_=AsyncSession,expire_on_commit=False)


async def create_db_table():
    from app.database.models import Product, Seller  # noqa: F401
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async with AsyncSession(engine) as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]

def get_product_service(session:SessionDep):
    return ProductService(session)

ServiceDep = Annotated[ProductService,Depends(get_product_service)]