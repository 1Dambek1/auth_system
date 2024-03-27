
import datetime
import jwt
import bcrypt
from ...config import config


from loguru import logger
from fastapi.exceptions import HTTPException

# work with token
async def create_access_token(payload:dict, 
                              algorithm:str = config.jwt_keys.algorithm, 
                              private_key:str = config.jwt_keys.private_key.read_text()) -> str :
        
        
        token = jwt.encode(payload=payload, algorithm=algorithm, key=private_key)
        return token

async def valid_access_token(
        token,
        algorithm:str = config.jwt_keys.algorithm,
        public_key:str = config.jwt_keys.public_key.read_text()
        ) -> dict:
        
    # определять срок годности и валидность token и при успешном возращать id или False
    
    try:
        payload = jwt.decode(jwt = token, key=public_key, algorithms=[algorithm])
    except:
        raise HTTPException(status_code=404, detail={
            "token":"not_valid",
            "status":404
    })
    if payload.get("time"):
        times = payload['time']
        if times > datetime.datetime.now(datetime.UTC).timestamp():
                return payload["user_id"]
    raise HTTPException(status_code=404, detail={
            "token":"not_valid",
            "status":404
    })
    
#  work with password

def encode_password(passowrd:str) -> bytes:
        passowrd = bcrypt.hashpw(password=passowrd.encode(),salt=bcrypt.gensalt())
        return passowrd


def check_password(our_password:bytes,new_password:str) -> bool:
    return (bcrypt.checkpw(password=new_password.encode(), hashed_password=our_password))
    