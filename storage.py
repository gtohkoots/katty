import os
import mimetypes
from google.cloud import storage
from dotenv import load_dotenv
from datetime import timedelta


load_dotenv()

CRED = os.getenv("GCP_CREDENTIALS_JSON")

storage_client = storage.Client.from_service_account_json(CRED)


def generate_upload_signed_url(bucket_name: str, blob_name: str, expiration_minutes: int = 15):
    """Generates a pre-signed URL allowing direct client uploads to GCS."""
    
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Determine content type based on file extension
    content_type, _ = mimetypes.guess_type(blob_name)
    if not content_type:
        content_type = "application/octet-stream"  # Default if unknown

    print("mime type guessed: ", content_type)

    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=expiration_minutes),
        method="PUT",  # Use PUT for file uploads
        content_type=content_type  # Ensure correct content type
    )

    print("Generated GET signed URL:")
    print(url)

    return {"upload_url": url, "blob_name": blob_name}