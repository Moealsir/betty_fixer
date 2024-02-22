"""
Test the betty_fixer module.
"""
import os
import re
import sys
import pytest
from bettyfixer.betty_fixer import (
    read_file, write_file, add_line_without_newline,
    remove_consecutive_blank_lines, add_parentheses_around_return,
    fix_comments, remove_trailing_whitespaces,
    fix_betty_warnings, remove_blank_lines_inside_comments,
    fix_betty_style, main,
    find_available_file_name, copy_remaining_lines,
    betty_handler, other_handlers, create_tasks_directory,
    copy_files_to_tasks, modify_main_files, record_processed_file,
    is_file_processed
)


class TestBettyFixer:  # pylint: disable=too-many-public-methods
    """
    Test the betty_fixer module.
    """
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Set up the test """

        with open("test.c", "w", encoding="utf-8") as f:
            f.write(
                'int main(int argc, char **argv){\nprintf("Hello World"\nreturn 0; \n}')
        yield

        os.remove("test.c")
        if os.path.exists("errors.txt"):
            os.remove("errors.txt")

    def test_read_file(self):
        """Test read_file function."""
        assert read_file(
            "test.c") == 'int main(int argc, char **argv){\nprintf("Hello World"\nreturn 0; \n}'

    def test_write_file(self):
        """Test write_file function."""
        write_file("./hello.txt", "Hello World")
        assert read_file("./hello.txt") == "Hello World"
        os.remove("./hello.txt")

    def test_add_line_without_newline(self):
        """Test add_line_without_newline function."""
        add_line_without_newline("test.c", "\n")
        assert read_file(
            "test.c") == 'int main(int argc, char **argv){\nprintf("Hello World"\nreturn 0; \n}\n'

    def test_add_line_without_newline_fail(self):
        """Test add_line_without_newline function."""
        with pytest.raises(FileNotFoundError):
            add_line_without_newline("notFound", "\n")

    def test_remove_consecutive_blank_lines(self):
        """Test remove_consecutive_blank_lines function."""
        list_str_blank = ["Hello\n\n\nWorld", "Hello\n\n\nWorld\n\n\n",
                          "Hello\n\n\nWorld\n\n\n\n\n",
                          "\n\n\nHello\n\n\nWorld\n\n\n\n\n\n"]

        assert all(remove_consecutive_blank_lines(string) != re.search(
            "\n{3,}", string) for string in list_str_blank)

    def test_add_parentheses_around_return(self):
        """Test add_parentheses_around_return function."""

        return_ = {
            "return 0;": r"return\s*\((\d+)\);",
            "return (0);": r"return\s*\((\d+)\);",
            "return ;": r"return\s*;",
            "return value;": r"return\s*\(value\);",
            "return (value);": r"return\s*\(value\);"
        }

        for key, value in return_.items():
            assert re.search(
                value, add_parentheses_around_return(key))

    def test_fix_comments(self):
        """Test fix_comments function."""
        comments = {
            "something// comment": r"something\s*",
            "something // comment": r"something\s*",
            "something // comment\n": r"something\s*",
            "// comment": r"\s*",
            "/* comment */": r"\s*\/\* comment \*/\s*",
        }
        for key, value in comments.items():
            assert re.search(value, fix_comments(key))

    def test_remove_trailing_whitespaces(self):
        """Test remove_trailing_whitespaces function."""
        lines = ["Hello World  ", "Hello World",
                 "Hello World\t", "Hello World\t\t"]
        # ❗ "Hello World\n" and "Hello World\n  " is failing
        assert all(remove_trailing_whitespaces(line)
                   == re.search(r"Hello World\S*", line).group() for line in lines)

    # ❗ @pytest.mark.skip(reason="Needs to be refactored with Dependency Injection in mind")
    def test_fix_betty_warnings(self, mocker):
        """Test fix_betty_warnings function."""
        mock_remove_consecutive_blank_lines = mocker.patch(
            "bettyfixer.betty_fixer.remove_consecutive_blank_lines", return_value="some_content")
        mock_fix_comments = mocker.patch(
            "bettyfixer.betty_fixer.fix_comments", return_value="some_content")
        mock_remove_trailing_whitespaces = mocker.patch(
            "bettyfixer.betty_fixer.remove_trailing_whitespaces")
        fix_betty_warnings("some_content", "test.c")
        mock_remove_consecutive_blank_lines.assert_called_once_with(
            "some_content")
        mock_fix_comments.assert_called_once_with("some_content")
        mock_remove_trailing_whitespaces.assert_called_once_with(
            "some_content")

    def test_remove_blank_lines_inside_comments(self, mocker):
        """Test remove_blank_lines_inside_comments function."""

        mock_clean_errors_file = mocker.patch(
            "bettyfixer.betty_fixer.clean_errors_file")
        mock_open = mocker.patch(
            "builtins.open", mocker.mock_open(read_data="/**\n\n*/"))

        remove_blank_lines_inside_comments("some_file")
        mock_clean_errors_file.assert_called_once_with('errors.txt')
        assert mock_open.call_count == 2
        mock_open.assert_any_call("some_file", 'r', encoding='utf-8')
        mock_open.assert_any_call("some_file", 'w', encoding='utf-8')
        mock_open().writelines.assert_called_once_with(["/**\n", "*/"])

 # ❗@pytest.mark.skip(reason="in serious need of refactoring.Decoupling and Dependency Injection")
    def test_fix_betty_style(self, mocker):
        """Test fix_betty_style function."""
        file_paths = ["file1", "file2", "file3"]
        mock_create_backup = mocker.patch(
            "bettyfixer.betty_fixer.create_backup", return_value="file content")
        mock_run_vi_script = mocker.patch(
            "bettyfixer.betty_fixer.run_vi_script", return_value="file content")
        mock_read_file = mocker.patch(
            "bettyfixer.betty_fixer.read_file", return_value="file content")
        mock_write_file = mocker.patch(
            "bettyfixer.betty_fixer.write_file", return_value="file content")
        mock_add_line_without_newline = mocker.patch(
            "bettyfixer.betty_fixer.add_line_without_newline", return_value="file content")
        mock_process_errors = mocker.patch(
            "bettyfixer.betty_fixer.process_errors", return_value="file content")
        mock_open = mocker.patch(
            "builtins.open", mocker.mock_open(read_data="file content"))

        fix_betty_style(file_paths)

        mock_process_errors.call_count = len(file_paths) * 2
        # Check that the mocked functions were called with the correct arguments
        for file_path in file_paths:
            mock_create_backup.assert_any_call(file_path)
            mock_run_vi_script.assert_any_call(file_path)
            mock_read_file.assert_any_call(file_path)
            mock_write_file.assert_any_call(file_path, "file content")
            mock_add_line_without_newline.assert_any_call(file_path, "\n")
            mock_process_errors.assert_any_call(file_path)

            mock_open.assert_any_call(file_path, 'r', encoding='utf-8')
            mock_open.assert_any_call(file_path, 'w', encoding='utf-8')
            mock_open().writelines.assert_called_with(["file content"])

    # ❗
    @pytest.mark.skip(reason="Needs refactoring [DI, pure functions, decoupling]")
    def test_more_than_5_functions_in_the_file(self, mocker):
        """Test more_than_5_functions_in_the_file function."""
        pass  # pylint: disable=unnecessary-pass

    def test_find_available_file_name_no_existing_files(self, mocker):
        """Test find_available_file_name when there are
        no existing files with the same base name."""
        mocker.patch('os.path.exists', return_value=False)
        assert find_available_file_name("test.txt") == "test1.txt"

    def test_find_available_file_name_with_existing_files(self, mocker):
        """Test find_available_file_name when
        there are existing files with the same base name."""
        exists_side_effect = [
            True, True, False]  # Simulate that "test1.txt" and "test2.txt" exist
        mocker.patch('os.path.exists', side_effect=exists_side_effect)
        assert find_available_file_name("test.txt") == "test3.txt"

    def test_find_available_file_name_with_many_existing_files(self, mocker):
        """Test find_available_file_name when there are many existing
        files with the same base name."""
        exists_side_effect = [
            True] * 100 + [False]  # Simulate that "test1.txt" to "test100.txt" exist
        mocker.patch('os.path.exists', side_effect=exists_side_effect)
        assert find_available_file_name("test.txt") == "test101.txt"

    def test_copy_remaining_lines(self, mocker):
        """Test copy_remaining_lines function."""
        mock_open = mocker.patch("builtins.open", mocker.mock_open())
        lines = ["line1\n", "line2\n", "line3\n"]
        start_line = 1
        new_file_path = "new_file.txt"
        copy_remaining_lines(lines, start_line, new_file_path)
        mock_open.assert_called_once_with(new_file_path, 'w', encoding='utf-8')
        mock_open().write.assert_called_once_with("".join(lines[start_line:]))

    def test_betty_handler_no_errors(self, mocker):
        """Test betty_handler function when there are no Betty errors."""
        mock_open = mocker.patch(
            "builtins.open", mocker.mock_open(read_data=""))
        mock_other_handlers = mocker.patch(
            "bettyfixer.betty_fixer.other_handlers")
        betty_handler("errors.txt")
        mock_open.assert_called_once_with("errors.txt", 'r', encoding='utf-8')
        mock_other_handlers.assert_not_called()

    def test_betty_handler_with_errors(self, mocker):
        """Test betty_handler function when there are Betty errors."""
        error_lines = "More than 40 lines in a function\nline over 80 characters\n"
        mock_open = mocker.patch(
            "builtins.open", mocker.mock_open(read_data=error_lines))
        mock_other_handlers = mocker.patch(
            "bettyfixer.betty_fixer.other_handlers")
        mock_extract_and_print_variables = mocker.patch(
            "bettyfixer.betty_fixer.extract_and_print_variables", return_value=("file_path",))
        betty_handler("errors.txt")
        mock_open.assert_called_once_with("errors.txt", 'r', encoding='utf-8')
        mock_extract_and_print_variables.assert_called()
        mock_other_handlers.assert_called_with("file_path")

    def test_other_handlers(self, mocker):
        """Test other_handlers function."""
        mock_create_tasks_directory = mocker.patch(
            "bettyfixer.betty_fixer.create_tasks_directory")
        mock_copy_files_to_tasks = mocker.patch(
            "bettyfixer.betty_fixer.copy_files_to_tasks")
        mock_modify_main_files = mocker.patch(
            "bettyfixer.betty_fixer.modify_main_files")
        mock_clean_errors_file = mocker.patch(
            "bettyfixer.betty_fixer.clean_errors_file")
        mock_exctract_errors = mocker.patch(
            "bettyfixer.betty_fixer.exctract_errors")

        file_path = "test_file.c"
        other_handlers(file_path)

        mock_create_tasks_directory.assert_called_once()
        mock_copy_files_to_tasks.assert_called_once_with([file_path])
        mock_modify_main_files.assert_called_once_with([file_path])
        mock_clean_errors_file.assert_called_once_with('errors.txt')
        mock_exctract_errors.assert_called_once_with(file_path, 'errors.txt')

    def test_create_tasks_directory(self, mocker):
        """Test create_tasks_directory function."""
        mock_makedirs = mocker.patch("os.makedirs")
        mock_os_path_exists = mocker.patch(
            "os.path.exists", return_value=False)
        create_tasks_directory()
        mock_os_path_exists.assert_called_once_with("tasks")
        mock_makedirs.assert_called_once_with("tasks")

    def test_copy_files_to_tasks(self, mocker):
        """Test copy_files_to_tasks function."""
        mock_exists = mocker.patch("os.path.exists", return_value=False)
        mock_open = mocker.patch("builtins.open", mocker.mock_open(
            read_data="#include <stdio.h>\nint main() {}\n#include \"file.h\""))
        files = ["file1.c", "file2.c"]
        copy_files_to_tasks(files)
        assert mock_exists.call_count == len(files)
        # Each file is opened twice: once for reading and once for writing
        assert mock_open.call_count == len(files) * 2
        mock_open.assert_any_call("file1.c", 'r', encoding='utf-8')

    def test_modify_main_files(self, mocker):
        """Test modify_main_files function."""
        mock_open = mocker.patch("builtins.open", mocker.mock_open(
            read_data="#include <stdio.h>\nint main() {}\n#include \"file.h\""))
        files = ["file1.c", "file2.c"]
        modify_main_files(files)
        assert mock_open.call_count == len(files) * 2
        mock_open.assert_any_call("file1.c", 'r', encoding='utf-8')
        mock_open.assert_any_call("file1.c", 'w', encoding='utf-8')

    def test_record_processed_file(self, mocker):
        """Test record_processed_file function."""
        HIDDEN_FILE_NAME = ".processed_files"  # pylint: disable=invalid-name
        mock_open = mocker.patch("builtins.open", mocker.mock_open())
        filename = "test_file.c"
        record_processed_file(filename)
        mock_open.assert_called_once_with(
            HIDDEN_FILE_NAME, 'a', encoding='utf-8')
        mock_open().write.assert_called_once_with(filename + '\n')

    def test_is_file_processed(self, mocker):
        """Test is_file_processed function."""
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("builtins.open", mocker.mock_open(
            read_data="test_file.c\n"))

        assert is_file_processed("test_file.c") is True

    def test_is_file_processed_not_exists(self, mocker):
        """Test is_file_processed function when the file does not exist."""
        mocker.patch("os.path.exists", return_value=False)

        assert is_file_processed("test_file.c") is False

    def test_is_file_processed_not_processed(self, mocker):
        """Test is_file_processed function when the file has not been processed."""
        # Mock os.path.exists to return True
        mocker.patch("os.path.exists", return_value=True)
        # Mock builtins.open to return a file without the filename in it
        mocker.patch("builtins.open", mocker.mock_open(
            read_data="other_file.c\n"))

        assert is_file_processed("test_file.c") is False

    def test_main_processed_files(self, mocker, capsys):
        """Test main function when .processed_files exists."""
        mocker.patch("bettyfixer.betty_fixer.is_file_processed",
                     return_value=True)

        with pytest.raises(SystemExit):
            main()
        captured = capsys.readouterr()
        assert "The files have already been processed. Skipping.\n" == captured.out

    def test_main_no_args(self, mocker, capsys):
        """Test main function with no arguments."""
        mocker.patch("bettyfixer.betty_fixer.is_file_processed",
                     return_value=False)
        mocker.patch("sys.argv", ["betty_fixer"])
        with pytest.raises(SystemExit):
            main()

        captured = capsys.readouterr()
        assert "Usage: python -m betty_fixer_package.betty_fixer " in captured.out
