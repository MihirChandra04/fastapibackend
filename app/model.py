from pydantic import BaseModel, EmailStr

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
