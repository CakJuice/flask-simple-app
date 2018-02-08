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

	def test_post_signup_fail_required(self):
		response = self.app.post('/signup/', data={
			'password': 'cakjuice',
			'password_confirm': 'cakjuice'
		}, follow_redirects=True)
		assert 'danger' in str(response.data)

	def test_post_signup_fail_not_email(self):
		response = self.app.post('/signup/', data={
			'email': 'Not email',
			'name': 'Cak Juice',
			'password': 'cakjuice',
			'password_confirm': 'cakjuice'
		}, follow_redirects=True)
		assert 'danger' in str(response.data)

	def test_post_signup_fail_email_not_unique(self):
		self.dummy_get_signup()
		response = self.dummy_get_signup()
		assert 'danger' in str(response.data)

	def test_post_signup_fail_password_not_same(self):
		response = self.app.post('/signup/', data={
			'email': 'test@test.com',
			'name': 'Cak Juice',
			'password': 'cakjuice',
			'password_confirm': 'weladalah'
		}, follow_redirects=True)
		assert 'danger' in str(response.data)

	def test_get_verify_success(self):
		self.dummy_get_signup()
		user = User.query.get(1)
		response = self.app.get('/verify/{}/'.format(user.verify_code), follow_redirects=True)
		assert 'login' in str(response.data)

	def test_get_verify_failed(self):
		self.dummy_get_signup()
		response = self.app.get('/verify/{}/'.format('ngawurcode'), follow_redirects=True)
		assert 'danger' in str(response.data)

	def test_get_verify_not_found(self):
		response = self.app.get('/verify/')
		assert response.status_code == 404