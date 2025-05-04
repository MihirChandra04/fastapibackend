from pydantic import BaseModel, EmailStr
from typing import Optional

class FormData(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    country: str
    street_address: str
    city: str
    state: str
    postalCode: str
    comments: bool
    candidates: bool
    offers: bool
    pushnotification: str


class AddressUpdate(BaseModel):
    street_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postalCode: Optional[str] = None