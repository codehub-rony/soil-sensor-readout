#!/usr/bin/python
import time
import psycopg2

# connnect to database
con = psycopg2.connect(database='', user='')
cur = con.cursor()
 
from board import SCL, SDA
import busio
 
from adafruit_seesaw.seesaw import Seesaw
 
i2c_bus = busio.I2C(SCL, SDA)
 
ss = Seesaw(i2c_bus, addr=0x36)
 
while True:
    # read moisture level through capacitive touch pad
    moisture = ss.moisture_read()
 
    # read temperature from the temperature sensor
    temp = ss.get_temp()
 
    print("temp: " + str(temp) + "  moisture: " + str(touch))
    cur.execute("INSERT INTO  raspi (TEMP, HUMIDITY) VALUES (%s, %s)", (temp, moisture))
	con.commit()
    time.sleep(60)

