"""Authentication system"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from .models import DB, Credential

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    cred = Credential.query.filter_by(email = email).first()

    if not cred or (cred.password != password):
        flash('Check your login credentials')
        return redirect(url_for('auth.login'))
    
    login_user(cred, remember=remember)
    
    return redirect(url_for('main.root'))

@auth.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    cred = Credential.query.filter_by(email = email).first()

    if cred:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_cred = Credential(email=email, username=username, password=password)

    DB.session.add(new_cred)
    DB.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))