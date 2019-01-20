from flask import render_template, request, redirect, url_for, flash
from . import auth
from flask_login import login_required
from .forms import LoginForm, RegisterForm
from app.models import User
from flask_login import login_user, logout_user
from app import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            flash('Login Successfully !')
            return redirect(next)
        flash('Invalid email or password.')

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out !')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data

        user = User(email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()

        flash('You can login now !')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)
