import datetime
import typing
import uuid
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .enums_user import SexEnumss

from ..metadata import Base

from enum import Enum








class User(Base):
    
    __tablename__ = "user_table"
    
    # data name
    first_name:Mapped[str]
    second_name:Mapped[str]
    third_name:Mapped[str]
    
    # passport data
    passport_data:Mapped[str] = mapped_column(String(length=11), unique=True)
    
    # dates
    date_to_birth:Mapped[datetime.date]
    date_passport:Mapped[datetime.date]
    
    # sex
    sex:Mapped[SexEnumss]
    
    # passwords
    password:Mapped[bytes]
    code:Mapped[str] = mapped_column(String(6))
    
    email:Mapped[str] = mapped_column(unique=True)
    
    is_active:Mapped[bool] = mapped_column(default=True)
    



class UrlForUpdatePassword(Base):
    
    __tablename__ = "url_update_passowrd" 
    
    id:Mapped[uuid.UUID] = mapped_column(primary_key=True)
    
    
    user_id:Mapped[int] = mapped_column(ForeignKey("user_table.id", ondelete="CASCADE"), unique=True)
    
    
    user:Mapped["User"] = relationship(uselist=False)