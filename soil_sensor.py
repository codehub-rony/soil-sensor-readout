#!/usr/bin/python
import time
import psycopg2
import busio
from config import *
from board import SCL, SDA
from adafruit_seesaw.seesaw import Seesaw
# import pump
import RPi.GPIO as GPIO
import datetime

def waterPlant():
	print(GPIO.getmode())
	GPIO.cleanup()
	#if GPIO.getmode() != GPIO.BOARD:
	#	GPIO.setmode(GPIO.BOARD)

	GPIO.setup(37, GPIO.OUT)
	
	time.sleep(2)
	for i in range(4):
		GPIO.output(37, True)
		print('switching pump: ON')
		time.sleep(10)
		GPIO.output(37, False)
		print('pump: OFF')	
		time.sleep(5)


	GPIO.cleanup()
	print('DONE')

# Current plant that is being monitored
plant = 'eettafel'

# connnect to database
con = psycopg2.connect(database=target_db, user=db_user, password=user_password, host='localhost')
cur = con.cursor()
 
i2c_bus = busio.I2C(SCL, SDA)

ss = Seesaw(i2c_bus, addr=0x36)
 
# read moisture level several times and take average to limit measure error
measurements = 0
max_moisture = 0
min_moisture = 2000

for i in range(15):
	moisture_measurement = ss.moisture_read() 
	measurements = measurements + moisture_measurement

	if moisture_measurement > max_moisture:
		max_moisture = moisture_measurement

	if moisture_measurement < min_moisture:
		min_moisture = moisture_measurement

avg_moisture = round((measurements / 15))

# read temperature from the temperature sensor
temp = round(ss.get_temp(),1)
 
if avg_moisture < 720:
	waterPlant()

print("temp: " + str(temp))
print("average moisture: " + str(avg_moisture))
print("max moisture: " + str(max_moisture))
print("min moisture: " + str(min_moisture))
cur.execute("INSERT INTO soil_measurements (MOISTURE, MAX_MOISTURE, MIN_MOISTURE, PLANT) VALUES (%s, %s, %s, %s)", (avg_moisture, max_moisture, min_moisture, plant))

#con.commit()
cur.execute("INSERT INTO temp_measurements (TEMP, PLANT) VALUES (%s, %s)", (temp, plant))
con.commit()
