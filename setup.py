from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='bdt2cpp',
    version='0.1.3',
    description='Transpile BDTs to C++ code.',
    long_description=long_description,
    packages=['bdt2cpp'],
    scripts=['bin/bdt2cpp'],
    author='Kevin Heinicke <kevin@kehei.de>',
    url='https://github.com/bixel/bdt2cpp',
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
        ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Code Generators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
)
