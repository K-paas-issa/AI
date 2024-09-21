import boto3
import collections
collections.Callable = collections.abc.Callable


service_name = 's3'
endpoint_url = 'https://kr.object.ncloudstorage.com'
region_name = 'kr-standard'
access_key = '3947F4C4535058753EAF'
secret_key = 'EE4E3873904FA3E16BFFF276AAC183FD4CDF302A'

if __name__ == "__main__":
 
    s3 = boto3.client(service_name, endpoint_url=endpoint_url, aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)
    bucket_name = 'contest73-bucket'

    object_name = 'climate_data_21:41:46.149013.csv'
    local_file_path = './data/data.csv'
    

    s3.download_file(bucket_name, object_name, local_file_path)
