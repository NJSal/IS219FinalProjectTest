import logging

from flask import Blueprint, render_template, redirect, url_for, flash, current_app, abort
from flask_login import login_user, login_required, logout_user, current_user
from jinja2 import TemplateNotFound
from sqlalchemy import select
from werkzeug.security import generate_password_hash

from app.auth.decorators import admin_required
from app.auth.forms import login_form, register_form, profile_form, security_form, user_edit_form, create_user_form
from app.db import db
from app.db.models import User, Location, location_user
from app.db.models import Product
#from flask_mail import Message

product = Blueprint('product', __name__, template_folder='templates')

@product.route('/products')
@login_required
def browse_products():
    data = Product.query.all()

    # retrieve_url = ('product.retrieve_user', [('user_id', ':id')])
    # edit_url = ('product.edit_user', [('user_id', ':id')])
    # add_url = url_for('product.add_user')
    # delete_url = ('product.delete_user', [('user_id', ':id')])

    current_app.logger.info("Browse page loading")

    return render_template('view_product.html', data=data, product=Product, record_type="Products")
