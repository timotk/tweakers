# Tweakers
[![Build Status](https://travis-ci.org/timotk/tweakers.svg?branch=master)](https://travis-ci.org/timotk/tweakers)
[![codecov](https://codecov.io/gh/timotk/tweakers/branch/master/graph/badge.svg)](https://codecov.io/gh/timotk/tweakers)
[![PyPI](https://img.shields.io/pypi/v/tweakers.svg)](https://pypi.org/project/tweakers)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tweakers.svg)

A Python wrapper for [tweakers.net](https://tweakers.net/)

## Install
```
pip install tweakers
```

## Usage
```
import tweakers
```

Print a list of active topics:
```
for topic in tweakers.gathering.active_topics():
    print(topic.title)
```

Search for topics:
```
for topic in tweakers.gathering.search('tweakers.net'):
    print(topic.title)
```
