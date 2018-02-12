# -*- coding: utf-8 -*-

"""Use to manage database. Integrated with app.manager

Author:
	@CakJuice <hd.brandoz@gmail.com>
"""

from app import manager
from main import *
from modules.base.models.user import User
from modules.base.models.mail import MailOutgoing

if __name__ == '__main__':
	manager.run()
