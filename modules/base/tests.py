import unittest

from main import app
from .models import User
from test_helpers import DummyTest

class BaseTest(unittest.TestCase, DummyTest):
	def setUp(self):
		self.dummy_setup()

	def tearDown(self):
		self.dummy_teardown()

	def test_get_signup(self):
		response = self.app.get('/')
		assert response.status_code == 200

	def test_post_signup_success(self):
		response = self.dummy_get_signup()
		assert 'success' in str(response.data)

	def test_get_verify_success(self):
		self.dummy_get_signup()
		user = User.query.get(1)
		response = self.app.get('/verify/{}'.format(user.verify_code))
		assert 'login' in str(response.data)