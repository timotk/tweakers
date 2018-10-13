from setuptools import setup

from tweakers import __version__


with open('README.md') as f:
    readme = f.read()

with open('requirements.txt') as f:
    requirements = f.read()


setup(
    name='tweakers',
    version=__version__,
    description='A Python API for https://tweakers.net',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/timotk/tweakers',
    packages=['tweakers'],
    python_requires='>=3.6',
    install_requires=requirements,
    test_requires=['pytest'],
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
