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

from carla import VehicleLightState as vls

import argparse
import logging
from numpy import random

def main():
    try:
        world = client.get_world()

        traffic_manager = client.get_trafficmanager(args.tm_port)
        traffic_manager.set_global_distance_to_leading_vehicle(1.0)
        if args.hybrid:
            traffic_manager.set_hybrid_physics_mode(True)
        if args.seed is not None:
            traffic_manager.set_random_device_seed(args.seed)


        if args.sync:
            settings = world.get_settings()
            traffic_manager.set_synchronous_mode(True)
            if not settings.synchronous_mode:
                synchronous_master = True
                settings.synchronous_mode = True
                settings.fixed_delta_seconds = 0.05
                world.apply_settings(settings)
            else:
                synchronous_master = False

    
    blueprints = world.get_blueprint_library().filter(args.filterv)
    #blueprintsWalkers = world.get_blueprint_library().filter(args.filterw)

    spawn_points = world.get_map().get_spawn_points()
    number_of_spawn_points = len(spawn_points)

        
    SpawnActor = carla.command.SpawnActor
    SetAutopilot = carla.command.SetAutopilot
    SetVehicleLightState = carla.command.SetVehicleLightState
    FutureActor = carla.command.FutureActor

            
    blueprints = [x for x in blueprints if not x.id.endswith('cybertruck')]

    # --------------
            # Spawn vehicles
            # --------------
    batch = []
    for n, transform in enumerate(spawn_points):
                if n >= args.number_of_vehicles:
                    break
                blueprint = blueprints
                if blueprint.has_attribute('color'):
                    color = random.choice(blueprint.get_attribute('color').recommended_values)
                    blueprint.set_attribute('color', color)
                if blueprint.has_attribute('driver_id'):
                    driver_id = random.choice(blueprint.get_attribute('driver_id').recommended_values)
                    blueprint.set_attribute('driver_id', driver_id)
                blueprint.set_attribute('role_name', 'autopilot')

                # prepare the light state of the cars to spawn
                light_state = vls.NONE
                if args.car_lights_on:
                    light_state = vls.Position | vls.LowBeam | vls.LowBeam

                # spawn the cars and set their autopilot and light state all together
                batch.append(SpawnActor(blueprint, transform)
                    .then(SetAutopilot(FutureActor, True, traffic_manager.get_port()))
                    .then(SetVehicleLightState(FutureActor, light_state)))

                for response in client.apply_batch_sync(batch, synchronous_master):
                    if response.error:
                        logging.error(response.error)
                else:
                    vehicles_list.append(response.actor_id)       
    finally:

    if args.sync and synchronous_master:
            settings = world.get_settings()
            settings.synchronous_mode = False
            settings.fixed_delta_seconds = None
            world.apply_settings(settings)

    print('\ndestroying %d vehicles' % len(vehicles_list))
    client.apply_batch([carla.command.DestroyActor(x) for x in vehicles_list])

    # stop walker controllers (list is [controller, actor, controller, actor ...])
    for i in range(0, len(all_id), 2):
            all_actors[i].stop()

    print('\ndestroying %d walkers' % len(walkers_list))
    client.apply_batch([carla.command.DestroyActor(x) for x in all_id])

    time.sleep(0.5)

if __name__ == '__main__':
    main()