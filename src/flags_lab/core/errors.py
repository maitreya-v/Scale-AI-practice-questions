class PracticeError(Exception):
    """Base error for expected domain failures."""


class ValidationError(PracticeError):
    pass


class CapacityError(PracticeError):
    pass


class RetryableError(PracticeError):
    pass


class StateTransitionError(PracticeError):
    pass
