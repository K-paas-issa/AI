from fastapi import FastAPI
import os
import boto3

service_name = 's3'
endpoint_url = 'https://kr.object.ncloudstorage.com'
region_name = 'kr-standard'
access_key = os.getenv('NCP_ACCESSKEY')
secret_key = os.getenv('NCP_SECRETKEY')

app = FastAPI()

@app.get("/")
def simulation(object_name):
    res = download_csv(object_name) # test.csv로 다운로드한 상태
    
    '''
    여기서 시뮬레이션 또는 학습하길 바람.
    파이썬 시뮬레이션 버전 = ?
    파이썬 학습 버전 = ?
    '''
    
    return {"message" : res}

def download_csv(object_name):
    s3 = boto3.client(service_name, endpoint_url=endpoint_url, aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)
    bucket_name = 'contest73-bucket'

    local_file_path = 'test.csv'
    try:
        s3.download_file(bucket_name, object_name, local_file_path)
        return 'success'
    except Exception as e:
        print(f"Exception occurred: {str(e)}")  # 예외 메시지 출력
        return 'exception throws'