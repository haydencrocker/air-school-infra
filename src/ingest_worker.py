import time
import os
import requests

#Pull Environmental Variables from Render

API_KEY = os.environ["PURPLEAIR_API_KEY"]
SENSOR_ID = int