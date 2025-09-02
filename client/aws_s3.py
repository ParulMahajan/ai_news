import boto3
import os
from io import BytesIO
from PIL import Image
from utils.logger import logger
from dotenv import load_dotenv
load_dotenv()
import os

os.environ["AWS_ACCESS_KEY_ID"]
os.environ["AWS_SECRET_ACCESS_KEY"]

def upload_image_to_s3(image_bytes: bytes, bucket_name: str="news--image", region: str = "ap-southeast-1") -> str:
    try:
        # --- Convert image to JPEG ---
        img = Image.open(BytesIO(image_bytes))
        if img.mode in ['RGBA', 'LA']:
            img = img.convert('RGB')
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        jpeg_bytes = buffer.getvalue()

        # --- Generate a unique filename ---
        import uuid
        image_key = f"{uuid.uuid4().hex}.jpg"

        # --- Upload to S3 ---
        s3 = boto3.client("s3", region_name=region)
        resp = s3.put_object(
            Bucket=bucket_name,
            Key=image_key,
            Body=jpeg_bytes,
            ContentType="image/jpeg"
        )

        # --- Construct public URL ---
        public_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{image_key}"
        logger.info(f"✅ S3 public URL for Instagram: {public_url}")
        return public_url

    except Exception as e:
        logger.error(f"❌ S3 upload failed: {e}")
        return ""
