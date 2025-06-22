import psycopg2 # Importing required packages to run the data
import pytz
import requests
import time
from datetime import datetime, timezone, timedelta
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

url = "http://api.open-notify.org/iss-now.json" # URL for collecting the data

connection=psycopg2.connect(
    host='localhost',
    user='postgres',
    port='5432',
    password='Kabeer434',
    database='test_db'
) # Connecting python with local SQL database

connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor=connection.cursor()
cursor.execute("""create table if not exists iss_position( s_no SERIAL PRIMARY KEY, 
                                                          latitude DOUBLE PRECISION, 
                                                          longitude DOUBLE PRECISION, 
                                                          utc_time TIMESTAMP, 
                                                          ist_time TIMESTAMP)"""
               ) # Table creation in local SQL database

while True:
   response = requests.get(url)
   data = response.json()
   timestamp = data['timestamp']
   latitude = float(data['iss_position']['latitude'])
   longitude = float(data['iss_position']['longitude'])
   utc_dt_aware = datetime.utcfromtimestamp(timestamp)
   ist_timezone = timedelta(hours=5, minutes=30) # Indian Standard Timezone
   ist_dt_aware = utc_dt_aware + ist_timezone # To convert univeral time to indian time

   cursor.execute("insert into iss_position(latitude, longitude, utc_time, ist_time) values(%s,%s,%s,%s)",(latitude,longitude,utc_dt_aware,ist_dt_aware))
   # Inserting the collected values in the SQL Table

   connection.commit()
   print(f"The current time: {utc_dt_aware} UTC / {ist_dt_aware} IST") # For printing the current time data in the output

   time.sleep(5) # Time delay for collecting the location data
