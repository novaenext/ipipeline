from pathlib import Path
from setuptools import find_packages, setup

from ipipeline import __version__


with open(Path(__file__).parents[0] / 'README.md') as readme_file:
    readme = readme_file.read()

with open(Path(__file__).parents[0] / 'requirements.txt') as requirements_file:
    requirements = requirements_file.read().splitlines()

setup(
    name='ipipeline', 
    version=__version__, 
    description='a micro framework to build pipelines of different scopes', 
    url='https://github.com/novaenext/ipipeline', 
    author='novaenext', 
    author_email='contato@novaenext.com', 
    maintainer='novaenext', 
    maintainer_email='contato@novaenext.com', 
    license='proprietary', 
    platforms=['any'], 
    python_requires=">=3.5", 
    classifiers=[
        'Operating System :: OS Independent', 
        'Programming Language :: Python :: 3', 
        'Topic :: Scientific/Engineering'
    ], 
    packages=find_packages(exclude=('tests*',)), 
    install_requires=requirements, 
    long_description=readme, 
    long_description_content_type='text/markdown'
)
