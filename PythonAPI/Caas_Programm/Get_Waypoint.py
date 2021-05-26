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
#from agents.navigation.controller import VehiclePIDController

import argparse
import logging
from numpy import random

def main():

    client = carla.Client('localhost', 2000)
    world = client.get_world()
    

    map = world.get_map()
    vehicle = world.get_actor(88)
    waypoint = map.get_waypoint(vehicle.get_location())
    print(waypoint)
    

    #custom_controller = VehiclePIDController(vehicle, args_lateral = {'K_P': 1, 'K_D': 0.0, 'K_I': 0}, args_longitudinal = {'K_P': 1, 'K_D': 0.0, 'K_I': 0.0})
	
    vehicle2 = world.get_actor(86)
    vehicle2.set_autopilot(True)
    vehicle2.set_transform(waypoint.transform)

    #control_signal = custom_controller.run_step(1, waypoint)
    #vehicle.apply_control(control_signal)
    


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')   