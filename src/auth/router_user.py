# from main folder
from pydantic import EmailStr
from ..db import get_connection

# from this folder
from .models_user import User, UrlForUpdatePassword

from .utlils.dto_user import UserRegister, LoginUser, GiveaDataUser, UpdateUser
from .utlils.crud_user import UserCrud
from .utlils.auth_work import check_password, create_access_token, valid_access_token
from ..get_user import get_current_user

from ..db import get_connection
# lib
from sqlalchemy.ext.asyncio import AsyncSession

import datetime

import uuid

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import APIRouter,  Depends, Request, Response, HTTPException
from fastapi.params import Cookie
from loguru import logger
from sqlalchemy import select
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer = HTTPBearer()


app =APIRouter(prefix="/auth", tags=['auth'])


    

@app.post("/register")
async def register_user(data:UserRegister, connection:AsyncSession = Depends(get_connection)):
    
    token = await UserCrud.create_user(data, conn=connection)
    
    return token



@app.post("/login")
async def login_user(data:LoginUser, connection:AsyncSession = Depends(get_connection)):
    
        
        user = await connection.scalar(select(User).where(User.passport_data == data.passport_data, 
                                                          User.email == data.email, 
                                                          User.code == data.code))
        if user:
            if check_password(user.password, data.password):
                
                token = await create_access_token({
                "user_id": user.id,
                "time":(datetime.datetime.now(datetime.UTC) +datetime.timedelta(days=7)).timestamp() 
                })
                
                return token
                    
        raise  HTTPException(status_code=404, detail={
            "data":"Not valid",
            "status":404
        })
    
        

@app.get("/me")
async def me(me:User = Depends(get_current_user)): 
        return me

@app.put("/update")
async def update_user(data:UpdateUser ,me:User = Depends(get_current_user), connection:AsyncSession = Depends(get_connection)):
    update_data = await UserCrud.update_user(user = me, connection = connection, data = data)
    
    return update_data

@app.post("/password/update")
async def get_url_for_change(email:EmailStr, connection:AsyncSession = Depends(get_connection)):
    user = await connection.scalar(select(User).where(User.email == email))
    if user:
    
    
        pk = uuid.uuid1()
        url = f"http://127.0.0.1:8000/password/update/{pk}"
        
        url_model = UrlForUpdatePassword(id = pk)
        url_model.user = user
        
        connection.add(url_model)
        
        await connection.commit()
        
        
        return url
    
    
    raise HTTPException(status_code=404, detail={"email":"not valid", "status":404})



@app.put("/password/update/{token}")
async def update_password(new_password:str,token:uuid.UUID, connection:AsyncSession = Depends(get_connection)):
    
    data = await UserCrud.update_password(new_password=new_password, token=token,session= connection)

    return data

@app.get("/all_users")
async def all_users(connection:AsyncSession = Depends(get_connection)):
    user = await connection.scalars(select(User))
    
    return user.all()

@app.post("/decode_token")
async def tokens(token:HTTPAuthorizationCredentials = Depends(bearer)):
    
    return await valid_access_token(token=token.credentials)