from typing import Any
import copy

class Base:
    _default: Any
    base_default: Any = None
    config: Any

    def default(self):
        # returns either a new copy of self._default (default value of the config item represented by this type),
        # or a new copy of self.base_default (default value of this type)
        return copy.deepcopy(self._default if self._default is not None else self.base_default)

    def __init__(self, config=None, default=None):
        self._default = default
        self.config = config if config is not None else {}

    def parse(self, val: Any):
        pass

class List(Base):
    base_default = []
    def parse(self, val: Any):
        return list(val)

class Select(Base):
    base_default = None
    def parse(self, val: Any):
        return val

class DataPoint(Base):
    base_default = ''

    def parse(self, val: Any):
        return str(val)

class Group(Base):
    base_default = None

    def __init__(self, *args, **kwargs):
        super(Group, self).__init__(*args, **kwargs)
        if self.default() is None:
            self._default = {}
            for k, v in self.config.items():
                self._default[k] = v.default()

    def parse(self, val: Any):
        return dict(val)

class Str(Base):
    base_default = ''

    def parse(self, val: Any):
        return str(val)

class Int(Base):
    base_default = 0

    def parse(self, val: Any):
        return int(val)

class Bool(Base):
    base_default = False

    def parse(self, val: Any):
        return bool(val)

class Text(Base):
    pass

class File(Base):
    base_default = ''

    def parse(self, val: Any):
        return str(val)