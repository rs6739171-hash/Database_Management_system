from datetime import timedelta, datetime, timezone
import jwt
from fastapi import HTTPException
from sqlalchemy import select
from app.database.models import Seller
from app.schema.seller import SellerCreate
from sqlalchemy.ext.asyncio import session, AsyncSession
from passlib.context import CryptContext
from app.config import Securitysettings as st

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SellerService:
    def __init__(self,session:AsyncSession):
        self.session = session

    async def add(self,creadentials:SellerCreate)-> Seller:
        seller = Seller(
       **creadentials.model_dump(exclude={"password"}),
       password_hash=pwd_context.hash(creadentials.password)
        )
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)
        return seller

    async def login(self,email,password)->str:
        result =await self.session.execute(select(Seller).where(Seller.email == email))
        seller = result.scalar()
        if seller is None or not pwd_context.verify(password,seller.password_hash):
            raise HTTPException(
                status_code=401,
                detail = "Email or Password is not correct")

        #generate access token
        return jwt.encode(
            payload = {
                "user":{
                    "name": seller.name,
                    "email": seller.email
                },
                "exp":datetime.now(timezone.utc)+timedelta(minutes=30)
            },
            algorithm=st.JWT_ALGORITHM,
            key = st.JWT_SECRET
        )