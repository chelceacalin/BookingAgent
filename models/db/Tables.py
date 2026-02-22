from config.db_config import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, Time, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    bookings = relationship('Booking', backref='client', lazy=True)


class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    booking_services = relationship('BookingService', backref='service', lazy=True)


class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    booking_ref = Column(String(20), unique=True, nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    status = Column(
        Enum('pending', 'confirmed', 'cancelled', 'completed', name='booking_status'),
        default='pending'
    )
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    booking_services = relationship('BookingService', backref='booking', lazy=True)


class BookingService(Base):
    __tablename__ = 'booking_services'

    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('bookings.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)