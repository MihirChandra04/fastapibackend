from fastapi import APIRouter, HTTPException
from .model import FormData
from .database import collection

router = APIRouter()

@router.get('/')
async def data():
    return("data")

@router.post("/submit")
async def submit_form(data: FormData):
    try:
        collection.insert_one(data.model_dump())
        return {"message": "Form data saved successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# In Pydantic v1 → data.dict() was used
# In Pydantic v2 → .model_dump() is more flexible, supports customization and is future-proof