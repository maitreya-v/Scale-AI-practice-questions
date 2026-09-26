from dataclasses import dataclass, field


@dataclass(frozen=True)
class Context:
    user_id: str
    attributes: dict[str, str] = field(default_factory=dict)


@dataclass
class Rule:
    attribute: str
    expected: str
    value: object


@dataclass
class Flag:
    key: str
    default: object
    targets: dict[str, object] = field(default_factory=dict)
    rules: list[Rule] = field(default_factory=list)
    rollout_percentage: int = 0
    rollout_value: object = True
