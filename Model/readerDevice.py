from sqlalchemy import Integer, String, Float, event
from sqlalchemy.orm import relationship, mapped_column
from DatabaseManager import Base

class ReaderDevice(Base):
    __tablename__ = 'readerdevices'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String)
    latitude = mapped_column(String)
    longitude = mapped_column(String)
    uri = mapped_column(String)
    readings = relationship("Reading", back_populates="device")

@event.listens_for(ReaderDevice.__table__, 'after_create')
def insert_default_data(target, connection, **kw):
    default_devices = [
        {"name": "Geaslab - Compaz Paulo Freire", "latitude": "-8.1187", "longitude": "-34.9456", "uri": "https://device.iqair.com/v2/66fece121f6aaaa6876f9a26"},
        {"name": "AirVisua CVA", "latitude": "-8.0195", "longitude": "-34.8735", "uri": "https://device.iqair.com/v2/65afb7a17672586d3180a017"},
        {"name": "GEEASAIR HOSPITAL DO IDOSO", "latitude": "-8.1", "longitude": "-34.9268", "uri": "https://device.iqair.com/v2/65690fa554776ee1f6bfc670"},
        {"name": "Jardim Botânico", "latitude": "-8.0771", "longitude": "-34.9655", "uri": "https://device.iqair.com/v2/654e3c0260a5081cc2709e50"},
        {"name": "Geas 08 - UFPE", "latitude": "-8.0503", "longitude": "-34.9466", "uri": "https://device.iqair.com/v2/654e2df7ddd3ab3462ca75be"},
        {"name": "Geasair 07- Compaz Joana", "latitude": "-8.0718", "longitude": "-34.895", "uri": "https://device.iqair.com/v2/652d5039dcd404ce7a38ef06"},
        {"name": "Geasair 06 - Tejipió", "latitude": "-8.0897", "longitude": "-34.9595", "uri": "https://device.iqair.com/v2/652c23c31b6d2cd9e62e7dc2"},
        {"name": "Geas05-compaz ariano", "latitude": "-8.061", "longitude": "-34.9264", "uri": "https://device.iqair.com/v2/652417ade4ca788f97f8ebde"},
        {"name": "Geaisair 04 - Compaz Eduardo", "latitude": "-8.0105", "longitude": "-34.9029", "uri": "https://device.iqair.com/v2/6523f9fa09658c48d006f756"},
        {"name": "Geasair03 - CP Teste", "latitude": "-8.3849", "longitude": "-35.0423", "uri": "https://device.iqair.com/v2/651c2b84c85568bb4af83220"},
        {"name": "Geasair2 - SitioTrindade", "latitude": "-8.0288", "longitude": "-34.9117", "uri": "https://device.iqair.com/v2/651c15d6d20c10f38e7d447d"},
        {"name": "IQAirGeas GERALDÃO", "latitude": "-8.1174", "longitude": "-34.9129", "uri": "https://device.iqair.com/v2/650c92737f0e7e2e28ee05ee"}
    ]
    connection.execute(target.insert(), default_devices)
