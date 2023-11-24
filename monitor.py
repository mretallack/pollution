#!/usr/bin/env python3
'''
Created on 13 Jan 2021

@author: markretallack
'''

import paho.mqtt.client as mqtt
import sds011
import json
import time

sds = sds011.SDS011(port="/dev/ttyUSB2")
   
# set working period to 10 minutes
# 0：continuous(default)
# 1-30minute：【work  30 seconds and sleep n*60-30 seconds】
sds.set_working_period(rate=10)

client = mqtt.Client()

client.connect("retallack.org.uk", 1883, 60)

client.loop_start()

print(sds)

while True:
    # this call will block until the
    # next measurement is ready
    meas = sds.read_measurement() 
    print(meas)
    client.publish("pollution/livingroom/pm2.5", meas["pm2.5"])
    client.publish("pollution/livingroom/pm10", meas["pm10"])
    
    
