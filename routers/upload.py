from fastapi import APIRouter
from storage import generate_upload_signed_url
import os


router = APIRouter()

GCP_BUCKET_NAME = os.getenv("GCP_BUCKET_NAME")

@router.get("/generate-upload-url/{filename}")
async def get_upload_url(filename: str):
    """Returns a signed URL for direct client upload."""
    print("received url: ", filename)
    signed_url_data = generate_upload_signed_url(GCP_BUCKET_NAME, filename)
    return signed_url_data