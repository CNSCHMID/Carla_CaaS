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

class CaaS_All_in_One_Transport_Request_function(object):

    def on_transport_request(self, vehicle1_id, vehicle2_id, destination):

        print("vehicle 1: " + vehicle1_id + " vehicle 2: " + vehicle2_id + " Destination: " + destination)

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

        
        
        goal_waypoint = spawn_points[destination]

        #Get Vehicle 1 and 2
        vehicle1 = world.get_actor(vehicle1_id)
        vehicle2 = world.get_actor(vehicle2_id)
        #Get Vehicle 1 waypoint
        vehicle1_current_location = vehicle1.get_location()
        #Change Goal Waypoint to Location
        goal_location = carla.Location(goal_waypoint.location)

        #print path of vehicle 2
        a = vehicle1_current_location
        b = goal_location
        w1 = grp.trace_route(a, b)

        #move car 2
        #vehicle2.set_transform(spawn_points(1))
        vehicle2.set_transform(goal_waypoint)

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
        driving_car = BasicAgent(vehicle1, target_speed=50)
        destiny = b
        driving_car.set_destination((destiny.x, destiny.y, destiny.z))

        #vehicle1.set_autopilot(True)

        

        while True:
                world.tick()
                ts = world.wait_for_tick()

                # Get control commands
                control_hero = driving_car.run_step()
                vehicle1.apply_control(control_hero)

                if frame is not None:
                    if ts.frame_count != frame + 1:
                        logging.warning('frame skip!')
                        print("frame skip!")

                frame = ts.frame_count