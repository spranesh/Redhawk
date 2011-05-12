from setuptools import setup, find_packages

import redhawk

def ReadFile(f):
  fp = open(f)
  result=fp.read()
  fp.close()
  return result.strip()

setup(
    name='redhawk',
    description='An AST based navigation system.',
    version=redhawk.GetVersion(),
    long_description=ReadFile("README.txt"),
    author="Pranesh Srinivasan",
    author_email="spranesh@gmail.com",
    license="The BSD 2-Clause License",
    url="http://pypi.python.org/pypi/redhawk/",

    # packages = find_packages()
    packages=[
      'redhawk',
      'redhawk.c',
      'redhawk.c.utils',
      'redhawk.common',
      'redhawk.common.readers',
      'redhawk.common.writers',
      'redhawk.examples',
      'redhawk.python',
      'redhawk.python.utils',
      'redhawk.utils',
      'redhawk.scripts',
      'redhawk.test'],

    package_data = {
      'redhawk.utils': [
        'fake_libc_include/*'
       ],
      'redhawk.test': [
        'files/python/*',
        'files/c/*',
        'files/dot/*',
        'files/examples/*',
       ],
      'redhawk.common': [
        '*.yaml'
       ]
      },

    install_requires = [
      # 'PyYAML>=3.09',
      # 'nose>=0.11',
      # ,'pygraphviz>=0.99' # Optional Dependency
      'pycparser>=2.02' ],

    classifiers = [
      "Development Status :: 3 - Alpha",
      "Environment :: Console",
      "Environment :: Plugins",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: BSD License",
      "Operating System :: POSIX :: Linux",
      "Programming Language :: C",
      "Programming Language :: Python :: 2.6",
      "Programming Language :: Python :: 2.7",
      "Topic :: Software Development",
      "Topic :: Utilities"],

    scripts=['bin/redhawk']
)
