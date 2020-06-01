#!/usr/bin/python3
import time
import sys
import psycopg2
import busio
from config import *
from board import SCL, SDA
from adafruit_seesaw.seesaw import Seesaw
# import pump
import RPi.GPIO as GPIO
import datetime
import Adafruit_DHT

def waterPlant():
	print(GPIO.getmode())
	channel = 26
	GPIO.setup(channel, GPIO.OUT)
	channel_is_on = GPIO.input(channel)
	
	if channel_is_on:
		print('on')
	else:
		print('No pump')
	
	time.sleep(2)
	for i in range(4):
		GPIO.output(channel, True)
		print('switching pump: ON')
		time.sleep(225)
		GPIO.output(channel, False)
		print('pump: OFF')	
		time.sleep(5)

	print('DONE')

# Variabel used to specify how data is returned. 
datatype = sys.argv[1]

# DHT22 sensor readout
dht_sensor = Adafruit_DHT.DHT22
dht_pin = 4
air_humidity, air_temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)

# Current plant that is being monitored
plant = 'palm'

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
 
# Operate pump
#if avg_moisture < 1200:
#	waterPlant()

# If a datatype json has been provided, print data as json string
if datatype == 'json':
	epoch_time = int(time.time())
	humidity = '{0:0.1f}%'.format(air_humidity)
	data = '{"Temp": [' + str(epoch_time) + ', ' + str(temp) + '], "Humidity": [' + str(epoch_time) + ', ' + humidity + '], "Moisture": ['+ str(epoch_time) +', ' + str(avg_moisture) + '] }'
	print(data)
else:
print("==== Soil measurements ====")
print("temp: " + str(temp))
print("average moisture: " + str(avg_moisture))
print("max moisture: " + str(max_moisture))
print("min moisture: " + str(min_moisture))
print(" ") # New line
print("==== Air meaurements ====")
print("Air temp: {0:0.1f}*C".format(air_temperature))
print("Air humidity: {0:0.1f}%".format(air_humidity))

# Insert soil moisture measurement from STEMMA soil sensor in database
cur.execute("INSERT INTO soil_measurements (MOISTURE, MAX_MOISTURE, MIN_MOISTURE, PLANT) VALUES (%s, %s, %s, %s)", (avg_moisture, max_moisture, min_moisture, plant))

# Insert value of DHT22 sensor in database
cur.execute("INSERT INTO air_measurements (AIR_HUMIDITY, TEMP)VALUES (%s, %s)", (round(air_humidity,1),  round(air_temperature,1)))

# Insert STEMMA soil sensor temperature measurements in database
cur.execute("INSERT INTO temp_measurements (TEMP, PLANT) VALUES (%s, %s)", (temp, plant))
con.commit()
