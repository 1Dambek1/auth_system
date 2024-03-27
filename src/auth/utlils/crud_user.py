
# import from project
import datetime
import json

from fastapi import HTTPException
from .dto_user import UserRegister, LoginUser,UpdateUser
from ..models_user import UrlForUpdatePassword, User
from .auth_work import encode_password, create_access_token, check_password

# lib


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, update
from sqlalchemy.orm import joinedload



class UserCrudClass:
    
    # create_user_with_generate_token_and_hash_password
    async def create_user(self,data:UserRegister, conn:AsyncSession):
        # create_user
        data.password = encode_password(passowrd=data.password)
        user =User(**data.model_dump())

        conn.add(user)
        await conn.flush()

        # access_token
        token = await create_access_token({
            "user_id": user.id,
            "time":(datetime.datetime.now(datetime.UTC) +datetime.timedelta(days=7)).timestamp() 
            })
        
        await conn.commit()        
            
        return token
    
    
     
    async def update_user(self, user:User, data:UpdateUser,connection:AsyncSession):

        for field, value in data.model_dump().items():
            setattr(user, field,value)

        
        
        
        
        await connection.commit()
        
        
        print("work"*1000)
        
        return True
    

    async def update_password(self,new_password, token, session):
            
        url:UrlForUpdatePassword = await session.scalar(select(UrlForUpdatePassword).options(joinedload(UrlForUpdatePassword.user)).where(UrlForUpdatePassword.id == token))
        print(url)
        if url:
            
            password =  encode_password(new_password)
            
            url.user.password = password
            
            await session.execute(delete(UrlForUpdatePassword).where(UrlForUpdatePassword.id == url.id))
            
            await session.commit()
            
            return True
            
        raise HTTPException(status_code=404, detail={"url":"not valid", "status":404})
        
        
    
    
UserCrud = UserCrudClass()