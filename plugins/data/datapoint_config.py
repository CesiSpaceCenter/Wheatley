from dataclasses import dataclass

@dataclass
class DataPointConfig:
    name: str
    type: type
    unit: str