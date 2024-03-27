import os

from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings


BASE_DIR  = Path(__file__).parent.parent



class AuthJWTTokens(BaseModel):
    
    private_key:Path = BASE_DIR / "src" / "auth" / "keys" / "private_key.pem"
    
    public_key:Path = BASE_DIR /  "src" / "auth" / "keys" / "public_key.pem"  
    
    algorithm:str = "RS256"  
    

class Config(BaseSettings):
    secret_key:str  = "sdfkjbgbdjnkfghkjdgkjfkglhjiledhgkjdhgkjhlhjdkghkjkhdassadS"
          
    DB_URl:str = "postgres+asyncpg://postgres_test:KgHC4y8PNeR6iZtwooalIonOPF7qYoA6@dpg-co2149md3nmc73a2clc0-a/postgres_test_vgac"
    
    jwt_keys:AuthJWTTokens  = AuthJWTTokens()
    
    
    
    
    
config = Config()