import pytest

from unittest.mock import patch
from src.check_sys import (
    SystemCheck,
)


def test_check_os_system_linux():
    """Test if the system check passes on a Linux system without exiting."""
    with patch("src.check_sys.platform", new="linux"):
        with patch("src.check_sys.sys.exit") as mock_exit:
            SystemCheck()
            mock_exit.assert_not_called()


def test_check_os_system_non_linux():
    """Test if the system check exits on non-Linux systems."""
    with patch("src.check_sys.platform", new="win32"):
        with patch("src.check_sys.sys.exit") as mock_exit:
            SystemCheck()
            mock_exit.assert_called_once_with(1)


def test_check_python_installed_when_python_is_installed():
    with patch("os.system") as mock_system:
        mock_system.return_value = 0
        instance = SystemCheck()
        # Execute the function, expecting no exceptions or sys.exit
        instance.check_python_installed()
        mock_system.assert_called_with("python3 --version")


def test_check_python_installed_when_python_is_not_installed():
    with (
        patch("os.system") as mock_system,
        pytest.raises(SystemExit) as pytest_wrapped_e,
    ):
        mock_system.return_value = 1
        with patch("sys.exit") as mock_exit:
            mock_exit.side_effect = SystemExit
            instance = SystemCheck()
            instance.check_python_installed()
            mock_system.assert_called_with("python3 --version")
            mock_exit.assert_called_once_with(1)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1


def test_check_python_version_correct():
    """Test that no exit occurs if Python 3.10 or higher is installed."""
    with patch(
        "src.check_sys.os.system", return_value=0
    ):  # Assuming Python 3.10+ is correctly installed
        with patch("src.check_sys.sys.exit") as mock_exit:
            SystemCheck()
            mock_exit.assert_not_called()


def test_check_git_installed_when_git_is_installed():
    with patch("os.system") as mock_system:
        mock_system.return_value = 0
        instance = SystemCheck()
        # Execute the function, expecting no exceptions or sys.exit
        instance.check_git_installed()
        mock_system.assert_called_with("git --version")


def test_check_git_installed_when_git_is_not_installed():
    with (
        patch("os.system") as mock_system,
        pytest.raises(SystemExit) as pytest_wrapped_e,
    ):
        mock_system.return_value = 1
        with patch("sys.exit") as mock_exit:
            mock_exit.side_effect = SystemExit
            instance = SystemCheck()
            instance.check_git_installed()
            mock_system.assert_called_with("git --version")
            mock_exit.assert_called_once_with(1)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1


def test_check_git_installed_correctly():
    """Test that no exit occurs if Git is installed."""
    with patch("src.check_sys.os.system", return_value=0):
        with patch("src.check_sys.sys.exit") as mock_exit:
            _ = SystemCheck()
            mock_exit.assert_not_called()
