from setuptools import setup, find_packages
from setuptools.command.install import install

setup(
    name='bettyfixer',
    version='0.1',
    packages=find_packages(),
    package_data={
        'bettyfixer': ['install_dependency/.Betty/install.sh', 'install_dependency/.betty'],
    },
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
