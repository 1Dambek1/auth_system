

# lib
from fastapi import   Depends, HTTPException


from sqlalchemy import select

# from main folder

# from this folder
from .db import get_connection
from .auth.models_user import User
from .auth.utlils.auth_work import valid_access_token
# lib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer = HTTPBearer()

async def get_current_user(token:HTTPAuthorizationCredentials = Depends(bearer),connection:AsyncSession = Depends(get_connection)):
    
    user_id = await valid_access_token(token=token.credentials)
    user = await connection.scalar(select(User).where(User.id == user_id))
    
    if user:
    
        return user
    raise HTTPException(status_code=404, detail={
        "token":"Not actual",
        "status":404
    })