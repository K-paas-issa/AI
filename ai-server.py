from fastapi import FastAPI
import s3utils
from dbutils import engineconn
from db_models import LearningResult
from sqlalchemy.orm import Session
import main
from geopy.geocoders import Nominatim

app = FastAPI()
engine_conn = engineconn()

@app.get("/simulation-data")
def learning(path : str):
    download_path = s3utils.download_csv(path) # ai_input.npy로 다운받은 상태.
    print(download_path)

    # 다운받은 csv파일의 경로 매개변수, 실제로 학습하는 함수
    # learning_res는 ai.output.csv 문자열
    start_learning(download_path) 

    return 'success'


def start_learning(ai_input_data):
# 매개변수는 다운받은 ai_input.npy파일
# 실제 학습이 진행되는 함수
# TODO : 실제 학습 부분 구현
# 여기서 학습 결과로 나온 csv파일 ai_output.csv로 저장할 것
    
    print('main call')
    res_list = main.main2(ai_input_data)
    print('main call end')
    # 각 객체 생성 및 db 저장
    for i in range(3):
        tmp_dict = res_list[i]

        latitude=tmp_dict["latitude"]
        longitude=tmp_dict["longitude"]

        district = get_administrative_district(latitude, longitude)

        # LearningResult 객체 생성
        learning_result = LearningResult(
            latitude,
            longitude,
            district,
            risk=tmp_dict["risk"],
            start_prediction=tmp_dict["start_prediction_time"]
        )
        
        save_learning_result(learning_result)

    return

def get_administrative_district(lat, lng):
    print('convert to district start')
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    res = geolocoder.reverse([lat, lng], exactly_one=True, language='ko')

    return res.address


def save_learning_result(data: LearningResult):
    # DB 세션 생성
    print('save start')
    session: Session = engine_conn.get_session()
    
    try:
        # 데이터베이스에 추가하고 커밋
        session.add(data)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error saving to database: {e}")
    finally:
        print('save data end')
        session.close()

