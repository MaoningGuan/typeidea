#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .base import *

DEBUG = False

ALLOWED_HOSTS = []  # 配置服务器的域名


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'typeidea_db',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '<正式数据库的IP>',
        'PORT': 3306,
        'CONN_MAX_AGE': 5 * 60,
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}


