#!/opt/bin/python

from os import path

from setuptools import setup

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md')) as f:
    long_description = f.read()


setup(
    name='metraixbeat_client',
    version='1.21.12',
    author='Benjamin Herson-Macarel',
    author_email='benjamin.herson-macarel-isc.france@ibm.com',
    description='Python client for the metricbeat monitoring system AIX.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='GNU General Public License v3.0',
    keywords='metricbeat aix server power7/8 monitoring instrumentation client',
    url='https://github.com/bhm-kyndryl/Metraixbeat',
    packages=[

    ],
    package_data={
        'metraixbeat_client': ['py.typed']
    },
    extras_require={
        'twisted': ['twisted'],
    },
    test_suite='tests',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: OS AIX version and Power architecture (Power8/7/6+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: System :: Monitoring system OS AIX servers ',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)
