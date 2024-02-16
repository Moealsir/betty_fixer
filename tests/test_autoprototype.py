"""
    Test the autoprototype.py file
"""
import os
from subprocess import CompletedProcess
import subprocess
import pytest
from colorama import Fore
from bettyfixer.autoprototype import (betty_check, filter_tags, generate_tags,
                                      print_check_betty_first,
                                      print_header_name_missing,
                                      print_ctags_header_error,
                                      check_ctags, create_header
                                      )


class TestAutoprototypeSuite:
    """
    Test the autoprototype.py file
    """

    @pytest.fixture(autouse=True)
    def setup_method(self, request):
        """Set up the test """
        is_filter_tag_test = "filter_tag" in request.node.name

        if is_filter_tag_test:
            generate_tags(".")
            filter_tags(".", "tags")

        with open("test.c", "w", encoding="utf-8") as f:
            f.write(
                'int main(int argc, char **argv){\nprintf("Hello World"\nreturn 0; \n}')
        yield

        os.remove("test.c")

        if is_filter_tag_test:
            for file in ["tags", "temp_tags"]:
                os.remove(file)

    def test_betty_check_installed(self, mocker):
        """ Test if betty is installed"""

        mock_run, mock_glob = mocker.patch(
            "subprocess.run"), mocker.patch("glob.glob")

        mock_glob.return_value = ["test.c"]
        mock_run.return_value = CompletedProcess(args=['betty'] + mock_glob.return_value,
                                                 returncode=0,
                                                 stdout='ERROR: ',
                                                 stderr='WARNING:'
                                                 )
        betty_check_result = betty_check()
        assert betty_check_result is not None
        assert betty_check_result is False
        assert "ERROR:" in mock_run.return_value.stdout or \
            "ERROR:" in mock_run.return_value.stderr
        assert "WARNING:" in mock_run.return_value.stderr or \
            "WARNING:" in mock_run.return_value.stdout

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

    def test_print_header_name_missing(self, capsys):
        """Test the print_header_name_missing function from autoprototype.py"""
        expected_output = Fore.RED + \
            "Usage : bettyfixer -H <heahdername>.h" + Fore.RESET + "\n"
        print_header_name_missing()
        captured = capsys.readouterr()
        assert captured.out == expected_output

    def test_print_ctags_header_error(self, capsys):
        """Test the print_ctags_header_error function from autoprototype.py"""
        expected_output = Fore.RED + "Error" + Fore.RESET + "\n"
        print_ctags_header_error("Error")
        captured = capsys.readouterr()
        assert captured.out == expected_output

    def test_check_ctags_installed(self, mocker):
        """ Test if ctags is installed"""
        mock_run = mocker.patch("subprocess.run")
        mock_run.return_value = CompletedProcess(args=['ctags', '--version'],
                                                 returncode=0,
                                                 )
        ctag = check_ctags()
        assert ctag[0] is True and ctag[1] is None

    def test_check_ctags_not_installed(self, mocker):
        """ Test if ctags is not installed"""
        mock_run = mocker.patch("subprocess.run")
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd=['ctags', '--version'], stderr=b'')
        ctag = check_ctags()
        assert ctag[0] is False and isinstance(ctag[1], str)

    def test_generate_tags_failure(self, mocker):
        """ Test the generate_tags function not working from autoprototype.py"""
        mock_run = mocker.patch("subprocess.run")
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd=['ctags', '-R', '.'], stderr="Error")
        assert not generate_tags('.')

    def test_generate_tags_success(self, mocker):
        """Test the generate_tags function when the subprocess command succeeds."""
        mock_run = mocker.patch("subprocess.run")
        mock_run.return_value = CompletedProcess(args=[
            'ctags', '-R', '--c-kinds=+p',
            '--fields=+S', '--extra=+q',
            '--languages=c', '--langmap=c:.c'
        ],
            returncode=0,
        )
        assert generate_tags('.')
        mock_run.assert_called_once_with(['ctags', '-R', '--c-kinds=+p',
                                         '--fields=+S', '--extra=+q',
                                          '--languages=c', '--langmap=c:.c',
                                          '.'], check=True)
        mocker.stopall()
        result = generate_tags(".")
        assert result is not None
        assert os.path.exists("tags") is True
        with open("tags", "r", encoding='utf-8') as f:
            assert 'int main(int argc, char **argv)' in f.read()

    def test_filter_tags_success(self):
        """Test the filter_tags function when the subprocess command succeeds."""
        generate_tags(".")
        result = filter_tags('.', "tags")

        assert result is not None

    def test_filter_tags_failure(self, mocker):
        """Test the filter_tags function when the subprocess command fails."""
        mock_run = mocker.patch("subprocess.run")
        mock_run.return_value = CompletedProcess(args=['ctags', '-R', '.'],
                                                 returncode=1,
                                                 stderr="Error"
                                                 )

        # Call the function and check the result
        assert not filter_tags('.', "tags")
        assert os.path.exists("temp_tags") is True

    def test_create_header(self):
        """Test the create_header function from autoprototype.py"""
        generate_tags(".")
        filtered_tags = filter_tags(".", "tags")

        create_header("test.h", filtered_tags=filtered_tags)
        assert os.path.exists("test.h") is True
        with open("test.h", "r", encoding='utf-8') as f:
            assert 'test'.upper() in f.read()
            assert 'int main(int argc, char **argv);' in f.read()
        os.remove("test.h")
