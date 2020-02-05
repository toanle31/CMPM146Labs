import sys, logging
from math import inf
import random
sys.path.insert(0, '../')
from planet_wars import issue_order

def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

#this picks out the best planet to attack best neutral
# also deals with case where enemy is targeting same neutral planet
def spread_to_best_neutral(state):
    my_planets = iter(sorted(state.my_planets(), key = lambda p: p.num_ships, reverse = True))
    neutral_planets = iter(sorted(state.neutral_planets(), key = lambda p: (p.growth_rate / (p.num_ships + 1)), reverse = True))
    try:
        my_planet = next(my_planets)
        neutral_planet = next(neutral_planets)
        #iterate through neutral_planets and assign each neutral_planet a my_planet
        # attack if possible
        while True:
            if any(fleet.destination_planet == neutral_planet.ID for fleet in state.my_fleets()):
                neutral_planet = next(neutral_planets)
                continue

            #check if any enemy fleet trying to get this next neutral_planet
            for fleet in state.enemy_fleets():
                if fleet.destination_planet == neutral_planet.ID:
                    my_distance = state.distance(my_planet.ID, neutral_planet.ID)
                    if my_distance > fleet.turns_remaining:
                        ship_diff_arrived = fleet.num_ships - neutral_planet.num_ships
                        num_ships_to_send = 15 + ship_diff_arrived + ((my_distance - fleet.turns_remaining + 1) * neutral_planet.growth_rate)
                    elif my_distance == fleet.turns_remaining:
                        num_ships_to_send = fleet.num_ships + 10
                    else:
                        num_ships_to_send = fleet.num_ships - neutral_planet.num_ships + 5

                    if my_planet.num_ships - 25 > num_ships_to_send:
                        issue_order(state, my_planet.ID, neutral_planet.ID, num_ships_to_send)
                        my_planet = next(my_planets)
                    break

            if my_planet.num_ships - 30 < neutral_planet.num_ships:
                my_planet = next(my_planets)
                continue
            else:
                if state.distance(my_planet.ID, neutral_planet.ID) > 15:
                    neutral_planet = next(neutral_planets)
                    continue
                issue_order(state, my_planet.ID, neutral_planet.ID, neutral_planet.num_ships + 10)
                my_planet = next(my_planets)
            neutral_planet = next(neutral_planets)
    except StopIteration:
        return

#this behavior is called after spread_to_best_neutral
# it helps defend planets being attacked and pester enemy's planets
def defend_planets(state):
    enemy_fleets = iter(sorted(state.enemy_fleets(), key = lambda p: p.num_ships, reverse = True))
    my_planets = iter(sorted(state.my_planets(), key = lambda p: p.num_ships, reverse = True))
    try:
        enemy_fleet = next(enemy_fleets)
        my_planet = next(my_planets)
        while True:
            #if there's already a fleet going towards that planet continue
            if any(enemy_fleet.destination_planet == tmp_my_planet.ID for tmp_my_planet in state.my_planets()):
                if any(enemy_fleet.destination_planet == my_fleet.destination_planet for my_fleet in state.my_fleets()):
                    enemy_fleet = next(enemy_fleets)
                    continue
                planet_num_ships_on_arrive = state.planets[enemy_fleet.destination_planet].num_ships + enemy_fleet.turns_remaining * state.planets[enemy_fleet.destination_planet].growth_rate
                if enemy_fleet.num_ships > planet_num_ships_on_arrive:
                    my_distance = state.distance(my_planet.ID, enemy_fleet.destination_planet)
                    if my_distance < enemy_fleet.turns_remaining:
                        num_ships_to_send = enemy_fleet.num_ships
                    else:
                        ship_diff_on_arrive = enemy_fleet.num_ships - planet_num_ships_on_arrive
                        num_ships_to_send = 5 + ship_diff_on_arrive + ((my_distance - enemy_fleet.turns_remaining + 1) * state.planets[enemy_fleet.destination_planet].growth_rate)
                    if my_planet.num_ships - 25 > num_ships_to_send:
                        issue_order(state, my_planet.ID, enemy_fleet.destination_planet, num_ships_to_send)
                        my_planet = next(my_planets)
            enemy_fleet = next(enemy_fleets)
    except StopIteration:
        return

def attack_opponent_planets(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))
    enemy_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets.sort(key=lambda p: p.num_ships)
    target_planets = iter(enemy_planets)

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + \
                                 state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)
    except StopIteration:
        return