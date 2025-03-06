from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models import ImageMetadata
from storage import generate_upload_signed_url
from database import get_db
import os


router = APIRouter()

GCP_BUCKET_NAME = os.getenv("GCP_BUCKET_NAME")

@router.get("/generate-upload-url/{filename}")
async def get_upload_url(filename: str, request: Request):
    """Returns a signed URL for direct client upload."""
    print("received url: ", filename)
    signed_url_data = generate_upload_signed_url(GCP_BUCKET_NAME, filename)
    return signed_url_data

@router.post("/image-metadata")
async def update_image_metadata(data: dict, request: Request, db: AsyncSession = Depends(get_db)):
    """update image metadata after the image upload process"""
    print("received data: ", data)
    headers = request.headers
    user_id = headers.get("x-user-id")
    file_url = data['file_path']
    file_name = data['file_name']

    new_image = ImageMetadata(user_id=user_id, file_path=file_url, file_name=file_name, status="uploaded")

    db.add(new_image)
    await db.commit()
    await db.refresh(new_image)

    return {"message": "Image Added Successfully"}
    

        

