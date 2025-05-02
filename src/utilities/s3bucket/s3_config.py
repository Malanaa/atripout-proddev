import boto3
import os 
from dotenv import load_dotenv

load_dotenv()

aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')

s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

# #Image compression
# img = Image.open(image)
# img_io = io.BytesIO()
# img = img.convert("RGB")
# img.save(img_io, format="JPEG", quality=85, optimize=True)
# img_io.seek(0)
# #Image compression End

# s3.upload_fileobj(
# img_io,
# "atripout-images",
# unique_key,
# ExtraArgs={
# "ACL": "public-read",
# "ContentType": "image/jpeg", #Jpeg specifier
# },
# )
# s3_url = f"https://atripout-images.s3.us-east-2.amazonaws.com/{unique_key}"
# posts.update_one({"_id": post_id}, {"$set": {"image_url": s3_url}})