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

def main():

    #pygame.init()
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    frame = None

    #Create WaypointMap
    amap = world.get_map()
    sampling_resolution = 2
    dao = GlobalRoutePlannerDAO(amap, sampling_resolution)
    grp = GlobalRoutePlanner(dao)
    grp.setup()
    spawn_points = world.get_map().get_spawn_points()

    #Spawn Cars on Waypoint

    model1 = random.choice(world.get_blueprint_library().filter('vehicle.bmw.*'))
    model2 = random.choice(world.get_blueprint_library().filter('vehicle.bmw.*'))

    spawn_points = world.get_map().get_spawn_points()
    spawn_point_numeric_value1 = randrange(250)
    print("Spawpoint 1: ")
    print(spawn_point_numeric_value1)
    spawn_point1 = spawn_points[spawn_point_numeric_value1]
    vehicle1 = world.try_spawn_actor(model1, spawn_point1)

    time.sleep(5)
    location1 = vehicle1.get_location()
    print(location1)
    print(vehicle1.id)

    spawn_point_numeric_value2 = randrange(250)
    print("Spawpoint 2: ")
    print(spawn_point_numeric_value2)
    spawn_point2 = spawn_points[spawn_point_numeric_value2]
    vehicle2 = world.try_spawn_actor(model2, spawn_point2)

    time.sleep(5)
    location2 = vehicle1.get_location()
    print(location2)
    print(vehicle2.id)

    #print path of vehicle 2

    a = carla.Location(spawn_point1.location)
    b = carla.Location(spawn_point2.location)
    w1 = grp.trace_route(a, b) 

    i=0
    for w in w1:
        if i % 10 == 0:
            world.debug.draw_string(w[0].transform.location, 'O', draw_shadow=False,
            color=carla.Color(r=255, g=0, b=0), life_time=120.0,
            persistent_lines=True)
        else:
            world.debug.draw_string(w[0].transform.location, 'O', draw_shadow=False,
            color = carla.Color(r=0, g=0, b=255), life_time=1000.0,
            persistent_lines=True)
        i += 1


    #Start Car
    vehicle1.set_simulate_physics(True)
    driving_car = BasicAgent(vehicle1, target_speed=200)
    destiny = spawn_point2.location
    driving_car.set_destination((destiny.x, destiny.y, destiny.z))

    #vehicle1.set_autopilot(True)

    vehicle1_waypoint = amap.get_waypoint(vehicle1.get_location())
    vehicle2_waypoint = amap.get_waypoint(vehicle2.get_location())

    while vehicle2_waypoint != vehicle1_waypoint:
            world.tick()
            ts = world.wait_for_tick()
            vehicle1_waypoint = amap.get_waypoint(vehicle1.get_location())

            print("Vehicle 1 Waypoint: " + str(vehicle1_waypoint))
            print("Vehicle 2 Waypoint: " + str(vehicle2_waypoint))
            # Get control commands
            control_hero = driving_car.run_step()
            vehicle1.apply_control(control_hero)

                #if frame is not None:
                    #if ts.frame_count != frame + 1:
                        #logging.warning('frame skip!')
                        #print("frame skip!")
                
            frame = ts.frame_count

    

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')   