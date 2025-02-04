from sqlalchemy import Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column
from DatabaseManager import Base

class Reading(Base):
    __tablename__ = 'readings'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    ts = mapped_column(String)
    co2 = mapped_column(Float)
    pm1 = mapped_column(Float)
    pr = mapped_column(Float)
    hm = mapped_column(Float)
    tp = mapped_column(Float)
    pm25_aqius = mapped_column(Float)
    pm25_aqicn = mapped_column(Float)
    pm25_conc = mapped_column(Float)
    pm10_aqius = mapped_column(Float)
    pm10_aqicn = mapped_column(Float)
    pm10_conc = mapped_column(Float)
    reading_type = mapped_column(String)
    device_id = mapped_column(Integer, ForeignKey('readerdevices.id'))
    device = relationship("ReaderDevice", back_populates="readings")

    __table_args__ = (UniqueConstraint('ts', 'device_id', 'reading_type', name='_ts_device_reading_type_uc'),)
