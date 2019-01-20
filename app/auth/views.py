from flask import render_template, request, redirect, url_for, flash
from . import auth
from flask_login import login_required
from .forms import LoginForm
from app.models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        user = User.query.filter_by(email=email).first()

        password = form.password.data

        if user is not None and user.verify_password(password):
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid email or password.')

    return render_template('auth/login.html', form=form)


@auth.route('/sec')
@login_required
def sec():
    return '只有登录用户才能访问这个页面！'
