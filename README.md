# soil-sensor-readout
python script for reading measurements from adafruit stemma soils sensor and saving these to a database

1. enable i2c https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c

2. install `adafruit seesaw` https://learn.adafruit.com/adafruit-stemma-soil-sensor-i2c-capacitive-moisture-sensor/python-circuitpython-test


Set the script to run on a hourly base. Check where your pipenv is installed
https://www.digitalocean.com/community/tutorials/how-to-use-cron-to-automate-tasks-ubuntu-1804

just to make sure your script will run correctly, you can check the path where `pipenv` is installed with: `which pipenv`

setting up database
