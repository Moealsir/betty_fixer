"""
Test the backup module.
"""
import os
import shutil
import pytest
from bettyfixer import backup


class TestBackup:
    """Test the backup module."""

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Create a test file."""  # pylint: disable=attribute-defined-outside-init
        self.test_file = 'test.c'
        with open(self.test_file, 'w', encoding='utf-8') as f:
            self.test_file = f.name
            f.write(
                'int main(int argc, char **argv){\nprintf("Hello World"\nreturn 0; \n}')
        yield
        os.remove(self.test_file)
        if os.path.exists(self.test_file + '.bak'):
            os.remove(self.test_file + '.bak')

    def test_create_backup(self):
        """Test the create_backup function."""
        backup.create_backup(self.test_file)
        assert os.path.exists(self.test_file + '.bak')
        with open(self.test_file + '.bak', 'r', encoding='utf-8') as f:
            assert 'int main(int argc,' in f.read()
        os.remove(self.test_file + '.bak')

    def test_create_backup_same_file_error(self, mocker, capsys):
        """Test the create_backup function with a same file error."""

        mocker.patch('shutil.copy2', side_effect=shutil.SameFileError)
        backup.create_backup(self.test_file)
        captured = capsys.readouterr()
        assert 'Src and dest are same file' in captured.out
        assert not os.path.exists(self.test_file + '.bak')

    def test_create_backup_file_not_found(self, mocker, capsys):
        """Test the create_backup function with a file not found error."""
        mocker.patch('shutil.copy2', side_effect=FileNotFoundError)
        backup.create_backup(self.test_file)
        captured = capsys.readouterr()
        assert 'File not found' in captured.out
        assert not os.path.exists(self.test_file + '.bak')

    def test_create_backup_is_a_directory_error(self, mocker, capsys):
        """Test the create_backup function with an is a directory error."""
        mocker.patch('shutil.copy2', side_effect=IsADirectoryError)
        backup.create_backup(self.test_file)
        captured = capsys.readouterr()
        assert 'Is a directory error' in captured.out
        assert not os.path.exists(self.test_file + '.bak')

    def test_create_backup_permission_error(self, mocker, capsys):
        """Test the create_backup function with a permission error."""
        mocker.patch('shutil.copy2', side_effect=PermissionError)
        backup.create_backup(self.test_file)
        captured = capsys.readouterr()
        assert 'Permission error' in captured.out
        assert not os.path.exists(self.test_file + '.bak')

    def test_create_backup_os_error(self, mocker, capsys):
        """Test the create_backup function with an os error."""
        mocker.patch('shutil.copy2', side_effect=OSError)
        backup.create_backup(self.test_file)
        captured = capsys.readouterr()
        assert 'Unexpected error' in captured.out
        assert not os.path.exists(self.test_file + '.bak')
