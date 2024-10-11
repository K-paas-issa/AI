from fastapi import FastAPI, BackgroundTasks
import s3utils
from dbutils import engineconn
from db_models import LearningResult, CityDistrict
from sqlalchemy.orm import Session
from sqlalchemy import and_
import main
from geopy.geocoders import Nominatim
from fastapi import status
from fastapi import Response
import math

app = FastAPI()
engine_conn = engineconn()
start_latitude = 37.9381943
start_longitude = 126.5877948

@app.get("/simulation-data")
def learning(path : str, background_tasks: BackgroundTasks):
    download_path = s3utils.download_csv(path) # ai_input.npy로 다운받은 상태.
    print(download_path)

    # 다운받은 csv파일의 경로 매개변수, 실제로 학습하는 함수
    # learning_res는 ai.output.csv 문자열
    background_tasks.add_task(start_learning, download_path) 

    return Response(status_code=status.HTTP_200_OK)


def start_learning(ai_input_data):
# 매개변수는 다운받은 ai_input.npy파일
# 실제 학습이 진행되는 함수
# TODO : 실제 학습 부분 구현
# 여기서 학습 결과로 나온 csv파일 ai_output.csv로 저장할 것
    print('main call')
    res_list = main.main2(ai_input_data)
    if res_list == None or res_list == []:
        print('rl fault')
        return
    
    print('in ai-server ', res_list)
    print('main call end')
    if len(res_list) != 3:
        print('res list size : ', len(res_list))
        return
    
    # 각 객체 생성 및 db 저장
    for i in range(3):
        tmp_dict = res_list[i]
        
        latitude=tmp_dict["latitude"]
        longitude=tmp_dict["longitude"]
        print('latitude = {} longitude : {}'.format(latitude, longitude))
            
        after_lat, after_lng = calculate_new_position(latitude, longitude) # 변환 후 위경도

        district = get_administrative_district(after_lat, after_lng)

        if district == None:
            district_code = None
        else:
            district_arr = district.split(',')
            district_code = get_district_code(district_arr)
            print(district_code)
            print('district = {}'.format(district))

        # LearningResult 객체 생성
        learning_result = LearningResult(
            after_lat,
            after_lng,
            district,
            district_code,
            risk=tmp_dict["risk"],
            start_prediction_time=tmp_dict["start_prediction_time"]
        )
        
        save_learning_result(learning_result)

    return

def get_district_code(district_arr):

    session: Session = engine_conn.get_session()
    try:
        # 대한민국이 아닐경우
        results = session.query(CityDistrict).filter(
            CityDistrict.city.like(f"%{district_arr[-1].strip()}%")
        ).all()
        if results == None:
            return None
        
        # Check the length of district_arr
        if len(district_arr) < 4:
            return None
        
        # 세종특별자치시의 경우
        print(district_arr[-3])
        results = session.query(CityDistrict).filter(
            CityDistrict.city.like(f"%{district_arr[-3].strip()}%")
        ).all()
        if len(results) == 1:
            return results[0].code
        
        # 부산동, 오산시, 18132, 대한민국과 같은 경우
        results = session.query(CityDistrict).filter(CityDistrict.district.like(f"%{district_arr[-3].strip()}%")).all()
        if len(results) == 1:
            return results[0].code
        
        # 설악로, 임천리, 양양군, 강원특별자치도, 25035, 대한민국의 경우
        results = session.query(CityDistrict).filter(
            and_(
                CityDistrict.city.like(f"%{district_arr[-3].strip()}%"),
                CityDistrict.district.like(f"%{district_arr[-4].strip()}%"),
            )
        ).all()
        if len(results) == 1:
            return results[0].code
        
        # 전주시청, 기린대로, 서노송동, 완산구, 전주시, 전북특별자치도, 55032, 대한민국의 경우
        results = session.query(CityDistrict).filter(
            and_(
                CityDistrict.city.like(f"%{district_arr[-3].strip()}%"),
                CityDistrict.district.like(f"%{district_arr[-4].strip()}%"),
                CityDistrict.district.like(f"%{district_arr[-5].strip()}%")
            )
        ).all()
        if len(results) == 1:
            return results[0].code
        
        return None
    finally:
        print('save data end')
        session.close()

def get_administrative_district(lat, lng):
    print('convert to district start')

    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    res = geolocoder.reverse([lat, lng], exactly_one=True, language='ko')
    if res==None:
        return None
    print('res = {}'.format(res))
    return res.address

def calculate_new_position(variable_latitude_km, variable_longitude_km):
    # 지구의 반지름 (킬로미터)
    R = 6371.0

    # 위도 이동 (남북)
    delta_lat = variable_latitude_km / R
    new_lat = start_latitude + math.degrees(delta_lat)

    # 경도 이동 (동서)
    delta_lon = variable_longitude_km / (R * math.cos(math.radians(start_latitude)))
    new_lon = start_longitude + math.degrees(delta_lon)

    return new_lat, new_lon



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

