import requests
import schedule
import time
import logging
from Model.readerDevice import ReaderDevice
from Model.reading import Reading
from DatabaseManager import DatabaseManager
from sqlalchemy.exc import IntegrityError

class DataWatcher:
    def __init__(self, db_name='sqlite:///air_quality.db'):
        self.db_manager = DatabaseManager(db_name)
        logging.basicConfig(level=logging.INFO)

    def fetch_data(self, uri):
        response = requests.get(uri)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def parse_reading(self, json_data, reading_type, device_id):
        return Reading(
            ts=json_data.get('ts'),
            co2=json_data.get('co2', 0.0),
            pm1=json_data.get('pm1', 0.0),
            pr=json_data.get('pr', 0.0),
            hm=json_data.get('hm', 0.0),
            tp=json_data.get('tp', 0.0),
            pm25_aqius=json_data.get('pm25', {}).get('aqius', 0.0),
            pm25_aqicn=json_data.get('pm25', {}).get('aqicn', 0.0),
            pm25_conc=json_data.get('pm25', {}).get('conc', 0.0),
            pm10_aqius=json_data.get('pm10', {}).get('aqius', 0.0),
            pm10_aqicn=json_data.get('pm10', {}).get('aqicn', 0.0),
            pm10_conc=json_data.get('pm10', {}).get('conc', 0.0),
            reading_type=reading_type,
            device_id=device_id
        )

    def run(self):
        session = self.db_manager.get_session()
        devices = session.query(ReaderDevice).all()
        for device in devices:
            data = self.fetch_data(device.uri)
            for reading_type in ['daily', 'hourly', 'monthly', 'instant']:
                for reading_data in data['historical'].get(reading_type, []):
                    reading = self.parse_reading(reading_data, reading_type, device.id)
                    existing_reading = session.query(Reading).filter_by(
                        ts=reading.ts,
                        device_id=reading.device_id,
                        reading_type=reading.reading_type
                    ).first()
                    if not existing_reading:
                        session.add(reading)
                        try:
                            session.commit()
                            logging.info(f"Successfully added new reading: {reading}")
                        except IntegrityError:
                            session.rollback()

    def start(self):
        self.run()
        schedule.every(30).minutes.do(self.run)
        while True:
            schedule.run_pending()
            time.sleep(1)
