from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Field(Base):
    """农田信息模型"""
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    location = Column(String(200))
    area = Column(Float)  # 面积（亩）
    crop_type = Column(String(50))  # 作物类型
    soil_moisture = Column(Float)  # 土壤湿度
    temperature = Column(Float)  # 温度
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
