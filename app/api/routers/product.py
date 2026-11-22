from app.api.dependencies import ProductDep
from fastapi import APIRouter, HTTPException
from app.schema.models import ProductCreate, ProductUpdate
from app.database import Product

router = APIRouter(prefix="/product", tags=["Products"])


@router.get("/", response_model=Product)
async def get_product(id: int, service: ProductDep) -> Product:
    product = await service.get(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=Product)
async def create_product(data: ProductCreate, service: ProductDep) -> Product:
    return await service.add(data)


@router.patch("/", response_model=Product)
async def patch_product(id: int, body: ProductUpdate, service: ProductDep) -> Product:
    data = body.model_dump(exclude_none=True)
    if not data:
        raise HTTPException(status_code=400, detail="No data provided")
    updated = await service.update(id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated


@router.delete("/")
async def delete_product(id: int, service: ProductDep) -> dict[str, str]:
    success = await service.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": f"Product {id} deleted successfully"}
