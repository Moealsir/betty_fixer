"""
This file is used to package the bettyfixer tool and install it in the system.
"""
# import subprocess
# import time
# import shutil
from pathlib import Path
from setuptools import setup, find_packages
# from setuptools.command.install import install

setup(
    name='bettyfixer',
    version='1.4.6',
    packages=find_packages(),

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
    description='Betty Fixer is a tool designed to automatically fix coding style \
issues in C files based on the Betty coding style guidelines.\
It performs corrections to ensure that the code complies with the Betty style, \
making it more readable and consistent.',
    # Replace with your GitHub repository URL
    url='https://github.com/Moealsir/betty_fixer',
    license='MIT',  # Replace with your desired license

    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown"
)
