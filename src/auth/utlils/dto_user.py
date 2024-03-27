import datetime
from pydantic import BaseModel, EmailStr, validator

from enum import Enum

from ..models_user import SexEnumss



    
class UserRegister(BaseModel):
    first_name:str
    second_name:str
    third_name:str
    
    email:EmailStr
    
    
    passport_data:str 
    
    date_to_birth:datetime.date
    date_passport:datetime.date
    
    
    sex:SexEnumss
    
    
    password:str|bytes
    code:str
    # validators
    @validator("passport_data")
    def valid_passport_data(cls,value):
        if len(str(value)) == 10:
            return value
        raise ValueError("Not valid passport data")
        
        
    @validator("code")
    def valid_code(cls, value):
        if len(str(value)) == 6:
                    return value
        raise ValueError("Not valid code")


class LoginUser(BaseModel):
    
    passport_data:str
    
    email:EmailStr
    
    
    password:str
    
    code:str



class GiveaDataUser(BaseModel):
    
    first_name:str
    second_name:str
    third_name:str
    
    email:EmailStr
    
    
    passport_data:str
        
    date_to_birth:datetime.date
    date_passport:datetime.date
    
    
    sex:SexEnumss
    
    code:str



class UpdateUser(BaseModel):
    first_name:str
    second_name:str
    third_name:str
    
    email:EmailStr
    
    
    passport_data:str 
    
    date_to_birth:datetime.date
    date_passport:datetime.date
    
    
    sex:SexEnumss
    
    
    code:str
    # validators
    @validator("passport_data")
    def valid_passport_data(cls,value):
        if len(str(value)) == 10:
            return value
        raise ValueError("Not valid passport data")
        
        
    @validator("code")
    def valid_code(cls, value):
        if len(str(value)) == 6:
                    return value
        raise ValueError("Not valid code")
