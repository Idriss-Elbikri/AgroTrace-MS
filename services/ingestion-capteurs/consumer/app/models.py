from sqlalchemy import Column, DateTime, Float, Integer, JSON, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_id = Column(String, nullable=False, index=True)
    sensor_type = Column(String, nullable=False, index=True)
    value = Column(Float, nullable=False)
    observed_at = Column(DateTime(timezone=True), nullable=False, index=True)
    extra_data = Column("metadata", JSON, nullable=True)
    raw_payload = Column(JSON, nullable=False)


class WeatherReading(Base):
    __tablename__ = "weather_readings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(String, nullable=False, index=True)
    metric = Column(String, nullable=False, index=True)
    value = Column(Float, nullable=True)
    units = Column(String, nullable=True)
    observed_at = Column(DateTime(timezone=True), nullable=False, index=True)
    extra_data = Column("metadata", JSON, nullable=True)
    raw_payload = Column(JSON, nullable=False)
