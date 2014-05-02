from distutils.core import setup

setup(name='socialscraper',
      version='0.0.1',
      description='Scrapers for Social Networks',
      author='Moritz Gellner',
      author_email='moritz.gellner@gmail.com',
      url='http://dev.alpaca.io/',
      packages=['socialscraper'],
      install_requires=[
        'beautifulsoup4==4.3.2',
        'cssselect==0.9.1',        
        'enum34==0.9.23',
        'facebook-sdk==0.4.0',
        'lxml==3.3.4',        
      	'mechanize==0.2.5',
	      'python-dateutil==2.2',
      	'requests==2.2.1',
        'six==1.6.1',
        'wsgiref==0.1.2'
      ]
     )