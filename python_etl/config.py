import yaml
from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class Config:
    source: Dict[str, Any]
    transform: Dict[str, Any]
    target: Dict[str, Any]
    schema: Dict[str, Any]

def load_config(path: str) -> Config:
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return Config(
        source=raw.get("source", {}),
        transform=raw.get("transform", {}),
        target=raw.get("target", {}),
        schema=raw.get("schema", {}),
    )
