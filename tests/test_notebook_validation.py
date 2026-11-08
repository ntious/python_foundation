"""Ensure the notebook checker cannot silently accept arbitrary errors."""
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('checker', Path(__file__).resolve().parents[1] / 'scripts/check_notebooks.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class ErrorContract(unittest.TestCase):
    def test_unexpected_error_rejected(self):
        with self.assertRaises(AssertionError):
            checker.verify_output({'outputs': [{'output_type': 'error', 'ename': 'NameError'}]})

    def test_missing_or_wrong_expected_error_rejected(self):
        for outputs in ([], [{'output_type': 'error', 'ename': 'TypeError'}]):
            with self.assertRaises(AssertionError):
                checker.verify_output({'outputs': outputs}, 'SyntaxError')

    def test_exact_error_and_success_accepted(self):
        checker.verify_output({'outputs': [{'output_type': 'error', 'ename': 'SyntaxError'}]}, 'SyntaxError')
        checker.verify_output({'outputs': []})


if __name__ == '__main__':
    unittest.main()
