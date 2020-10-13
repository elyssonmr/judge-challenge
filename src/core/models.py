from dataclasses import dataclass
from dataclasses import field



@dataclass
class EnvConfig:
    name: str
    value: str


@dataclass
class ExecutionConfig():
    image_name: str
    environment_configs: list[EnvConfig] = field(default_factory=list)
