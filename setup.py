from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='revived',
    version='0.1.0',

    description='Redux-inspired library in python',
    long_description=long_description,

    url='https://github.com/RookieGameDevs/revived',
    author='Lorenzo Berni',
    author_email='lorenzo@rookiegamedevs.io',

    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
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
