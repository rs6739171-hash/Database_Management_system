from redis import RedisError
from app.database.reddis import add_jti_to_blacklist
from typing import Annotated
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.database.models import Seller
from app.schema.seller import SellerCreate
from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies import SellerDep, SellerServiceDep, get_access_token



router = APIRouter(prefix="/seller", tags=["Seller"])


@router.post("/signup")
async def register_seller(seller : SellerCreate,service:SellerDep)-> Seller:
    return await service.add(seller)

@router.post("/login")
async def login(request_form : Annotated[OAuth2PasswordRequestForm, Depends()], service : SellerDep):
    token = await service.login(request_form.username,request_form.password)
    return {"access_token": token , "token_type":"bearer"}

@router.get("/dashboard")
async def get_dashboard(seller: SellerServiceDep):
    if seller:
        return {"Details": seller, "Status": "Successfully Logged In"}
    raise HTTPException(status_code=401, detail="Invalid Token")

@router.get("/logout")
async def logout_seller(token_data:Annotated[dict,Depends(get_access_token)]):
    jti:str=token_data['jti']
    try:
        await add_jti_to_blacklist(jti)
    except RedisError:
        raise HTTPException(status_code=503, detail="Redis Down")
    return {"message": "Logout Successful"}