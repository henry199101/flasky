from flask import render_template, session, redirect, url_for, \
    current_app, request, flash
from .. import db
from ..models import User, Article
from ..email import send_email
from . import main
from .forms import NameForm, ArticleForm
from flask_login import current_user


@main.route('/', methods=['GET', 'POST'])
def index():
    form = ArticleForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        author = current_user._get_current_object()

        article = Article(title=title, content=content, author=author)
        db.session.add(article)
        db.session.commit()

        flash('Post Successfully !')

        return redirect(url_for('main.index'))

    articles = Article.query.order_by(Article.time_stamp.desc()).all()
    return render_template('index.html', form=form, articles=articles)
