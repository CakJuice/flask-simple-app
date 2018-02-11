# -*- coding: utf-8 -*-

"""
# Custom configuration of flask app
# @author: @CakJuice <hd.brandoz@gmail.com>
"""

import os

class Configuration(object):
	# flask config
	SERVER_NAME = 'your_server_name'
	APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
	DEBUG = True
	STATIC_DIR = os.path.join(APPLICATION_DIR, 'static')
	IMAGES_DIR = os.path.join(STATIC_DIR, 'images')
	SECRET_KEY = 'random_secret_key'

	# flask_sqlalchemy config
	SQLALCHEMY_DATABASE_URI = 'your_database_uri'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# flask_mail config
	MAIL_SERVER = 'your_mail_server'
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USERNAME = 'your_mail_username'
	MAIL_PASSWORD = 'your_mail_password'
