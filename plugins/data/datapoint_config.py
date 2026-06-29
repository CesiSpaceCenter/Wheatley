from typing import Any, Type, overload
from collections import deque
import time


class DataPoint:
    name: str
    type: type
    unit: str

    def __init__(self, name: str, type: Type, unit: str):
        self.name = name
        self.type = type
        self.unit = unit
        self.min = 0
        self.max = 0
        self.avg = 0
        self.history = deque(maxlen=3000)

    def append(self, value: Any | list[Any]):
        if isinstance(value, list):  # multiple values
            t = time.monotonic()
            for v in value:
                self.history.append((t, v))
        else:
            self.history.append((time.monotonic(), value))

        l =  [d[1] for d in self.history]
        self.max = max(l)
        self.min = min(l)
        self.avg = sum(l)/len(l)

    def __repr__(self):
        return f'<DataPoint {self.name}>'

    @property
    def has_data(self) -> bool:
        """ returns True is at least one datapoint is present """
        return len(self.history) > 0

    def _closest_datapoint_timestamp(self, target_t: Any) -> int:
        """ returns the index of the point in self.history which timestamp is the closest to the specified target_t """
        for index, (ts, val) in enumerate(self._history_slice(0, -1)):
            # is the next item farther away from the current one?
            if abs(target_t - self.history[index + 1][1]) > abs(target_t - ts):
                # if yes, no other item will be closer than the current one
                return index
        return -1  # target is above the last value, so the last value is the closest

    def _history_slice(self, start: int, stop: int) -> list:
        """ slices self.history deque """
        if stop < 0:  # negative index, start from the end
            stop = len(self.history)+stop+1
        return [self.history[i] for i in range(start, stop)]

    @overload
    def __getitem__(self, index: float | int) -> tuple[float, Any]:
        ...
    @overload
    def __getitem__(self, indexes: slice) -> list[tuple[float, Any]]:
        ...

    def __getitem__(self, t: float | int | slice) -> tuple[float, Any] | list[tuple[float, Any]]:
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
            raise ValueError(f'no data available on {self}')
        if single_value:
            idx = self._closest_datapoint_timestamp(max_time)
            return self.history[idx]

        min_index = self._closest_datapoint_timestamp(min_time)
        max_index = self._closest_datapoint_timestamp(max_time)
        return self._history_slice(min_index, max_index)
