# -*- coding: utf-8 -*-

"""Helper to model

Author:
	@CakJuice <hd.brandoz@gmail.com>
"""

from app import db

class BaseModel(object):
	"""Mixin class with db.Model
	"""

	def save(self):
		"""Save (commit) data to database
		"""
		db.session.add(self)
		db.session.commit()
