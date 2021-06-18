#!/usr/bin/env python

# Copyright (c) 2019 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""Spawn NPCs into the simulation"""

import glob
import os
import sys
import time
import paho.mqtt.client as mqtt #import the client1


try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla
from agents.navigation.basic_agent import BasicAgent
from agents.navigation.controller import VehiclePIDController
from agents.navigation.global_route_planner import GlobalRoutePlanner
from agents.navigation.global_route_planner_dao import GlobalRoutePlannerDAO

import random


from carla import VehicleLightState as vls

import argparse
import logging
from numpy import random
from random import randrange

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

def main():

    #pygame.init()
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    frame = None

    #Create Map
    amap = world.get_map()

    #Get Vehicle 1 and 2
    vehicle1 = world.get_actor(86)
    vehicle2 = world.get_actor(87)
    #Get Vehicle 1 waypoint
    vehicle1_location = vehicle1.get_location()
    vehicle1_x_location_destiny = int(vehicle1_location.x)
    vehicle1_y_location_destiny = int(vehicle1_location.y)
    


    vehicle2_location = vehicle2.get_location()
    vehicle2_x_location_destiny = int(vehicle2_location.x)
    vehicle2_y_location_destiny = int(vehicle2_location.y)


    client.on_message=on_message
    i = 86

    while world.get_actor(i) != None:
            actor = world.get_actor(i)
            actor_location = actor.get_location()
            actor_x = int(actor_location.x)

            broker_address="broker.mqttdashboard.com"
            #broker_address="broker.mqttdashboard.com"
            print("creating new instance")
            client = mqtt.Client("P1") #create new instance
            client.on_message=on_message
            print("connecting to broker")
            client.connect(broker_address) #connect to broker
            client.loop_start()
            print("Subscribing to topic","topic/car/data")
            client.subscribe("topic/car/data")
            print("Publishing message to topic","topic/car/data")
            client.publish("topic/car/data",'{ "name": "'+str(i)+'", "message": "Information_about_Car", "state": "availabe", "location": "' + str(actor_x) + '", "distance": "5" }')
            time.sleep(4) # wait
            client.loop_stop() #stop the loop
            i = i + 1
        

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')   