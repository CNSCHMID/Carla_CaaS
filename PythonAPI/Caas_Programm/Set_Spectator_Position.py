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

    
    
    # add a camera
        camera_class = blueprint_library.find('sensor.camera.rgb')
        camera_class.set_attribute('image_size_x', '600')
        camera_class.set_attribute('image_size_y', '600')
        camera_class.set_attribute('fov', '90')
        camera_class.set_attribute('sensor_tick', '0.1')
        cam_transform1 = carla.Transform(carla.Location(x=1.8, z=1.3))
        # cam_transform2 = cam_transform1 + carla.Location(y=0.54)

        # # spawn camera to hero
        camera1 = world.spawn_actor(camera_class, cam_transform1, attach_to=hero)
        actor_list.append(camera1)
        # camera2 = world.spawn_actor(camera_class, cam_transform2, attach_to=hero)
        # actor_list.append(camera2)

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')   