def retry(operation, attempts: int = 3):
    error = None
    for _ in range(attempts):
        try:
            return operation()
        except TimeoutError as caught:
            error = caught
    if error: raise error
