from setuptools import setup

def readme():
    with open('README') as f:
        return f.read()



setup(name='nanocorr',
      version='0.01',
      description='Correction For Oxford Nanopore',
      long_description=readme(),
      url='https://github.com/jgurtowski/nanocorr',
      author='James Gurtowski',
      author_email='gurtowsk@cshl.edu',
      license='GPL',
      #packages=['jptools'],
      install_requires = [
        "jptools >= 0.1",
        ],
      dependency_links = [
        "git+https://github.com/jgurtowski/jptools#egg=jptools-0.1",
        ],
      )
      
      
      
      
