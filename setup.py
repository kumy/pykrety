#!/usr/bin/env python

from distutils.core import setup

setup(name='pykrety',
      version='0.1',
      description='Python wrapper around Geokrety.org',
      author='Mathieu Alorent',
      author_email='pykrety@kumy.net',
      license='gplv2',
      url='https://github.com/kumy/pykrety',
      requires=['BeautifulSoup', 'xml.sax', 'urllib2', 'urllib', 'requests', 'csv'],
      packages=['pykrety', 'pykrety.parsers']
     )
