from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='bdt2cpp',
    version='0.0.1',
    description='Transpile BDTs to C++ code.',
    long_description=long_description,
    packages=['bdt2cpp'],
)
