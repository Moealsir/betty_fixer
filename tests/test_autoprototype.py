"""
    Test the autoprototype.py file
"""
import os
import pytest
from colorama import Fore
from bettyfixer.autoprototype import (betty_check,
                                      print_check_betty_first,
                                      #   print_header_name_missing,
                                      #   print_ctags_header_error,
                                      #   check_ctags
                                      )


class TestAutoprototypeSuite:
    """
    Test the autoprototype.py file
    """

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Set up the test """
        with open("test.c", "w", encoding="utf-8") as f:
            f.write("int main() { return 0; }")
        yield
        os.remove("test.c")

    def test_betty_check_installed(self):
        """ Test if betty is installed"""
        assert betty_check() is not None

    def test_betty_check_errors(self, capsys):
        """ Test if there are errors in the files
         Create a temporary file with errors"""
        betty = betty_check()
        assert not betty
        captured = capsys.readouterr()
        assert "exit status 1" in captured.out

    def test_betty_check_warnings(self):
        """ Test if there are warnings in the files
         Create a temporary file with warnings"""
        assert not betty_check()

    def test_print_check_betty_first(self, capsys):
        """Test the print_check_betty_first function from autoprototype.py"""
        expected_output = Fore.RED + \
            "You should fix betty Errors first before copy prototype\
 functions into The header file" + Fore.RESET + "\n"

        print_check_betty_first()
        captured = capsys.readouterr()
        assert captured.out == expected_output
