import minio


def check_obj_exists(s3: minio.Minio, bucket_name, object_name):
    try:
        return s3.stat_object(bucket_name, object_name)
    except minio.error.S3Error:
        return False
