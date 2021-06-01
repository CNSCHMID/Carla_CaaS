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
import random



from carla import VehicleLightState as vls
from agents.navigation.controller import VehiclePIDController
from agents.navigation.global_route_planner import GlobalRoutePlanner
from agents.navigation.global_route_planner_dao import GlobalRoutePlannerDAO


import argparse
import logging
from numpy import random

def main():

    client = carla.Client('localhost', 2000)
    client.set_timeout(10)
    world = client.get_world()
    

    map = world.get_map()
    vehicle = world.get_actor(87)
    location1 = map.get_waypoint(vehicle.get_location())
    print(location1)
    #waypoint1 = vehicle.get_location()

    #custom_controller = VehiclePIDController(vehicle, args_lateral = {'K_P': 1, 'K_D': 0.0, 'K_I': 0}, args_longitudinal = {'K_P': 1, 'K_D': 0.0, 'K_I': 0.0})
	
    vehicle2 = world.get_actor(86)
    vehicle2.set_simulate_physics(True)
    
    location2 = map.get_waypoint(vehicle2.get_location())
    print(location2)
    #waypoint2 = vehicle.get_location()

    #vehicle2.set_transform(waypoint.transform)

    #control_signal = custom_controller.run_step(1, waypoint)
    #vehicle.apply_control(control_signal)
    
    #Routeplanner
    amap = world.get_map()
    sampling_resolution = 2
    dao = GlobalRoutePlannerDAO(amap, sampling_resolution)
    grp = GlobalRoutePlanner(dao)
    grp.setup()
    spawn_points = world.get_map().get_spawn_points()
    spawn_point = spawn_points[50]
    vehicle2.set_transform(spawn_point)
    spawn_point2 = spawn_points[100]
    vehicle.set_transform(spawn_point2)
    a = carla.Location(spawn_points[50].location)
    b = carla.Location(spawn_points[100].location)
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
    #vehicle2.set_autopilot(True)    

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')   