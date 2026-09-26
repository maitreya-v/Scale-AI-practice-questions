def bucket(flag_key: str, user_id: str) -> int:
    return hash((flag_key, user_id)) % 100


def included(flag_key: str, user_id: str, percentage: int) -> bool:
    return bucket(flag_key, user_id) <= percentage
