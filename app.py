from flask import Flask, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from database import db
from forms import ClienteForm
from models import Cliente

app = Flask(__name__)
#Configuramos la Base de Datos.
USER_DB = 'Usuario de tu base de datos'
PASS_DB = 'Contraseña'
URL_DB = 'localhost'
NAME_DB = 'Nombre de la base de datos'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Inicialización del objeto db de sqalchemy
#db = SQLAlchemy(app)
db.init_app(app)

#Configurar flask-migrate
migrate = Migrate()
migrate.init_app(app, db)

#configuración de flask-wtf
app.config['SECRET_KEY'] = 'destroymaster123'

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def inicio():
    cliente = Cliente()
    clienteForm = ClienteForm(request.form)

    if request.method == 'POST' and clienteForm.validate_on_submit():
        clienteForm.populate_obj(cliente)
        app.logger.debug(f'Cliente a insertar: {cliente}')
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente agregado con éxito.', 'success')
        return redirect(url_for('inicio'))

    clientes = Cliente.query.order_by('id')
    cantidad_clientes = Cliente.query.count()
    app.logger.debug(f'Listado de clientes: {clientes}')
    app.logger.debug(f'Cantidad de clientes: {cantidad_clientes}')
    return render_template('index.html', clientes=clientes, cantidad_clientes=cantidad_clientes, forma=clienteForm)


@app.route('/ver/<int:id>')
def ver_detalle(id):
    cliente = Cliente.query.get_or_404(id)
    app.logger.debug(f'Cliente recuperado: {cliente}')
    return render_template('detalle.html', cliente=cliente)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cliente = Cliente.query.get_or_404(id)
    clienteForm = ClienteForm(obj=cliente)
    if request.method == 'POST' and clienteForm.validate_on_submit():
        clienteForm.populate_obj(cliente)
        db.session.commit()
        flash('Cliente editado con éxito.', 'success')
        return redirect(url_for('inicio'))
    return render_template('editar.html', forma=clienteForm)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    cliente = Cliente.query.get_or_404(id)
    app.logger.debug(f'Cliente a eliminar{cliente}')
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True) #$env:FLASK_DEBUG = "1"
