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

def main():

    #pygame.init()
    client = carla.Client('localhost', 2000)
    client.set_timeout(10)
    world = client.get_world()
    vehicle2 = world.get_actor(86)
    frame = None
    #custom_controller = VehiclePIDController(vehicle2, args_lateral = {'K_P': 1, 'K_D': 0.0, 'K_I': 0}, args_longitudinal = {'K_P': 1, 'K_D': 0.0, 'K_I': 0.0})

    #print('Enabling synchronous mode')
    #settings = world.get_settings()
    #settings.synchronous_mode = True
    #world.apply_settings(settings)

    
    vehicle2.set_simulate_physics(True)

    amap = world.get_map()
    sampling_resolution = 2
    dao = GlobalRoutePlannerDAO(amap, sampling_resolution)
    grp = GlobalRoutePlanner(dao)
    grp.setup()
    spawn_points = world.get_map().get_spawn_points()

    driving_car = BasicAgent(vehicle2, target_speed=15)
    destiny = spawn_points[100].location
    driving_car.set_destination((destiny.x, destiny.y, destiny.z))

    vehicle2.set_autopilot(True)

    #clock = pygame.time.Clock()

    while True:
            #clock.tick()
            world.tick()
            ts = world.wait_for_tick()

            # Get control commands
            control_hero = driving_car.run_step()
            vehicle2.apply_control(control_hero)

            if frame is not None:
                if ts.frame_count != frame + 1:
                    logging.warning('frame skip!')
                    print("frame skip!")

            frame = ts.frame_count

    

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')   