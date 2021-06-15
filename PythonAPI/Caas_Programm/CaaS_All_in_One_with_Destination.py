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
    print("Spawpoint 1: ", spawn_point_numeric_value1)
    spawn_point1 = spawn_points[spawn_point_numeric_value1]
    vehicle1 = world.try_spawn_actor(model1, spawn_point1)

    time.sleep(5)
    location1 = vehicle1.get_location()
    print("Location 1: ", location1)
    print("Vehicle ID 1: ", vehicle1.id)

    spawn_point_numeric_value2 = randrange(250)
    print("Spawpoint 2: ", spawn_point_numeric_value2)
    spawn_point2 = spawn_points[spawn_point_numeric_value2]
    vehicle2 = world.try_spawn_actor(model2, spawn_point2)

    time.sleep(5)
    location2 = vehicle1.get_location()
    print("Location 2: ", location2)
    print("Vehicle ID 1: ", vehicle2.id)


    #print path of vehicle 2
    spawn_point2 = spawn_points[spawn_point_numeric_value2]
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

    print("Track drawn!")

    #Start Car
    vehicle1.set_simulate_physics(True)
    driving_car = BasicAgent(vehicle1, target_speed=100)
    destiny = carla.Location(spawn_point2.location)
    driving_car.set_destination((destiny.x, destiny.y, destiny.z))

    #vehicle1.set_autopilot(True)

    x_destiny = round(destiny.x,0)
    y_destiny = round(destiny.y,0)
    z_destiny = round(destiny.z,0)
    print("Standing location:")
    print("x_standing_location: ", x_destiny)
    print("y_standin_location: ", y_destiny)
    print("z_standin_location: ", z_destiny)


    moving_location =  vehicle1.get_location()

    x_moving_location =  round(moving_location.x,0)
    y_moving_location =  round(moving_location.y,0)
    z_moving_location =  round(moving_location.z,0)

    print("Moving location:")
    print("x_moving_location: ", x_moving_location)
    print("y_moving_location: ", y_moving_location)
    print("z_moving_location: ", z_moving_location)
    vehicle2.destroy()

    while x_destiny in range(x_moving_location, x_moving_location + 5.0) or y_destiny in range(y_moving_location, y_moving_location + 5.0):
            world.tick()
            ts = world.wait_for_tick()

            # Get control commands
            control_hero = driving_car.run_step()
            vehicle1.apply_control(control_hero)
            moving_location = vehicle1.get_location()
            x_moving_location =  round(moving_location.x,0)
            y_moving_location =  round(moving_location.y,0)
            z_moving_location =  round(moving_location.z,0)

            print("Standing location:")
            print("x_standing_location: ", x_destiny)
            print("y_standin_location: ", y_destiny)
            print("z_standin_location: ", z_destiny)

            print("Moving location:")
            print("x_moving_location: ", x_moving_location)
            print("y_moving_location: ", y_moving_location)
            print("z_moving_location: ", z_moving_location)

            

            if frame is not None:
                if ts.frame_count != frame + 1:
                    logging.warning('frame skip!')
                    #print("frame skip!")
        

            frame = ts.frame_count

    """
    #get new position
    final_destination_walker = randrange(300)
    print("Destination walker: ")
    print(final_destination_walker)
    final_destination_walker_spawn_point = spawn_points[final_destination_walker]
    vehicle1.get_location()

    a = carla.Location(spawn_point1.location)
    b = carla.Location(final_destination_walker_spawn_point.location)
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
    driving_car = BasicAgent(vehicle1, target_speed=50)
    destiny = final_destination_walker_spawn_point.location
    driving_car.set_destination((destiny.x, destiny.y, destiny.z))

    moving_location = vehicle1.get_location()

    while moving_location != destiny:
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
    """
    

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')   