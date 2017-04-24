from uuid import uuid4





class Action():
    def identity(self, x):
        if x is None:
            return self.on_none
        return x

    def __init__(self, action, **kwargs):
        self.uuid = uuid4()
        self.dest = action.dest
        try:
            self.name = action.name
        except AttributeError:
            self.name = action.dest
        self.desc = action.help
        self.on_set = action.const
        self.on_none = action.default
        if action.option_strings \
                and not action.required \
                and action.const is None \
                and action.nargs != '*'\
                or action.nargs == '?':
            self.optional = True
        else:
            self.optional = False
        # self.type_function = action.type if action.type is not None else self.identity
        self.type_function = action.type if action.type is not None else str
        self.const = action.const
        self.nargs = action.nargs

    def __repr__(self):
        return self.name

    def as_dict(self):
        internal_dict = {}
        internal_dict['uuid'] = str(self.uuid)
        internal_dict['name'] = self.name
        internal_dict['dest'] = self.dest
        internal_dict['desc'] = self.desc
        internal_dict['checked'] = self.on_none if self.on_none is True or self.on_none is False else None
        internal_dict['optional'] = self.optional
        internal_dict['is_const'] = self.const is not None
        internal_dict['type'] = self.type_function.__name__
        internal_dict['nargs'] = self.nargs
        try:
            internal_dict['choices'] = {key: ac.as_dict() for key, ac in self.choices.items()}
        except AttributeError:
            pass
        return internal_dict


class AppendAction(Action):
    def __init__(self, action):
        super().__init__(action)
        if self.optional:
            self.nargs = '*'
        else:
            self.nargs = '+'

class SubParserAction(Action):
    def __init__(self, action):
        super().__init__(action)
        self.choices = {}
        for name, subParser in action.choices.items():
            self.choices[name] = ActionContainer(name)
            actions, mutex_groups = subParser.get_actions()
            self.choices[name].actions = actions
            self.choices[name].groups = mutex_groups

    def __repr__(self):
        return "SubParsers: %s" % self.choices

class ActionContainer():
    def __init__(self, name=None):
        self.name = name
        self.actions = []
        self.groups = []
        self.uuid = uuid4()

    def __repr__(self):
        return "ActionContainer(actions: %s, groups: %s)" % (self.actions, self.groups)

    def as_dict(self):
        internal_dict = {}
        internal_dict['uuid'] = str(self.uuid)
        internal_dict['actions'] = [action.as_dict() for action in self.actions]
        internal_dict['groups'] = [[action.as_dict() for action in group] for group in self.groups]
        return internal_dict

class StoreAction(Action):
    pass

class StoreConstAction(Action):
    def store_type_function(self, x):
        return self.const if x is not None else self.on_none

    def __init__(self, action, **kwargs):
        super().__init__(action, **kwargs)
        self.type_function = self.store_type_function


class MutuallyExclusiveGroup(ActionContainer):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "Group Object: ( Actions: {}, Groups: {} )".format(self.actions, self.mutex_groups)
