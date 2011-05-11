from distutils.core import setup

fp = open("README.txt")
long_description=fp.read()
fp.close()

setup(
    name='redhawk',
    version='1.0.1',
    description='An AST based navigation system.',
    long_description=long_description,
    author="Pranesh Srinivasan",
    author_email="spranesh@gmail.com",
    license="BSD Two Clause License",
    url="http://pypi.python.org/pypi/redhawk/",

    packages=['redhawk'
             ,'redhawk.examples'
             ,'redhawk.c'
             ,'redhawk.common'
             ,'redhawk.common.readers'
             ,'redhawk.common.writers'
             ,'redhawk.python'
             ,'redhawk.utils'],

    install_requires = ['PyYAML>=3.09'
                      ,'nose>=0.11'
                      ,'pycparser>=2.02'
                      # ,'pygraphviz>=0.99' # Optional Dependency
                      ],

    scripts=['bin/redhawk_prompt'
            ,'bin/redhawk']
)
