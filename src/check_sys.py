import os
import sys
from sys import platform


class SystemCheck:
    """Check the system requirements"""

    def __init__(self):
        self.check_os_system()
        self.check_python_installed()
        self.check_python_version()
        self.check_git_installed()

    def check_os_system(self):
        """check operating system"""
        if platform != "linux":
            print("Only Linux is supported")
            return sys.exit(1)

    def check_python_installed(self):
        """check if python is installed"""
        if os.system("python3 --version") != 0:
            print("Python is not installed")
            return sys.exit(1)

    def check_python_version(self):
        """check python version"""
        if os.system("python3 --version") >= 3.10:
            print("Please use Python 3.10 or higher")
            return sys.exit(1)

    def check_git_installed(self):
        """check if git is installed"""
        if os.system("git --version") != 0:
            print("Git is not installed")
            return sys.exit(1)

    def __str__(self):
        return "SystemCheck class"
