# -*- coding: utf-8-*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

__author__ = 'purejade'

from flask import Blueprint

auth = Blueprint('auth',__name__)

from . import views