#!/usr/bin/env python
from setuptools import setup
from io import open
import re

def read(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()

with open('pyPayokAPI/version.py', 'r', encoding='utf-8') as f:  # Credits: LonamiWebs
    version = re.search(r"^__version__\s*=\s*'(.*)'.*$",
                        f.read(), flags=re.MULTILINE).group(1)

setup(name='pyPayokAPI',
      version=version,
      description='Python implementation of Payok.io (https://payok.io/) pubilc API',
      long_description=read('README.md'),
      long_description_content_type="text/markdown",
      author='Badiboy',
      url='https://github.com/Badiboy/pyPayokAPI',
      packages=['pyPayokAPI'],
      requires=['requests', 'hashlib', 'urllib'],
      license='MIT license',
      keywords="Payok Pay API",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
      ],
)
