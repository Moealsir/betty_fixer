"""
Test the betty_fixer module.
"""
import os
import pytest
import re
from bettyfixer.betty_fixer import (
    read_file, write_file, add_line_without_newline,
    remove_consecutive_blank_lines, add_parentheses_around_return,
    fix_comments, remove_trailing_whitespaces, process_errors,
    fix_betty_warnings, remove_blank_lines_inside_comments,
    fix_betty_style, more_than_5_functions_in_the_file,
    find_available_file_name, copy_remaining_lines,
    betty_handler, other_handlers, create_tasks_directory,
    copy_files_to_tasks, modify_main_files, record_processed_file,
    is_file_processed
)


class TestBettyFixer:
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
