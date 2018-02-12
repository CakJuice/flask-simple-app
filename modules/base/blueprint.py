# -*- coding: utf-8 -*-

"""To handle all route in base modules

Author:
	@CakJuice <hd.brandoz@gmail.com>
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from flask_login import login_user, logout_user

from .forms import SignupForm, LoginForm, ResendVerifyForm
from .models.user import User

base_app = Blueprint('base', __name__, template_folder='templates')

@base_app.route('/')
def homepage():
	return render_template('base/homepage.html')

@base_app.route('/signup/', methods=['GET', 'POST'])
def signup():
	"""Handle route user signup

	Decorators:
		base_app.route('/signup/', methods=['GET', 'POST'])

	Returns:
		Template|Redirect -- If method 'GET' will render template, but if method 'POST' and valid \
will redirect to 'base.homepage'
	"""
	if request.method == 'POST':
		form = SignupForm(request.form)
		if form.validate():
			user = form.save_user()
			if not user.is_admin:
				user.send_verification_mail()
			flash("Signup success. Please check your email to verify your account.", 'success')
			return redirect(url_for('base.homepage'))
		else:
			flash("Terjadi kesalahan!", 'danger')
	else:
		form = SignupForm()
	return render_template('base/signup.html', form=form)

@base_app.route('/verify/<verify_code>/')
def verify(verify_code):
	"""Handle route user verification account

	Decorators:
		base_app.route('/verify/<verify_code>/')

	Arguments:
		verify_code {String} -- Verification code to be checked

	Returns:
		Redirect -- Redirecting user after verify. If valid, user redirect to 'base.login'. \
If not valid, user redirect to 'base.homepage' and get error message.
	"""
	user = User.query.filter_by(verify_code=verify_code, status=User.STATUS_NOT_ACTIVE).first()
	if user is None:
		flash("Anda tidak diperkenankan melakukan ini!", 'danger')
		return redirect(url_for('base.homepage'))

	user.set_verified()
	flash("Status anda telah diverifikasi!", 'success')
	return redirect(url_for('base.login'))

@base_app.route('/resend-verify/', methods=['GET', 'POST'])
def resend_verify():
	"""Handle route user resend verification account

	Decorators:
		base_app.route('/resend-verify/', methods=['GET', 'POST'])

	Returns:
		Template|Redirect -- If method 'GET' will render template, but if method 'POST' and valid \
will redirect to 'base.homepage'
	"""
	if request.method == 'POST':
		form = ResendVerifyForm(request.form)
		if form.validate():
			form.user.resend_verification_mail()
			flash("Verification link has been send. Please check your email.", 'success')
			return redirect(url_for('base.homepage'))
		else:
			flash("Terjadi kesalahan!", 'danger')
	else:
		form = ResendVerifyForm()
	return render_template('base/resend_verify.html', form=form)

@base_app.route('/login/', methods=['GET', 'POST'])
def login():
	"""Handle route user login

	Decorators:
		base_app.route('/login/', methods=['GET', 'POST'])

	Returns:
		Template|Redirect -- If method 'GET' will render template, but if method 'POST' and valid \
will redirect to 'base.homepage'
	"""
	if request.method == 'POST':
		form = LoginForm(request.form)
		if form.validate():
			login_user(form.user, remember=form.remember_me.data)
			flash("Successfully logged in as {}.".format(form.user.email), 'success')
			return redirect(request.args.get('next', default=url_for('base.homepage')))
	else:
		form = LoginForm()
	return render_template('base/login.html', form=form)

@base_app.route('/logout/')
def logout():
	"""Handle route user logout

	Decorators:
		base_app.route('/logout/')

	Returns:
		Redirect -- If valid redirect to next arguments or 'base/homepage'
	"""
	if g.user.is_authenticated:
		logout_user()
		flash("You have been logged out.", 'success')
		return redirect(request.args.get('next', default=url_for('base.homepage')))
	else:
		flash("You're not logged in!", 'danger')
		return redirect(url_for('base.homepage'))
