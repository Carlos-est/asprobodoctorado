from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField, StringField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields.html5 import DateField, TimeField
from wtforms.fields import html5 as h5fields
from wtforms.widgets import html5 as h5widgets

class FormForward(FlaskForm):

    fechaFloracion = DateField('Fecha de floración (belloteo, manzaneo, semana *) - (*)primera semana de floración', format='%Y-%m-%d', validators=(DataRequired(),))
    submit = SubmitField('Calcular')



class FormIndicadoresCultivo(FlaskForm):
    fechaCosecha = DateField('Fecha de última cosecha:', format='%Y-%m-%d', validators=(DataRequired(),))
    fechaFloracion = DateField('Fecha de floración (belloteo, manzaneo, semana *) - (*)primera semana de floración', format='%Y-%m-%d', validators=(DataRequired(),))


class FormBiomasa(FlaskForm):
    fechaFloracion = DateField('Fecha de floración fg (belloteo, manzaneo, semana *) - (*)primera semana de floración', format='%Y-%m-%d', validators=(DataRequired(),))

class FormPrediction(FlaskForm):
    fechaPredictionF1 = DateField('Fecha de la última fumigación correctiva', format='%Y-%m-%d', validators=(DataRequired(),))
    fechaPredictionF2 = DateField('Fecha de la última fumigación preventiva', format='%Y-%m-%d', validators=(DataRequired(),))
    fechaPredictionC = DateField('Fecha de la última limpieza realizada a la parcela', format='%Y-%m-%d', validators=(DataRequired(),))
class FormDescargar(FlaskForm):
    year = h5fields.IntegerField("Año:", widget=h5widgets.NumberInput(min=2019, max=2022), validators=(DataRequired(),))
    CantSemana = h5fields.IntegerField("Cantidad de semanas:", widget=h5widgets.NumberInput(min=1, max=52), validators=(DataRequired(),))
    NroSemana = h5fields.IntegerField("Semana del año (1-52):", widget=h5widgets.NumberInput(min=1, max=52), validators=(DataRequired(),))
    