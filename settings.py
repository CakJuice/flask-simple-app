"""
# Custom configuration of flask app
# @author: @CakJuice <hd.brandoz@gmail.com>
"""

import os

try:
    import local_settings
except Exception:
    print("[WARNING] Local settings not found!")


class Configuration:
    # flask config
    # SERVER_NAME = 'your_server_name'
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    DEBUG = True
    STATIC_DIR = os.path.join(APPLICATION_DIR, 'static')
    IMAGES_DIR = os.path.join(STATIC_DIR, 'images')
    try:
        SECRET_KEY = local_settings.SECRET_KEY
    except Exception:
        print("[WARNING] Secret key not provided!")

    # flask_sqlalchemy config
    try:
        SQLALCHEMY_DATABASE_URI = local_settings.SQLALCHEMY_DATABASE_URI
    except Exception:
        print("[WARNING] Database setting not valid!")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TABLE_PREFIX = 'cjfa_'

    # flask_mail config
    try:
        MAIL_SERVER = local_settings.MAIL_SERVER
        MAIL_USERNAME = local_settings.MAIL_USERNAME
        MAIL_PASSWORD = local_settings.MAIL_PASSWORD
        MAIL_DEFAULT_SENDER = local_settings.MAIL_DEFAULT_SENDER
    except Exception:
        print("[WARNING] Email setting not valid!")
    MAIL_PORT = 465
    MAIL_USE_SSL = True
