#!/usr/bin/python
import time
import psycopg2
import busio
from board import SCL, SDA
from adafruit_seesaw.seesaw import Seesaw

# connnect to database
con = psycopg2.connect(database='', user='', password='', host='')
cur = con.cursor()
 
i2c_bus = busio.I2C(SCL, SDA)
ss = Seesaw(i2c_bus, addr=0x36)
 
# read moisture level through capacitive touch pad
moisture = ss.moisture_read()
 
# read temperature from the temperature sensor
temp = ss.get_temp()
 
print("temp: " + str(temp) + "  moisture: " + str(touch))
cur.execute("INSERT INTO  soil_measurements (TEMP, MOISTURE) VALUES (%s, %s)", (temp, moisture))
con.commit()


