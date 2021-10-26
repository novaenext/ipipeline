from pathlib import Path
from setuptools import find_packages, setup

from ipipeline import __version__


project_path = Path(__file__).resolve().parents[0]

with open(project_path / 'README.md') as readme_file:
    readme = readme_file.read()

with open(project_path / 'requirement.txt') as requirement_file:
    requirement = requirement_file.read().splitlines()

setup(
    name='ipipeline', 
    version=__version__, 
    description=(
        'A micro framework to flexibly build and execute pipelines from '
        'different domains.'
    ), 
    url='https://github.com/novaenext/ipipeline', 
    author='novaenext', 
    author_email='contato@novaenext.com', 
    maintainer='novaenext', 
    maintainer_email='contato@novaenext.com', 
    license='BSD-3-Clause', 
    platforms=['any'], 
    python_requires=">=3.5", 
    classifiers=[
        'Operating System :: OS Independent', 
        'Programming Language :: Python :: 3', 
        'Topic :: Scientific/Engineering'
    ], 
    packages=find_packages(exclude=('test*',)), 
    install_requires=requirement, 
    long_description=readme, 
    long_description_content_type='text/markdown'
)
