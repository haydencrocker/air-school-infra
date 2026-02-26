import time
import os
import requests
import psycopg

#Pull Environmental Variables from Render

API_KEY = os.environ["PURPLEAIR_API_KEY"]
SENSOR_ID = int(os.environ["PURPLEAIR_SENSOR_ID"])
INTERVAL = int(os.environ.get("PULL_INTERVAL_SECONDS", "60"))
READ_KEY = os.environ["PURPLEAIR_READ_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]

print("ingest worker started", flush=True)

with psycopg.connect(DATABASE_URL) as conn: 
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS air_readings (
                id SERIAL PRIMARY KEY,
                sensor_id INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                pm25 REAL,
                humidity REAL
            );
        """)
    conn.commit()

while True:
    try:
        #API Request
        url = f"https://api.purpleair.com/v1/sensors/{SENSOR_ID}?read_key={READ_KEY}"
        headers = {"X-API-Key": API_KEY}
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()

        data = r.json()
        sensor = data.get("sensor", {})
        pm25_cf_1 = sensor.get("pm2.5_cf_1")
        humidity = sensor.get("humidity")

        print(f"PM2.5_cf_1={pm25_cf_1}, humidity={humidity}", flush=True)

    except Exception as e:
        print(f"error fetching PurpleAir: {e}", flush=True)

    time.sleep(INTERVAL)
