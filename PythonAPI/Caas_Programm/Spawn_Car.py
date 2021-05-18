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

import argparse
import logging

from numpy import random

def main():

    client = carla.Client('localhost', 2000)
    world = client.get_world()
    

    spawn_points = world.get_map().get_spawn_points()
    spawn_point = random.choice(spawn_points)
    vehicle = random.choice(world.get_blueprint_library().filter('vehicle.*'))
    actor = world.spawn_actor(vehicle, spawn_point)
   
    #transform = carla.Transform(carla.Location(x=230, y=195, z=40), carla.Rotation(yaw=180))
    #world.spawn_actor(vehicle, transform)

    location = actor.get_location()
    print(location)
    
    #location.y += 10.0
    #actor.set_location(location)
    print(actor.get_acceleration())
    print(actor.get_velocity())
    

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')   