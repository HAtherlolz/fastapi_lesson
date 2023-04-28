import boto3

from fastapi import UploadFile
from config.conf import settings


async def is_file_valid(file: UploadFile) -> bool:
    megabyte_limit = 20
    allowed_extensions = ['png', 'jpg', 'jpeg']
    if not file.filename.split('.')[1].lower() in allowed_extensions:
        return False
    if file.size > megabyte_limit * 1024 * 1024:
        return False
    return True


async def upload_file_to_s3(file: UploadFile, image_path: str) -> str:
    """ Upload file to s3 bucket """
    s3 = boto3.resource(
        "s3", aws_access_key_id=settings.AWS_BUCKET_KEY_ID, aws_secret_access_key=settings.AWS_BUCKET_SECRET_KEY
    )
    bucket = s3.Bucket(settings.AWS_BUCKET_NAME)
    bucket.upload_fileobj(file.file, image_path, ExtraArgs={"ACL": "public-read"})
    uploaded_file_url = f"https://{settings.AWS_BUCKET_NAME}.s3.amazonaws.com/{image_path}"
    return uploaded_file_url
