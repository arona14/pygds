from setuptools import setup

setup(name='pygds',
      version='0.1',
      description='A python package to make it easy interacting with gds ',
      url=' https://mbayehann@bitbucket.org/mbayehann/pygds.git',
      author='Mbaye Hann',
      author_email='mbaye@ctsfares.com',
      license='MIT',
      packages=['pygds'],
      install_requires=[
          'pyodbc',
          'pandas',
          'psycopg2',
          'jxmlease',
          'xmltodict',
      ],
      include_package_data=True,
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
