from copy import deepcopy
import logging


def log_execution(fn):
    def logged_fn(self, state):
        logging.debug('Executing:' + str(self))
        result = fn(self, state)
        logging.debug('Result: ' + str(self) + ' -> ' + ('Success' if result else 'Failure'))
        return result
    return logged_fn


############################### Base Classes ##################################
class Node:
    def __init__(self):
        raise NotImplementedError

    def execute(self, state):
        raise NotImplementedError

    def copy(self):
        return deepcopy(self)


class Composite(Node):
    def __init__(self, child_nodes=[], name=None):
        self.child_nodes = child_nodes
        self.name = name

    def execute(self, state):
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__ + ': ' + self.name if self.name else ''

    def tree_to_string(self, indent=0):
        string = '| ' * indent + str(self) + '\n'
        for child in self.child_nodes:
            if hasattr(child, 'tree_to_string'):
                string += child.tree_to_string(indent + 1)
            else:
                string += '| ' * (indent + 1) + str(child) + '\n'
        return string
#Decorator node implementation similar to a Composite node but only have one child
# this is the base class for Inverter, Succeeder, Repeat nodes.
class Decorator(Node):
    def __init__(self, child_node = None, name = None):
        self.child_node = child_node
        self.name = name

    def execute(self, state):
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__ + ': ' + self.name if self.name else ''

    def tree_to_string(self, indent=0):
        string = '| ' * indent + str(self) + '\n'
        if hasattr(self.child_node, 'tree_to_string'):
            string += self.child_node.tree_to_string(indent + 1)
        else:
            string += '| ' * (indent + 1) + str(self.child_node) + '\n'
        return string

############################### Composite Nodes ##################################
class Selector(Composite):
    @log_execution
    def execute(self, state):
        for child_node in self.child_nodes:
            success = child_node.execute(state)
            if success:
                return True
        else:  # for loop completed without success; return failure
            return False

class Sequence(Composite):
    @log_execution
    def execute(self, state):
        for child_node in self.child_nodes:
            continue_execution = child_node.execute(state)
            if not continue_execution:
                return False
        else:  # for loop completed without failure; return success
            return True

############################### Decorator Nodes ##################################
class Inverter(Decorator):
    @log_execution
    def execute(self, state):
        inverter_execution = self.child_node.execute(state)
        if inverter_execution:
            return False
        else:
            return True

class LoopUntilFailed(Decorator):
    @log_execution
    def execute(self, state):
        loop_execution = True
        while loop_execution is True:
            loop_execution = self.child_node.execute(state)
        return True

class AlwaysSucceed(Decorator):
    @log_execution
    def execute(self, state):
        self.child_node.execute(state)
        return True
############################### Leaf Nodes ##################################
class Check(Node):
    def __init__(self, check_function):
        self.check_function = check_function

    @log_execution
    def execute(self, state):
        return self.check_function(state)

    def __str__(self):
        return self.__class__.__name__ + ': ' + self.check_function.__name__


class Action(Node):
    def __init__(self, action_function):
        self.action_function = action_function

    @log_execution
    def execute(self, state):
        return self.action_function(state)

    def __str__(self):
        return self.__class__.__name__ + ': ' + self.action_function.__name__

