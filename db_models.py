from sqlalchemy import Column, BIGINT, DOUBLE, String, DATETIME
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class LearningResult(Base):
    __tablename__ = "learning_result"

    id = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    latitude = Column(DOUBLE, nullable=False)
    longitude = Column(DOUBLE, nullable=False)
    administrative_district = Column(String(100), nullable=False)
    risk = Column(DOUBLE, nullable=False)
    start_prediction_time = Column(DATETIME(6), nullable=False)

    def __init__(self, latitude, longitude, administrative_district, risk, start_prediction_time):
        self.latitude = latitude
        self.longitude = longitude
        self.administrative_district = administrative_district
        self.risk = risk
        self.start_prediction_time = start_prediction_time
