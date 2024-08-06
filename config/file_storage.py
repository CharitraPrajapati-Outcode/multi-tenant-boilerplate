from decouple import config
from storages.backends.s3boto3 import S3Boto3Storage


class CustomS3Boto3Storage(S3Boto3Storage):
    if config('DEBUG', cast=bool):
        def url(self, name, parameters=None, expire=None):
            url = super().url(name, parameters=parameters, expire=expire)
            return url.replace('https://', 'http://')