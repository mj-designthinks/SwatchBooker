#!/usr/bin/env python
# coding: utf-8
#
#       Copyright 2008 Olivier Berten <olivier.berten@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#

from urllib.parse import quote_plus, unquote_plus, urlencode
from urllib.request import urlopen, Request, urlretrieve
import importlib
import xml.etree.ElementTree as etree
from xml.sax.saxutils import escape as xmlescape
from xml.sax.saxutils import unescape as xmlunescape
from swatchbook import *
import string
from swatchbook.codecs import idfromvals

class WebSvc(object):
	about = False

for websvc in os.listdir((dirpath(__file__) or ".")):
	if os.path.splitext(websvc)[1] == '.py' and websvc not in ('__init__.py','template.py'):
		_mod = importlib.import_module('swatchbook.websvc.' + os.path.splitext(websvc)[0])
		globals().update({k: v for k, v in vars(_mod).items() if not k.startswith('_')})

members = {}

for websvc in WebSvc.__subclasses__():
	members[websvc.__name__] = websvc.__doc__
