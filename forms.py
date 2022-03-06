from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField, StringField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields import DateField, TimeField


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