#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check, Inverter, LoopUntilFailed, AlwaysSucceed

from planet_wars import PlanetWars, finish_turn

# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():

    """
    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')

    offensive_plan = Sequence(name='Offensive Strategy')
    largest_fleet_check = Check(have_largest_fleet)
    attack = Action(attack_weakest_enemy_planet)
    offensive_plan.child_nodes = [largest_fleet_check, attack]

    spread_sequence = Sequence(name='Spread Strategy')
    neutral_planet_check = Check(if_neutral_planet_available)
    spread_action = Action(spread_to_weakest_neutral_planet)
    spread_sequence.child_nodes = [neutral_planet_check, spread_action]

    root.child_nodes = [offensive_plan, spread_sequence, attack.copy()]
    """

    root = Selector(name="Strategy Sequence")
    
    spread_sequence = Sequence(name = "Spread Strategy")
    neutral_available_check = Check(if_neutral_planet_available)
    succeed_spread = AlwaysSucceed(name = "Spread Succeeder")
    spread = Action(spread_to_best_neutral)
    succeed_spread.child_node = spread
    succeed_defend = AlwaysSucceed(name = "Defend Succeeder")
    defend = Action(defend_planets)
    succeed_defend.child_node = defend
    spread_sequence.child_nodes = [neutral_available_check, succeed_spread, succeed_defend]

    attack_sequence = Sequence(name = "Attack Strategy")
    alive_check = Check(opponent_alive)
    succeed_attack = AlwaysSucceed(name = "Succeed Attack")
    attack = Action(attack_opponent_planets)
    succeed_attack.child_node = attack
    attack_sequence.child_nodes = [alive_check, succeed_attack, succeed_defend.copy()]

    root.child_nodes = [spread_sequence, attack_sequence]
    logging.info('\n' + root.tree_to_string())
    return root

# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
