from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

VERSION = '0.1.2'

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

with open(path.join(here, 'CHANGELOG.rst'), encoding='utf-8') as f:
    CHANGELOG = f.read()

setup(
    name='revived',
    version=VERSION,

    description='Redux-inspired library in python',
    long_description='\n\n'.join([
        LONG_DESCRIPTION,
        CHANGELOG
    ]),

    url='https://github.com/RookieGameDevs/revived',
    author='Lorenzo Berni',
    author_email='lorenzo@rookiegamedevs.io',

    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='state store redux',

    packages=find_packages(exclude=['tests']),

    install_requires=[],

    extras_require={
        'dev': [''],
        'test': ['pytest'],
    },
)
