from setuptools import setup, find_packages
from setuptools.command.install import install
from pathlib import Path
import subprocess
import shutil

from setuptools.command.install import install
import shutil
import subprocess

# class CustomInstallCommand(install):
#     def run(self):
#         install.run(self)
#         # Check if Betty is installed
#         betty_executable = shutil.which('betty')
#         if betty_executable is None:
#             print("Betty not found. Installing...")
#             self.install_betty()

#         # Check if black is installed, if not install it
#         black_executable = shutil.which('black')
#         if black_executable is None:
#             print("Black not found. Installing...")
#             self.install_black()

#         # Check if exuberant-ctags is installed, if not install it
#         ctags_executable = shutil.which('ctags')
#         if ctags_executable is None:
#             print("Exuberant-ctags not found. Installing...")
#             self.install_ctags()

#     def install_betty(self):
#         subprocess.run(["sh", "bettyfixer/install_dependency/.Betty/install.sh"])
#         subprocess.run([
#             "sudo", "cp", "bettyfixer/install_dependency/.betty", "/bin/betty"])

#     def install_black(self):
#         subprocess.run(["sudo", "pip", "install", "black"])

#     def install_ctags(self):
#         subprocess.run(["sudo", "apt-get", "install", "exuberant-ctags"])
 
setup(
    name='bettyfixer',
    version='1.4.5',
    packages=find_packages(),
    scripts=['install.sh'],
    # cmdclass={'install': CustomInstallCommand},  # Use the custom install command
    entry_points={
        'console_scripts': [
            'bettyfixer = bettyfixer.betty_fixer:main',
            'show-changelog = show_changelog:main',  # Include the show-changelog script
        ],
    },
    install_requires=[
        'colorama', 'black',
        # other dependencies...
    ],
    author='Moealsir',
    author_email='mohamedwdalsir@gmail.com',
    description='Betty Fixer is a tool designed to automatically fix coding style issues in C files based on the Betty coding style guidelines. It performs corrections to ensure that the code complies with the Betty style, making it more readable and consistent.',
    url='https://github.com/Moealsir/betty_fixer',  # Replace with your GitHub repository URL
    license='MIT',  # Replace with your desired license

    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown"
)
