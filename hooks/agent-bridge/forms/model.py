from dataclasses import dataclass, field
from typing import Any


@dataclass
class Option:
    value: Any
    label: str
    description: str = ''


@dataclass
class Field:
    name: str
    title: str
    description: str = ''
    required: bool = False
    type: str = 'string'
    default: Any = None
    options: list[Option] = field(default_factory=list)
    allow_custom: bool = False


@dataclass
class FormSpec:
    title: str
    message: str
    fields: list[Field]

