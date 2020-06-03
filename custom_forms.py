from flask_wtf import FlaskForm
from flask_wtf.file import *
from wtforms.fields import StringField, BooleanField, FileField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

class timeSeriesForm(FlaskForm):
	#MAX LOOKBACK 8 DAYS -- Twitter API constraint
	lookback = IntegerField('Days Lookback (Max: 7 days):', validators=[DataRequired(), NumberRange(min=1, max=7)])
	daily_sample_size = IntegerField('Daily Sample Size (Max: 3000) INOP-WIP:', validators=[DataRequired(), NumberRange(min=1, max=3000)])
	submit = SubmitField('generate')



# placeholder for lat long
# placeholder for variables from evaluator that can be changed

class ipfsForm(FlaskForm):
	#lat and lon must be converted if not already to max 3 decimal places
	dataSets = [
		("chirps_05-daily", "chirps_05-daily"),
	 	("chirps_05-monthly", "chirps_05-monthly"),
	 	("chirps_25-daily", "chirps_25-daily"),
	  	("chirps_25-monthly", "chirps_25-monthly"),
	   	("cpc_us-daily", "cpc_us-daily"),
	    ("cpc_us-monthly", "cpc_us-monthly")]

	lat = StringField('Latitude', validators=[DataRequired()])
	lon = StringField('Longitude', validators=[DataRequired()])

	selectData = SelectField('Select Dataset', choices=dataSets)

	submit = SubmitField('run')