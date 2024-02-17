"""
Test the backup module.
"""
import os
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
            assert f.read() == 'test'
        os.remove(self.test_file + '.bak')

    def test_create_backup_same_file_error(self):
        """Test the create_backup function with a same file error."""
        with open(self.test_file + '.bak', 'w', encoding='utf-8') as f:
            f.write('test')
        backup.create_backup(self.test_file)
        assert os.path.exists(self.test_file + '.bak')
        with open(self.test_file + '.bak', 'r', encoding='utf-8') as f:
            assert f.read() == 'test'
        os.remove(self.test_file + '.bak')

    def test_create_backup_file_not_found(self):
        """Test the create_backup function with a file not found error."""
        os.remove(self.test_file)
        backup.create_backup(self.test_file)
        assert not os.path.exists(self.test_file + '.bak')

    def test_create_backup_is_a_directory_error(self):
        """Test the create_backup function with an is a directory error."""
        os.remove(self.test_file)
        os.mkdir(self.test_file)
        backup.create_backup(self.test_file)
        assert not os.path.exists(self.test_file + '.bak')

    def test_create_backup_permission_error(self):
        """Test the create_backup function with a permission error."""
        os.chmod(self.test_file, 0o000)
        backup.create_backup(self.test_file)
        assert not os.path.exists(self.test_file + '.bak')

    def test_create_backup_os_error(self):
        """Test the create_backup function with an os error."""
        os.remove(self.test_file)
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write('test')
        os.chmod(self.test_file, 0o000)
        backup.create_backup(self.test_file)
        assert not os.path.exists(self.test_file + '.bak')
