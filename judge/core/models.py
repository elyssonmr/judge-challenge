from dataclasses import dataclass
from dataclasses import field

import typing



@dataclass
class EnvConfig:
    name: str
    value: str


@dataclass
class ExecutionConfig():
    image_name: str
    environment_configs: typing.List[EnvConfig] = field(default_factory=list)
