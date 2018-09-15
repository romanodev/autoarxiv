from setuptools import setup,find_packages
import os


setup(name='autoarxiv',
      version='0.9.01',
      description='A program that submits manuscripts to arXiv ',
      author='Giuseppe Romano',
      author_email='romanog@mit.edu',
      classifiers=['Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.6'],
      install_requires=['selenium'],
      license='GPLv2',\
      packages = ['autoarxiv'],
      entry_points = {
     'console_scripts': ['autoarxiv=autoarxiv.autoarxiv:main'],
      },
      zip_safe=False)
