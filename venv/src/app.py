from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS 
from werkzeug.utils import secure_filename
import os


# Configurar la aplicación Flask
app = Flask(__name__)

# Crear una instancia de Flask
app = Flask(__name__)
CORS(app)

# Configurar la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/videojuegos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'ruta/a/la/carpeta/de/imagenes'  # Ajusta la ruta adecuada

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Videojuego(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Float, nullable=True)
    requisitos_minimos = db.Column(db.Text, nullable=True)
    requisitos_recomendados = db.Column(db.Text, nullable=True)

# Ruta para obtener todos los videojuegos
@app.route('/videojuegos', methods=['GET'])
def get_videojuegos():
    videojuegos = Videojuego.query.all()
    return jsonify([v.to_dict() for v in videojuegos])

# Ruta para crear un nuevo videojuego
@app.route('/videojuegos', methods=['POST'])
def create_videojuego():
    try:
        data = request.json

        # Validar los campos requeridos
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        requisitos_minimos = data.get('requisitos_minimos', '')
        requisitos_recomendados = data.get('requisitos_recomendados', '')

        # Validar el campo precio
        precio = data.get('precio')
        if precio:
            precio = float(precio)
        else:
            precio = None  # O asigna un valor predeterminado según tu lógica de negocio

        # Crear un nuevo objeto Videojuego
        new_videojuego = Videojuego(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            requisitos_minimos=requisitos_minimos,
            requisitos_recomendados=requisitos_recomendados
        )

        # Guardar en la base de datos
        db.session.add(new_videojuego)
        db.session.commit()

        return jsonify(new_videojuego.to_dict()), 201
    except Exception as e:
        print(str(e))  # Imprime el mensaje de error en la consola de Flask para depuración
        return jsonify({'error': str(e)}), 500
# Ruta para obtener un videojuego por ID
@app.route('/videojuegos/<int:id>', methods=['GET'])
def get_videojuego(id):
    videojuego = Videojuego.query.get_or_404(id)
    return jsonify(videojuego.to_dict())

# Ruta para actualizar un videojuego por ID
@app.route('/videojuegos/<int:id>', methods=['PUT'])
def update_videojuego(id):
    data = request.get_json()
    videojuego = Videojuego.query.get_or_404(id)
    videojuego.nombre = data['nombre']
    videojuego.descripcion = data['descripcion']
    db.session.commit()
    return jsonify(videojuego.to_dict())

# Ruta para eliminar un videojuego por ID
@app.route('/videojuegos/<int:id>', methods=['DELETE'])
def delete_videojuego(id):
    videojuego = Videojuego.query.get_or_404(id)
    db.session.delete(videojuego)
    db.session.commit()
    return '', 204

# Método para convertir el objeto Videojuego a diccionario
def to_dict(self):
    return {
        'id': self.id,
        'nombre': self.nombre,
        'descripcion': self.descripcion,
        'precio': self.precio,
        'requisitos_minimos': self.requisitos_minimos,
        'requisitos_recomendados': self.requisitos_recomendados
    }

Videojuego.to_dict = to_dict

if __name__ == '__main__':
    app.run(debug=True)
