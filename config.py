# -*- coding: utf-8-*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

__author__ = 'purejade'

import os

basedir = os.path.abspath(os.path.dirname(__file__))

import ConfigParser
config_handler = ConfigParser.ConfigParser()
config_handler.read('config.ini')

INIT_CONFIG={}

kv = config_handler.items('config')
for ele in kv:
    value = ele[1].strip()
    if value:
        INIT_CONFIG[ele[0].upper()] = ele[1]

class Config:

    SECRET_KEY = INIT_CONFIG.get('SECRET_KEY') or 'whdr'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = INIT_CONFIG.get('FLASKY_MAIL_SENDER')
    FLASKY_ADMIN = INIT_CONFIG.get('FLASKY_ADMIN')
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS= True
    MAIL_USERNAME =  INIT_CONFIG.get('MAIL_USERNAME')
    MAIL_PASSWORD = INIT_CONFIG.get('MAIL_PASSWORD')
    FLASKY_POSTS_PER_PAGE = int(INIT_CONFIG.get('FLASKY_POSTS_PER_PAGE'))
    FLASKY_COMMENTS_PER_PAGE = int(INIT_CONFIG.get('FLASKY_COMMENTS_PER_PAGE'))
    FLASKY_SLOW_DB_QUERY_TIME = int(INIT_CONFIG.get('FLASKY_SLOW_DB_QUERY_TIME'))
    FLASKY_FOLLOWERS_PER_PAGE = int(INIT_CONFIG.get('FLASKY_FOLLOWERS_PER_PAGE'))
    @staticmethod
    def init_app(app):
        pass

    def init_config(self):
        print self.SECRET_KEY

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI =INIT_CONFIG.get('DEV_DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = INIT_CONFIG.get('TEST_DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI =INIT_CONFIG.get('DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'data.sqlite')

config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':ProductionConfig
}

if __name__ == '__main__':

    config1 = Config()
    config1.init_config()