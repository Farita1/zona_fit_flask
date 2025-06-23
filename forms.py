from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired


# Formulario para agregar clientes
class ClienteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    membresia = IntegerField('Membresía', validators=[DataRequired()])
    enviar = SubmitField('Enviar')
