from db_models import LearningResult
import main
from geopy.geocoders import Nominatim
import math
import repository
import s3utils

start_latitude = 37.9381943
start_longitude = 126.5877948

def start_learning(path):

    ai_input_data = s3utils.download_csv(path)

    print('main call')
    res_list = main.main2(ai_input_data)
    if res_list == None or res_list == []:
        print('rl fault')
        return
    
    print('in ai-server ', res_list)
    print('main call end')
    if len(res_list) != 3:
        print('res list size : ', len(res_list))
    
    # 각 객체 생성 및 db 저장
    for i in range(len(res_list)):
        tmp_dict = res_list[i]
        
        latitude=tmp_dict["latitude"]
        longitude=tmp_dict["longitude"]
        print('latitude = {} longitude : {}'.format(latitude, longitude))
            
        after_lat, after_lng = calculate_new_position(latitude, longitude) # 변환 후 위경도

        district = get_administrative_district(after_lat, after_lng)

        if district == None:
            district_code = None
        else:
            print('district = {}'.format(district))
            district_arr = district.split(',')

            if not isInKorea(district_arr):
                continue
            
            district_code = get_district_code(district_arr)
            print(district_code)

            district = rearrange_district(district_arr)
            
        if district == None or district_code == None:
            continue

        learning_result = LearningResult(
            after_lat,
            after_lng,
            district,
            district_code,
            risk=tmp_dict["risk"],
            start_prediction_time=tmp_dict["start_prediction_time"]
        )
        
        repository.save_learning_result(learning_result)
    return

def rearrange_district(district_arr):
    filtered_words = [word.strip() for word in district_arr if not word.strip().isdigit()]
    reversed_words = filtered_words[::-1]
    res_string = ' '.join(reversed_words)
    
    return res_string

def isInKorea(district_arr):
    if district_arr[-1].strip() != '대한민국':
        return False
    return True
        

def get_district_code(district_arr):
    try:
        # Check the length of district_arr 단어가 2개 이하거나, 3개이면서 2번째 단어가 숫자일 경우
        if len(district_arr) < 3 or (len(district_arr) < 4 and district_arr[-2].isdigit() == True):
            return None
        
        # 숫자가 없는 경우. 태안군, 충청남도, 대한민국의 경우
        results = repository.findByCityAndDistrict(district_arr[-2].strip(), district_arr[-3].strip())
        if len(results) == 1:
            return results[0].code

        # 숫자가 없는 경우. 일산동구, 고양시, 대한민국의 경우
        results = repository.findByOnlyDistrict(district_arr[-2].strip(), district_arr[-3].strip())
        if len(results) == 1:
            return results[0].code
        
        # 세종특별자치시의 경우
        results = repository.findByCity(district_arr[-3].strip())
        if len(results) == 1:
            return results[0].code
        
        # 양주시, 21341, 대한민국의 경우
        results = repository.findByDistrict(district_arr[-3].strip())
        if district_arr[-3].strip() == '양주시':
            return 41630
        if len(results) == 1:
            return results[0].code
        
        # 설악로, 임천리, 양양군, 강원특별자치도, 25035, 대한민국의 경우
        results = repository.findByCityAndDistrict(district_arr[-3].strip(), district_arr[-4].strip())
        if len(results) == 1:
            return results[0].code

        # 풍산동, 일산동구, 고양시, 10442, 대한민국의 경우
        results = repository.findByOnlyDistrict(district_arr[-3].strip(), district_arr[-4].strip())
        if len(results) == 1:
            return results[0].code
        
        # 전주시청, 기린대로, 서노송동, 완산구, 전주시, 전북특별자치도, 55032, 대한민국의 경우
        results = repository.findByCityAndDistricts(district_arr[-3].strip(), district_arr[-4].strip(), district_arr[-5].strip())
        if len(results) == 1:
            return results[0].code
        
        return None
    except Exception as e:
        print(f"쿼리 실행 중 오류 발생: {e}")
    finally:
        print('save data end')


def get_administrative_district(lat, lng):
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