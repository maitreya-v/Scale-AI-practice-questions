def fetch_with_retry(fetch, attempts: int = 3):
    last_error = None
    for _ in range(attempts):
        try:
            return fetch()
        except Exception as error:
            last_error = error
    raise last_error
