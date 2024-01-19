from setuptools import setup, find_packages
from setuptools.command.install import install
from pathlib import Path
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
        # Get the directory where this setup.py is located
        current_directory = Path(__file__).resolve().parent

        # Add the commands to install Betty
        betty_install_script = current_directory / 'bettyfixer' / 'install_dependency' / '.Betty' / 'install.sh'
        betty_dest = Path('/usr/local/bin/betty')  # Adjust the destination if needed

        subprocess.run(['bash', str(betty_install_script)])
        shutil.copy(str(current_directory / 'bettyfixer' / 'install_dependency' / '.betty'), str(betty_dest))
        betty_dest.chmod(0o755)  # Make sure the copied file is executable

setup(
    name='bettyfixer',
    version='1.4.2',
    packages=find_packages(),
    cmdclass={'install': CustomInstallCommand},  # Use the custom install command
    entry_points={
        'console_scripts': [
            'bettyfixer = bettyfixer.betty_fixer:main',
            'show-changelog = show_changelog:main',  # Include the show-changelog script
        ],
    },
    install_requires=[
        'colorama',
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
