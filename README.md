# Tweakers API
A small Python wrapper for [tweakers.net](https://tweakers.net/).

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
