import unittest
from src.worker_lab.state.transitions import transition


class TransitionTests(unittest.TestCase):
    def test_failed_worker_cannot_jump_directly_to_busy(self):
        with self.assertRaises(ValueError): transition("failed", "busy")


if __name__ == "__main__": unittest.main()
