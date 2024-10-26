from sqlalchemy import Column, BIGINT, INT, DOUBLE, String, DATETIME
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class LearningResult(Base):
    __tablename__ = "learning_result"

    id = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    latitude = Column(DOUBLE, nullable=False)
    longitude = Column(DOUBLE, nullable=False)
    administrative_district = Column(String(100), nullable=False)
    district_code = Column(String(15), nullable=False)
    risk = Column(DOUBLE, nullable=False)
    report_count = Column(INT, default=0, nullable=False)
    status = Column(String(20), default='미처리', nullable=False)
    start_prediction_time = Column(DATETIME(6), nullable=False)

    def __init__(self, latitude, longitude, administrative_district, district_code, risk, start_prediction_time):
        self.latitude = latitude
        self.longitude = longitude
        self.administrative_district = administrative_district
        self.district_code = district_code
        self.risk = risk
        self.start_prediction_time = start_prediction_time

class CityDistrict(Base):
    __tablename__ = "city_district"

    id = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    code = Column(String(15), nullable=False, unique=True)
    city = Column(String(10), nullable=False)
    district = Column(String(20), nullable=False)
    country = Column(String(20), nullable=False)

    def __init__(self, code, city, district, country):
        self.code = code
        self.city = city
        self.district = district
        self.country = country