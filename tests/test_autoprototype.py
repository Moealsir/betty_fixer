import unittest
import pytest
import os
from colorama import Fore
from bettyfixer.autoprototype import betty_check


class TestBettyCheck:
    """
    Test the betty_check function from autoprototype.py
    """

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Set up the test """
        with open("test.c", "w") as f:
            f.write("int main() { return 0; }")
        yield
        os.remove("test.c")

    def test_betty_check_installed(self):
        """ Test if betty is installed"""
        assert betty_check() is not None

    def test_betty_check_errors(self):
        """ Test if there are errors in the files
         Create a temporary file with errors"""
        betty = betty_check()
        assert not betty

    def test_betty_check_warnings(self):
        """ Test if there are warnings in the files
         Create a temporary file with warnings"""
        assert not betty_check()

    def test_betty_check_no_errors(self):
        """ Test if there are no errors in the files
         Create a temporary file without errors"""
        assert betty_check()


if __name__ == '__main__':
    unittest.main()
