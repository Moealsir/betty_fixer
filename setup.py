from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import shutil

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        # Check if Betty is installed
        betty_executable = shutil.which('betty')
        if betty_executable is None:
            print("Betty not found. Installing...")
            self.install_betty()

    def install_betty(self):
        # Add the commands to install Betty
        subprocess.run(['sudo', 'bettyfixer/install_dependency/.Betty/./install.sh'])
        subprocess.run(['sudo', 'cp', 'bettyfixer/install_dependency/.betty', '/bin/betty'])

setup(
    name='bettyfixer',
    version='0.1',
    packages=find_packages(),
    cmdclass={'install': CustomInstallCommand},  # Use the custom install command
    entry_points={
        'console_scripts': [
            'bettyfixer = bettyfixer.betty_fixer:main',
        ],
    },
    install_requires=[
        # Any dependencies your package may have
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A description of your package',
    url='https://github.com/yourusername/betty-fixer',  # Replace with your GitHub repository URL
    license='MIT',  # Replace with your desired license
)
