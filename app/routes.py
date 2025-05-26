from fastapi import APIRouter, HTTPException,status
from .model import FormData,AddressUpdate
from .database import collection
from pydantic import EmailStr

router = APIRouter()

@router.get("/user")
async def get_data(email : str):
    try:
        data = collection.find_one({"email":email})
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


@router.delete('/delete/{email}')
async def delete_data(email: str):
    try:
        data =  collection.find_one({"email": email})
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Form data with email {email} not found"
            )

        result =  collection.delete_one({"email": email})
        if result.deleted_count == 1:
            return {"message": f"Form data with email {email} deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete the document"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )


@router.get("/all-users")
async def get_all_users():
    try:
        data = []
        for doc in collection.find():
            doc["_id"] = str(doc["_id"])  # Make ObjectId JSON serializable
            data.append(doc)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error occurred: {str(e)}")

    
# In Pydantic v1 → data.dict() was used
# In Pydantic v2 → .model_dump() is more flexible, supports customization and is future-proof