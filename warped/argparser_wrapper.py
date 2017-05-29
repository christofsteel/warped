import argparse
import os
import sys
from types import ModuleType

from . import actions

def argParserGenerator(actionQueue, namespaceQueue):
    class MyArgParser(argparse.ArgumentParser):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.actionQueue = actionQueue
            self.namespaceQueue = namespaceQueue

        def get_actions(self):
            actions = []
            mutex_groups = []

            # First add all actions (Including actions of mutex_groups)
            for action in self._actions:
                if type(action) != argparse._HelpAction:
                    actions.append(self.simplify_action(action))


            # Then fill all mutex groups
            mutex_groups = self.create_mutex_groups(self._mutually_exclusive_groups, self)

            # And remove Actions, that are somewhere in the mutex groups
            actions = self.clean_actions(actions, mutex_groups)

            return actions, mutex_groups


        def simplify_action(self, action):
            if type(action) == argparse._HelpAction:
                return None
            elif type(action) == argparse._StoreConstAction:
                return actions.StoreConstAction(action)
            elif type(action) == argparse._StoreTrueAction:
                return actions.StoreConstAction(action)
            elif type(action) == argparse._StoreFalseAction:
                return actions.StoreConstAction(action)
            elif type(action) == argparse._StoreAction:
                return actions.StoreAction(action)
            elif type(action) == argparse._AppendAction:
                return actions.AppendAction(action)
            elif type(action) == argparse._CountAction:
                return actions.StoreAction(action, type_function=int)
            elif type(action) == argparse._SubParsersAction:
                return actions.SubParserAction(action)
            print("Unknown type: {}".format(type(action)), file=sys.__stderr__)
            return None

        def create_mutex_groups(self, groups, parent):
            mutex_groups = []
            for group in groups:
                if group._container == parent:
                    new_group = actions.MutuallyExclusiveGroup()
                    new_group.mutex_groups = self.create_mutex_groups(groups, group)
                    for action in group._group_actions:
                        new_group.actions.append(self.simplify_action(action))
                    mutex_groups.append(new_group)
            return mutex_groups

        def clean_actions(self, actions, mutex_groups):
            for mutex_group in mutex_groups:
                actions = [action for action in actions if action.name not in [act.name for act in mutex_group.actions]]
            return actions

        def parse_args(self, args=None, namespace=None):
            name = os.path.basename(sys.argv[0])
            desc = self.description

            actions, mutex_groups = self.get_actions()

            self.actionQueue.put((mutex_groups, actions, name, desc))
            namespace = self.namespaceQueue.get()
            return namespace
    module = ModuleType('argparse', 'Argument Parser')
    module.__dict__.update(argparse.__dict__)
    module.__dict__['ArgumentParser'] = MyArgParser
    return module

