"""Creating a package."""

from setuptools import setup

dependencies = ['ipython', 'pytest', 'pytest-watch', 'os', 'math', 'sys']

setup(
    name='client',
    description='Client and Server Step3 File Access.',
    version='0.5',
    author='Sean Beseler and Alex Short',
    author_email='ajshort2010@hotmail.com',
    py_modules=['client'],
    package_dir={'': 'src'},
    install_requires=dependencies,
    entry_points={'console_scripts': ['client = client:main']}
)
