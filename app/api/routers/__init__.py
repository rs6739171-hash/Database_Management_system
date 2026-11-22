from fastapi import APIRouter
from app.api.routers import sellers, product

router = APIRouter()

router.include_router(sellers.router)
router.include_router(product.router)
