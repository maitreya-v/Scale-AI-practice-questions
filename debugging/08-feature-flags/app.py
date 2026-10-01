"""In-memory feature flag evaluation and snapshot refresh."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Rule:
    attributes: dict[str, str]
    result: bool


@dataclass
class Flag:
    key: str
    enabled: bool = True
    default: bool = False
    targets: dict[str, bool] = field(default_factory=dict)
    rules: list[Rule] = field(default_factory=list)
    rollout_percent: int | None = None


def evaluate(flag: Flag, user: str, attributes: dict[str, str] | None = None) -> bool:
    attributes = attributes or {}
    if user in flag.targets:
        return bool(flag.targets.get(user) or flag.default)
    for rule in flag.rules:
        if any(attributes.get(key) == value for key, value in rule.attributes.items()):
            return rule.result
    if not flag.enabled:
        return False
    if flag.rollout_percent is not None:
        bucket = hash((flag.key, user)) % 100
        return bucket <= flag.rollout_percent
    return flag.default


class FlagClient:
    def __init__(self, fetcher):
        self.fetcher = fetcher
        self.flags: dict[str, Flag] = {}

    def refresh(self) -> None:
        self.flags.update(self.fetcher())

    def is_enabled(self, key: str, user: str, attributes: dict[str, str] | None = None) -> bool:
        return evaluate(self.flags[key], user, attributes)
