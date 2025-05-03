from fastapi import APIRouter, HTTPException
from .model import FormData
from .database import collection

router = APIRouter()

@router.get("/user")
async def get_data(name : dict):
    try:
        data = collection.find_one({"firstname":name["name"]})
        data["_id"] = str(data["_id"])
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/submit")
async def submit_form(data: FormData):
    try:
        collection.insert_one(data.model_dump())
        return {"message": "Form data saved successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# In Pydantic v1 → data.dict() was used
# In Pydantic v2 → .model_dump() is more flexible, supports customization and is future-proof