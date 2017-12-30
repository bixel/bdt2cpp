from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='bdt2cpp',
    version='0.1.1',
    description='Transpile BDTs to C++ code.',
    long_description=long_description,
    packages=['bdt2cpp'],
    scripts=['bin/bdt2cpp'],
    package_data={
        'bdt2cpp': [
            'templates/main.cpp.template',
            'templates/Makefile.template',
            'templates/standalone.function.template',
            'templates/tree.function.template',
            ],
        },
    install_requires=[
        'jinja2',
        'numpy',
        ],
)
