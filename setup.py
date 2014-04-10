from distutils.core import setup

setup(name='socialscraper',
      version='0.0.1',
      description='Scrapers for Social Networks',
      author='Moritz Gellner',
      author_email='moritz.gellner@gmail.com',
      url='http://dev.alpaca.io/',
      packages=['twitter','facebook'],
      install_requires=[
      	'beautifulsoup4==4.3.2',
      	'mechanize==0.2.5',
      	'requests==2.2.1'
      ]
     )