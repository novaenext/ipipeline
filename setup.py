from pathlib import Path
from setuptools import find_packages, setup

from ipipeline import __version__


proj_path = Path(__file__).resolve().parents[0]

with open(str(proj_path / 'README.md')) as readme_file:
    readme = readme_file.read()

with open(str(proj_path / 'requirements' / 'prod.txt')) as requirements_file:
    requirements = requirements_file.read().splitlines()

setup(
    name='ipipeline', 
    version=__version__, 
    description=(
        'A micro framework for building and executing pipelines from '
        'different domains.'
    ), 
    url='https://github.com/novaenext/ipipeline', 
    author='novaenext', 
    license='BSD-3-Clause', 
    platforms=['any'], 
    python_requires=">=3.6", 
    classifiers=[
        'License :: OSI Approved :: BSD License', 
        'Operating System :: OS Independent', 
        'Programming Language :: Python :: 3'
    ], 
    packages=find_packages(exclude=['test*']), 
    install_requires=requirements, 
    long_description=readme, 
    long_description_content_type='text/markdown'
)
