from setuptools import setup, find_packages
from setuptools.command.install import install
from pathlib import Path
import subprocess
import time
import shutil

class CustomInstallCommand(install):
    def run(self):
        install.run(self)

        # Check if Betty is installed
        betty_executable = shutil.which('betty')
        if betty_executable is None:
            print("Betty not found. Installing...")
            self.install_betty()

        # Check if exuberant-ctags is installed, if not install it
        ctags_executable = shutil.which('ctags')
        if ctags_executable is None:
            print("Exuberant-ctags not found. Installing...")
            self.install_ctags()

    def install_betty(self):
        try:
            # Clone Betty repository
            subprocess.run(["git", "clone", "https://github.com/alx-tools/Betty.git"])

            # Wait until cloning finishes
            cloned_directory = Path("Betty")
            while not cloned_directory.exists():
                time.sleep(1)  # Adjust the sleep interval as needed
            
            # Run Betty install script
            subprocess.run(["sudo", "./Betty/install.sh"])

            # Download and copy .betty file
            subprocess.run(["wget", "https://github.com/Moealsir/betty_fixer/raw/main/bettyfixer/install_dependency/.betty"])
            subprocess.run(["sudo", "cp", ".betty", "/bin/betty"])

            # Clean up
            subprocess.run(["rm", "-rf", "Betty", ".betty"])
        except Exception as e:
            print(f"Error installing Betty: {e}")

    def install_ctags(self):
        try:
            # Install exuberant-ctags
            subprocess.run(["sudo", "apt-get", "install", "exuberant-ctags"])
        except Exception as e:
            print(f"Error installing exuberant-ctags: {e}")

 
setup(
    name='bettyfixer',
    version='1.4.5.3',
    packages=find_packages(),
    cmdclass={'install': CustomInstallCommand},  # Use the custom install command
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
