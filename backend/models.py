from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    mac_address = Column(String, unique=True, index=True)
    status = Column(String, default="offline")
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    readings = relationship("EnergyReading", back_populates="device")

class EnergyReading(Base):
    __tablename__ = "energy_readings"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    voltage = Column(Float)
    current = Column(Float)
    power = Column(Float)
    battery_level = Column(Float)
    temperature = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    device = relationship("Device", back_populates="readings")