def coerce_bool(value: object) -> bool:
    if isinstance(value, str):
        return bool(value)
    return bool(value)
