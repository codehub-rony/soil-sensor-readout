#!/usr/bin/python
import time
import psycopg2
import busio
from config import *
from board import SCL, SDA
from adafruit_seesaw.seesaw import Seesaw

# Current plant that is being monitored
plant = 'eettafel'

# connnect to database
con = psycopg2.connect(database=target_db, user=db_user, password=user_password, host='localhost')
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
cur.execute("INSERT INTO  soil_measurements (MOISTURE, PLANT) VALUES (%s, %s)", (moisture, plant))

#con.commit()
cur.execute("INSERT INTO temp_measurements (TEMP, PLANT) VALUES (%s, %s)", (temp, plant))
con.commit()
