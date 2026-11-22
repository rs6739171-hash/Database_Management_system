from typing import Annotated
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.database.models import Seller
from app.schema.seller import SellerCreate
from fastapi import APIRouter, Depends
from app.api.dependencies import SellerDep

router = APIRouter(prefix="/seller", tags=["Seller"])


@router.post("/signup")
async def register_seller(seller : SellerCreate,service:SellerDep)-> Seller:
    return await service.add(seller)

@router.post("/login")
async def login(request_form : Annotated[OAuth2PasswordRequestForm, Depends()], service : SellerDep):
    token = await service.login(request_form.username,request_form.password)
    return {"access_token": token , "token_type":"bearer"}