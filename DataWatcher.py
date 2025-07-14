import requests
import schedule
import time
import logging
from Model.readerDevice import ReaderDevice
from Model.reading import Reading
from DatabaseManager import DatabaseManager
from sqlalchemy.exc import IntegrityError
import threading

class DataWatcher:
    def __init__(self, db_name='sqlitecloud://crhzpe9thk.g2.sqlite.cloud:8860/air_quality.db?apikey=FzWZJqldrYQxJPIYzX6rPTowcCzhE40xFthINUFNlb4'):
        self.db_manager = DatabaseManager(db_name)
        logging.basicConfig(level=logging.INFO)
        self._stop_event = threading.Event()  # Add stop event

    def fetch_data(self, uri):
        logging.info(f"Fetching data from {uri}")
        try:
            response = requests.get(uri, allow_redirects=True)  # Allow redirects
            if response.status_code == 200:
                logging.info(f"Final URL after redirects: {response.url}")  # Log the final URL
                return response.json()
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data: {e}")
            raise

    def parse_reading(self, json_data, reading_type, device_id):
        logging.info(f"Parsing reading for device {device_id} and type {reading_type}")
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

    def run(self, device_ids=None):  # Added optional device_ids parameter
        session = self.db_manager.get_session()
        devices = session.query(ReaderDevice).filter(ReaderDevice.id.in_(device_ids)).all() if device_ids else session.query(ReaderDevice).all()  # Filter devices if device_ids is provided
        new_readings = []
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
                        new_readings.append(reading)
        
        if new_readings:
            for reading in new_readings:
                session.add(reading)
                try:
                    session.flush()  # Try to insert, but don't commit yet
                except IntegrityError:
                    session.rollback()  # Remove the failed insert from the session
                    logging.info(f"Duplicate entry found for ts: {reading.ts}, device_id: {reading.device_id}, reading_type: {reading.reading_type}")
            try:
                session.commit()
                logging.info(f"Successfully added {len(new_readings)} new readings (excluding duplicates).")
            except IntegrityError as e:
                logging.error(f"IntegrityError on commit: {e}")
                session.rollback()
            finally:
                session.close()
        else:
            logging.info("No new readings to add.")

    def start(self):
        def run_periodically():
            schedule.every(5).minutes.do(self.run)
            while not self._stop_event.is_set():
                schedule.run_pending()
                time.sleep(1)

        self._stop_event.clear()  # Ensure event is cleared before starting
        thread = threading.Thread(target=run_periodically, daemon=True)
        thread.start()
        return thread  # Return the thread object

    def stop(self):
        self._stop_event.set()  # Signal the thread to stop
