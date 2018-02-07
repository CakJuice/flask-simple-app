from flask import Blueprint, render_template, request, redirect, url_for, flash

from .forms import SignupForm
from .models import User

base_app = Blueprint('base', __name__, template_folder='templates')

@base_app.route('/')
def homepage():
	return render_template('base/homepage.html')

@base_app.route('/signup/', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		form = SignupForm(request.form)
		if form.validate():
			form.save_user()
			flash("Signup Berhasil!", 'success')
			return redirect(url_for('base.homepage'))
	else:
		form = SignupForm()
	return render_template('base/signup.html', form=form)

@base_app.route('/verify/<verify_code>')
def verify(verify_code):
	user = User.query.filter_by(verify_code==verify_code).first()
	if user is None:
		flash("Anda tidak diperkenankan melakukan ini!", 'warning')
		return redirect(url_for('base.homepage'))

	user.set_verified()
	flash("Status anda telah diverifikasi!", 'success')
	return redirect(url_for('base.login'))

@base_app.route('/login/')
def login():
	return 'This is login page!'