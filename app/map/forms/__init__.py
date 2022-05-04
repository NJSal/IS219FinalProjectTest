from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *

class loc_edit_form(FlaskForm):
    population = TextAreaField('Population', description="Please add the info for population")

    submit = SubmitField()

class csv_upload(FlaskForm):
    file = FileField()
    submit = SubmitField()

class add_location_form(FlaskForm):
    title = TextAreaField('Location City', [validators.DataRequired(), ],
                          description="Location")
    longitude = TextAreaField('Longitude', [validators.DataRequired(), ],
                          description="Longitude")
    latitude = TextAreaField('Latitude', [validators.DataRequired(), ],
                          description="Latitude")
    population = TextAreaField('Population', [validators.DataRequired(), ],
                          description="Population Count")
    submit = SubmitField()
