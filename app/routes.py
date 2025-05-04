from fastapi import APIRouter, HTTPException
from .model import FormData,AddressUpdate
from .database import collection
from pydantic import EmailStr

router = APIRouter()

@router.get("/user")
async def get_data(email : dict):
    try:
        data = collection.find_one({"email":email["email"]})
        data["_id"] = str(data["_id"])
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update-address/{email}")
async def update_address(email: EmailStr, address: AddressUpdate):
    result = collection.update_one(
        {"email": email},
        {"$set": {
            "street_address": address.street_address,
            "city": address.city,
            "state": address.state,
            "country": address.country,
            "postalCode": address.postalCode
        }}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Address updated successfully"}

@router.post("/submit")
async def submit_form(data: FormData):
    try:
        collection.insert_one(data.model_dump())
        return {"message": "Form data saved successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# In Pydantic v1 → data.dict() was used
# In Pydantic v2 → .model_dump() is more flexible, supports customization and is future-proof