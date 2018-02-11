# -*- coding: utf-8 -*-

"""Main file to run apps

Author:
	@CakJuice <hd.brandoz@gmail.com>
"""

from app import app
from modules.base.blueprint import base_app

app.register_blueprint(base_app, url_prefix='')

if __name__ == '__main__':
	app.run(port=9999)
