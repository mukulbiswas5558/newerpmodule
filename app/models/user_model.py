from pydantic import BaseModel
from datetime import datetime
from typing import Optional




class CreateUser(BaseModel):
    name: str
    username: str
    password: str
    role: str = 'user'  # Default value for role is 'user'


class UpdateUser(BaseModel):
    phone: str
    department: Optional[str] = None
    shift_information: Optional[str] = None
    employee_type: Optional[str] = None
    job_position: Optional[str] = None
    reporting_manager: Optional[str] = None
    work_location: Optional[str] = None
    work_type: Optional[str] = None
    salary: Optional[str] = None
    company: Optional[str] = None
    bank_name: Optional[str] = None
    branch: Optional[str] = None
    bank_address: Optional[str] = None
    bank_code_1: Optional[str] = None
    bank_code_2: Optional[str] = None
    account_number: Optional[str] = None
    bank_country: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    
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
