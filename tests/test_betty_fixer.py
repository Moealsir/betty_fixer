"""
Test the betty_fixer module.
"""
import os
import pytest
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
