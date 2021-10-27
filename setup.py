from pathlib import Path
from setuptools import find_packages, setup

from ipipeline import __version__


root_path = Path(__file__).resolve().parents[0]

with open(root_path / 'README.md') as readme_file:
    readme = readme_file.read()

with open(root_path / 'requirement' / 'prod.txt') as requirement_file:
    requirements = requirement_file.read().splitlines()

setup(
    name='ipipeline', 
    version=__version__, 
    description=(
        'A micro framework to flexibly build and execute pipelines from '
        'different domains.'
    ), 
    url='https://github.com/novaenext/ipipeline', 
    author='novaenext', 
    maintainer='novaenext', 
    license='BSD-3-Clause', 
    platforms=['any'], 
    python_requires=">=3.5", 
    classifiers=[
        'Programming Language :: Python :: 3', 
        'License :: OSI Approved :: BSD License', 
        'Operating System :: OS Independent'
    ], 
    packages=find_packages(exclude=['test*']), 
    install_requires=requirements, 
    long_description=readme, 
    long_description_content_type='text/markdown'
)
