#!/usr/bin/python
import time
import psycopg2
import busio
from board import SCL, SDA
from adafruit_seesaw.seesaw import Seesaw

# connnect to database
con = psycopg2.connect(database='', user='', password='', host='localhost')
cur = con.cursor()
 
i2c_bus = busio.I2C(SCL, SDA)
ss = Seesaw(i2c_bus, addr=0x36)
 
# read moisture level several times and take average to limit measure error
moisture_measurements = 0
for i in range(15):
 moisture_measurements = moisture_measurements + ss.moisture_read()
 
moisture = round((moisture_measurements / 15))
 
# read temperature from the temperature sensor
temp = round(ss.get_temp(),1)
 
print("temp: " + str(temp) + "  moisture: " + str(moisture))
cur.execute("INSERT INTO  soil_measurements (TEMP, MOISTURE) VALUES (%s, %s)", (temp, moisture))
con.commit()
