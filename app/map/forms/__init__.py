from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *

class loc_edit_form(FlaskForm):
    population = TextAreaField('Population', description="Please add the info for population")

    submit = SubmitField()

class csv_upload(FlaskForm):
    file = FileField()
    submit = SubmitField()