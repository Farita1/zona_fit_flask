#Creamos un modelo, como en Django:
from app import db


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250))
    apellido = db.Column(db.String(250))
    membresia = db.Column(db.Integer)
    
    def __str__(self):
        return (
            f'Cliente #{self.id}, '
            f'Nombre: {self.nombre}, '
            f'Apellido: {self.apellido}, '
            f'Email: {self.membresia}'
        )
