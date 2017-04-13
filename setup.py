from distutils.core import setup

setup(
    name='invaana-scout',
    version='0.0.1',
    packages=['scout', 'scout.db', 'scout.scider', 'tests',
              'scout.sanitizer', 'examples'],
    url='https://github.com/invaana/scout',
    license='',
    author='Ravi RT Merugu',
    author_email='rrmerugu@gmail.com',
    description='This is a data aggregation framework for scouting and aggregating Scientific Data. '
)
