from setuptools import setup, find_packages
import sys, os

version = '0.2'

setup(name='BenderBot_Archive',
      version=version,
      description="A Pluggable Process for BenderBot",
      long_description="",
      classifiers=[],
      keywords='',
      author='Jeffrey Ness',
      author_email='jeffrey.ness@rackspace.com',
      url='',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['launchpadlib', 'BenderBot'],
      test_suite='nose.collector',
      )
