from uuid import UUID
from app.database.reddis import is_jti_blacklisted
from app.database.models import Seller
from app.core.security import auth2_scheme
from app.utils import decode_access_token
from app.services.seller import SellerService
from app.services.product import ProductService
from app.database.session import get_session
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
SessionDep = Annotated[AsyncSession, Depends(get_session)]

def get_product_service(session:SessionDep):
    return ProductService(session)

# Acess user data

async def get_access_token(token:Annotated[str,Depends(auth2_scheme)])->dict:
    data = decode_access_token(token)
    if data is None or not data.get("jti") or await is_jti_blacklisted(data["jti"]):
        raise HTTPException(status_code=401, detail="Invalid Token")     
    return data

# Get logged in seller
async def get_current_seller(
    token_data:Annotated[dict,Depends(get_access_token)],session:SessionDep):
    user_id = token_data.get("user", {}).get("id") if isinstance(token_data, dict) else None
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid Token")
    seller = await session.get(Seller, UUID(user_id))
    return seller

CurrentSellerDep = Annotated[Seller, Depends(get_current_seller)]
SellerServiceDep = CurrentSellerDep


ProductDep = Annotated[ProductService,Depends(get_product_service)]

def get_seller_service(session:SessionDep):
    return SellerService(session)

SellerDep = Annotated[SellerService,Depends(get_seller_service)]
