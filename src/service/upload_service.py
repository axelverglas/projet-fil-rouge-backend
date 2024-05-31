import boto3
from botocore.exceptions import NoCredentialsError
import os

class UploadService:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            region_name=os.getenv('AWS_S3_REGION'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        self.bucket = os.getenv('AWS_S3_BUCKET')

    def upload_file(self, file_name, file):
        try:
            self.s3_client.upload_fileobj(
                Fileobj=file,
                Bucket=self.bucket,
                Key=file_name,
                ExtraArgs={'CacheControl': 'max-age=31536000'}
            )
        except NoCredentialsError:
            print("Credentials not available")
            return False
        return True

    def delete_file(self, file_name):
        try:
            self.s3_client.delete_object(Bucket=self.bucket, Key=file_name)
        except NoCredentialsError:
            print("Credentials not available")
            return False
        return True

    def get_file_url(self, file_name):
        url = self.s3_client.generate_presigned_url('get_object', 
                                                    Params={'Bucket': self.bucket, 'Key': file_name})
        return url
