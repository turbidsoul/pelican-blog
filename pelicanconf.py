#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Turbidsoul'
SITENAME = u"Turbidsoul's 小黑屋"
SITEURL = ''

ARTICLE_DIR='posts/'
PAGE_DIR='pages/'
OUTPUT_PATH=''

TIMEZONE = 'Asia/Chongqing'

DEFAULT_LANG = u'cn'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Turbidsoul\'s 小黑屋', 'http://blog.turbidsoul.me'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

ARTICLE_URL='posts/{slug}.html'
ARTICLE_SAVE_AS='posts/{slug}.html'
