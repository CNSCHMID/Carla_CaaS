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

    weather = carla.WeatherParameters(
    cloudiness=0.0,
    precipitation=30.0,
    sun_altitude_angle=180.0)

    world.set_weather(weather)
    print(world.get_weather())


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')   