from dbutils import engineconn
from db_models import LearningResult, CityDistrict
from sqlalchemy.orm import Session
from sqlalchemy import and_

engine_conn = engineconn()

def save_learning_result(data: LearningResult):
    # DB 세션 생성
    print('save start')
    session: Session = engine_conn.get_session()
    
    try:
        # 데이터베이스에 추가하고 커밋
        print('before data commit')
        session.add(data)
        session.commit()
        print('data commit, success save')
    except Exception as e:
        session.rollback()
        print(f"Error saving to database: {e}")
    finally:
        print('save data end')
        session.close()


def findByOnlyDistrict(district1, district2):
    try:
        session: Session = engine_conn.get_session()
        return session.query(CityDistrict).filter(
                and_(
                    CityDistrict.district.like(f"%{district1}%"),
                    CityDistrict.district.like(f"%{district2}%"),
                )
            ).all()
    finally:
        session.close()


def findByCityAndDistrict(city, district):
    try:
        session: Session = engine_conn.get_session()
        return session.query(CityDistrict).filter(
                and_(
                    CityDistrict.city.like(f"%{city}%"),
                    CityDistrict.district.like(f"%{district}%"),
                )
            ).all()
    finally:
        session.close()

def findByCity(city):
    try:
        session: Session = engine_conn.get_session()
        return session.query(CityDistrict).filter(
                CityDistrict.city.like(f"%{city}%")
            ).all()
    finally:
        session.close()

def findByDistrict(district):
    try:
        session: Session = engine_conn.get_session()
        return session.query(CityDistrict).filter(
                CityDistrict.district.like(f"%{district}%")
            ).all()
    finally:
        session.close()

def findByCityAndDistricts(city, district1, district2):
    try:
        session: Session = engine_conn.get_session()
        return session.query(CityDistrict).filter(
                and_(
                    CityDistrict.city.like(f"%{city}%"),
                    CityDistrict.district.like(f"%{district1}%"),
                    CityDistrict.district.like(f"%{district2}%")
                )
            ).all()
    finally:
        session.close()