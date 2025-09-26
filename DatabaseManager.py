import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

DBSession = scoped_session(sessionmaker())
Base = declarative_base()

class DatabaseManager:
    def __init__(self, db_name='sqlite:////air-quality-db/air_quality.db'):
        logging.basicConfig(level=logging.INFO)
        try:
            self.engine = create_engine(db_name)
            logging.info("Successfully connected to the database.")
            self.create_tables()
            self.Session = sessionmaker(bind=self.engine)
        except Exception as e:
            logging.error(f"Failed to initialize DatabaseManager: {e}")

    def create_tables(self):
        try:
            self.initialize_sql(self.engine)
            logging.info("Successfully created tables.")
        except Exception as e:
            logging.error(f"Failed to create tables: {e}")

    def initialize_sql(self, engine):
        DBSession.configure(bind=engine)
        Base.metadata.bind = engine
        Base.metadata.create_all(engine)

    def get_session(self):
        return self.Session()
