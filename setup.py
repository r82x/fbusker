try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(name='fbusker',
      version='1.0',
      description='Get some photos',
      author='r82x',
      author_email='r82x@mailinator.com',
      url='https://github.com/r82x/fbusker',
      packages=['fbusker'],
      license='BSD',
      download_url="https://github.com/r82x/fbusker/tarball/master",
      install_requires=['fbconsole']
     )
