from io import BytesIO
import boto3
from buckets.models import Bucket
import string    
import random
from datetime import datetime



class BucketUtils():

    def upload_file_obj(self,bucket,company,in_file,ftype,type,out_filename):
        s3 = boto3.client('s3',aws_access_key_id=bucket.aws_access_key_id,aws_secret_access_key=bucket.aws_secret_access_key)
        rstring=''.join(random.choices(string.ascii_lowercase + string.digits, k = 8))
        out_filename=type.lower()+"_"+ftype.lower()+"_"+datetime.now().strftime("%d%m%Y_%H%M%S")+"_"+rstring+".xlsm"
        path="vendors/"+company.vid+"/"+type.lower()+"/"+ftype.lower()+"/"+out_filename
        try:
            s3.upload_fileobj(in_file, "amos-bucket-v2z4s5", path)
        except:
            return False
        return path

    def get_obj(self,path):

        bucket=Bucket.objects.all()[0]
        s3 = boto3.client('s3',aws_access_key_id=bucket.aws_access_key_id,aws_secret_access_key=bucket.aws_secret_access_key)
        try:
            f=BytesIO()
            s3.download_fileobj('amos-bucket-v2z4s5', path, f)
            return f
        except:
            return False