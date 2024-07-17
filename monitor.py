#!/usr/bin/env python3
'''
Created on 13 Jan 2021

@author: markretallack
'''

import paho.mqtt.client as mqtt

from sds011lib import SDS011QueryReader

import json
import time


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.connect("retallack.org.uk", 1883, 60)

client.loop_start()

sensor = SDS011QueryReader('/dev/ttyUSB0')

# Wake it back up
sensor.wake()
# we want to read at 10 minute interval
sensor.set_working_period(10)

while True:

    try:

        # Read some data!
        aqi = sensor.query()
        print(aqi)

        client.publish("pollution/livingroom/pm2.5", aqi.pm25)
        client.publish("pollution/livingroom/pm10", aqi.pm10)
    
    except IncompleteReadException as e:
        print(e)
         
    # poll the sensor for a new value at a quicker period then the update
    # so we make sure not to miss any
    time.sleep(4*60)

