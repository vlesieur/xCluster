import os

from basedir import basedir

SECRET = 'jf1G2tZvFc74yetoo1ElmrFUT3UN91ZS'

class BaseConfig(object):
    MONGODB_SETTINGS = {
        # 'USERNAME': None,
        # 'PASSWORD': None,
        # 'HOST': '127.0.0.1',
        # 'PORT': 27017,
        # 'DB': 'xclusterdb'
		# Config mLab
        'USERNAME': 'xcluster',
        'PASSWORD': 'xcluster',
        'HOST': 'ds050869.mlab.com',
        'PORT': 50869,
        'DB': 'bd_films'
    }
    SECRET_KEY = SECRET
    DEBUG = True

class TestingConfig(object):
    """Development configuration."""
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False