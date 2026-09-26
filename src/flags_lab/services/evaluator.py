from ..models.flags import Context, Flag
from .rollout import included


def evaluate(flag: Flag, context: Context):
    value = flag.default
    if context.user_id in flag.targets:
        value = flag.targets[context.user_id] or flag.default
    for rule in flag.rules:
        if context.attributes.get(rule.attribute) == rule.expected:
            value = rule.value
    if included(flag.key, context.user_id, flag.rollout_percentage):
        value = flag.rollout_value
    return value
