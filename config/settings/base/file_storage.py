from decouple import config
from django.conf import settings
        

DEFAULT_FILE_STORAGE = 'config.file_storage.CustomS3Boto3Storage'
AWS_ACCESS_KEY_ID = 'test_access_key'
AWS_SECRET_ACCESS_KEY = 'test_secret_key'
AWS_STORAGE_BUCKET_NAME = 'my_bucket'
AWS_S3_REGION_NAME = 'us-east-1' 
AWS_S3_ENDPOINT_URL = 'http://s3:9090'
AWS_S3_USE_SSL = False
AWS_S3_VERIFY = False
AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN', default="http://localhost:9090")
AWS_QUERYSTRING_AUTH = False
