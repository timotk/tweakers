# Tweakers
![Build](https://github.com/timotk/tweakers/workflows/Build/badge.svg)
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

### Gathering
With the `tweakers.gathering` module you can access the forum.
#### Active topics
```
for topic in tweakers.gathering.active_topics():
    print(topic.title)
```

#### Search
```
for topic in tweakers.gathering.search('tweakers.net'):
    print(topic.title)
```

### Topic
#### Get comments for a specific topic
```
topic = Topic("https://gathering.tweakers.net/forum/list_messages/1551828")
for comment in topic.comments(page=1):
    print(comment.user.name, comment.text)
```

#### Generate new comments as they are added
```
for comment in topic.comment_stream():
    print(comment.user.name, comment.text)
```

### Login
```
tweakers.login("YOUR_USERNAME", "YOUR_PASSWORD")
```
Now you can access pages that are unavailable for logged out users:
```
for topic in tweakers.gathering.bookmarks():
    print(topic.name)
```
