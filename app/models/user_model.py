from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__ident="2b", deprecated="auto")



class CreateUser(BaseModel):
    name: str
    username: str
    password: str
    role: str = 'user'  # Default value for role is 'user'
    def hash_password(self):
        self.password = pwd_context.hash(self.password)
class LoginUser(BaseModel):
    username: str
    password: str   

class User(BaseModel):
    id: int
    name: str
    username: str
    password: Optional[str] = None  # Make password optional
    role: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        # Automatically convert datetime to string (ISO format)
        anystr_strip_whitespace = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if isinstance(v, datetime) else str(v)
        }
