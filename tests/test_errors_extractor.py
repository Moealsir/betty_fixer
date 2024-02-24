"""
Test the errors_extractor module.
"""
from subprocess import CompletedProcess, CalledProcessError
from bettyfixer.errors_extractor import exctract_errors


def test_exctract_errors_no_errors(mocker):
    """
    Test the exctract_errors function when Betty does not return any errors.
    """
    mock_subprocess = mocker.patch('subprocess.run', return_value=CompletedProcess(
        ['betty', 'file1.c'], 0, 'output', ''))
    mock_open = mocker.patch('builtins.open', mocker.mock_open())

    exctract_errors('file1.c', 'errors.txt')

    mock_subprocess.assert_called_once_with(['betty', 'file1.c'],
                                            capture_output=True, text=True, check=True)
    mock_open.assert_called_once_with('errors.txt', 'a', encoding='utf-8')
    mock_open().write.assert_called_once_with('output')
