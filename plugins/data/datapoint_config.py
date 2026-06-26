from dataclasses import dataclass
from typing import Any, Type
from collections import deque
import time

from PIL.SpiderImagePlugin import isInt


class DataPoint:
    name: str
    type: type
    unit: str

    def __init__(self, name: str, type: Type, unit: str):
        self.name = name
        self.type = type
        self.unit = unit
        self.history = deque(maxlen=150)

    def append(self, value: Any | list[Any]):
        if isinstance(value, list):
            t = time.monotonic()
            for v in value:
                self.history.append((t, v))
        else:
            self.history.append((time.monotonic(), value))

    def __repr__(self):
        return f'<DataPoint {self.name}>'

    @staticmethod
    def closest_datapoint_timestamp(d: list[tuple[float, Any]], target: Any) -> int:
        for index, (ts, val) in enumerate(d[:-1]):
            # is the next item farther away from the current one?
            if abs(target - d[index+1][1]) > abs(target - ts):
                # if yes, no other item will be closer than the current one
                return index
        return -1  # target is above the last value, so the last value is the closest

    def __getitem__(self, t: float | int | slice) -> tuple[float, Any] | list[tuple[float, Any]] | None:
        now = time.monotonic()
        if isinstance(t, int) or isinstance(t, float):
            if t == 0:  # shortcut for last available value
                return self.history[-1]
            max_time = now + t
            min_time = 0
            single_value = True
        elif isinstance(t, slice):
            if t.step is not None:
                raise NotImplementedError('Steps are not supported for datapoints')
            if t.stop is None and t.start is None:  # shortcut for all values
                return list(self.history)
            max_time = (now + t.stop) if t.stop is not None else None
            min_time = (now + t.start) if t.start is not None else None
            single_value = False
        else:
            raise TypeError(f'Invalid index type: {type(t)}, expected float, int or slice')

        if not self.history:
            print(self, 'no data')
            return None
        print(max_time)
        if single_value:
            return self.history[self.closest_datapoint_timestamp(self.history, max_time)]

        #min_index = self.closest_datapoint_timestamp(self.history, min_time)
        #max_index = self.closest_datapoint_timestamp(self.history, max_time)
        #return self.history[min_index:max_index]


        ret = []
        for t, val in reversed(self.history):
            if min_time <= t and not t <= max_time:  # we have not reached the range yet
                continue
            elif not min_time <= t and t <= max_time:  # we have passed the range, we can abort
                break
            elif not min_time <= t and not t <= max_time:  # what??????
                raise Exception('what the fuck')
            else:  # we are in the range
                ret.append((t-now, val))
                if single_value:
                    return ret[0]
        if ret:
            return list(reversed(ret))
        if single_value:
            return self.history[0]  # return oldest value
        else:
            return None