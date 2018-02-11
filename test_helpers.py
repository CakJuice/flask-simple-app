import os
from main import app
from app import db

class DummyTest(object):
	"""Use for dummy testing
	"""

	def dummy_setup(self):
		"""Setup / initialize test
		"""
		self.test_db = '{}/test.db'.format(app.config['APPLICATION_DIR'])
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(self.test_db)
		app.testing = True
		app.config['WTF_CSRF_ENABLED'] = False
		self.app = app.test_client()
		with app.app_context():
			db.create_all()

	def dummy_teardown(self):
		"""Call when test done.
		"""
		os.unlink(self.test_db)

	def dummy_get_signup(self):
		"""Data dummy for signup test

		Returns:
			Object -- Post data dummy
		"""
		return self.app.post('/signup/', data={
			'email': 'hello@cakjuice.com',
			'name': 'Cak Juice',
			'password': 'cakjuice',
			'password_confirm': 'cakjuice'
		}, follow_redirects=True)