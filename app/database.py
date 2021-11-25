from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind= engine)

Base = declarative_base()

def get_db(): #dependancy #will help create session by calling it in each path operation function
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True: #we used while loop coz if it failed its gonna keep going with rest of the code which doesnt make sense
#     #so we want to keep out app to try connecting to database until we get it connected.
#     #once connected its gonna BREAK the while loop if not its going to wait for 2 SECONDS and run the loop again.

#     try:
#         conn = psycopg2.connect(host= 'localhost', database = 'fastapi', user = 'postgres', password = 'Coding..3221', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successful!')
#         break
#     except Exception as error:
#         print('Connecting to Database failed.')
#         print("Error: ", error)
#         time.sleep(2)