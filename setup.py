# -*- coding: utf-8 -*-
from distutils.core import setup
with open('README.md') as file:
    long_description = file.read()
setup(
  name = 'htmltree',
  packages = ['htmltree'], # this must be the same as the name above
  version = '0.7.3',
  description = 'Generalized nested html element tree with recursive rendering',
  long_description = long_description,
  author = 'Michael F. Ellis',
  author_email = 'michael.f.ellis@gmail.com',
  url = 'https://github.com/Michael-F-Ellis/htmltree', # use the URL to the github repo
  download_url = 'https://github.com/Michael-F-Ellis/htmltree/archive/0.7.3.tar.gz',
  keywords = ['html', 'css', 'Transcrypt', 'web app development'],
  classifiers = [],
)
