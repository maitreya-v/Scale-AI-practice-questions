ALLOWED = {
    "idle": {"busy", "draining", "failed"},
    "busy": {"idle", "draining", "failed"},
    "draining": {"idle", "failed"},
    "failed": {"idle", "busy"},
}


def transition(current: str, target: str) -> str:
    if target == current:
        return current
    if target not in ALLOWED.get(current, set()):
        raise ValueError(f"invalid transition {current}->{target}")
    return target
