from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.cliente.ClienteDao import ClienteDao

cliente_api = Blueprint('cliente_api', __name__)

# Trae todos los clientes
@cliente_api.route('/clientes', methods=['GET'])
def getClientes():
    cliente_dao = ClienteDao()

    try:
        clientes = cliente_dao.getClientes()

        return jsonify({
            'success': True,
            'data': clientes,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los clientes: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@cliente_api.route('/clientes/<int:cliente_id>', methods=['GET'])
def getCliente(cliente_id):
    cliente_dao = ClienteDao()

    try:
        cliente = cliente_dao.getClienteById(cliente_id)

        if cliente:
            return jsonify({
                'success': True,
                'data': cliente,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el cliente con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener cliente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo cliente
@cliente_api.route('/clientes', methods=['POST'])
def addCliente():
    data = request.get_json()
    cliente_dao = ClienteDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'direccion', 'telefono', 'email']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        nombre = data['nombre'].upper()
        direccion = data['direccion']
        telefono = data['telefono']
        email = data['email']

        cliente_id = cliente_dao.guardarCliente(nombre, direccion, telefono, email)
        if cliente_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': cliente_id, 'nombre': nombre, 'direccion': direccion, 'telefono': telefono, 'email': email},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el cliente. Consulte con el administrador.'
            }), 500

    except Exception as e:
        app.logger.error(f"Error al agregar cliente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@cliente_api.route('/clientes/<int:cliente_id>', methods=['PUT'])
def updateCliente(cliente_id):
    data = request.get_json()
    cliente_dao = ClienteDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'direccion', 'telefono', 'email']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    nombre = data['nombre'].upper()
    direccion = data['direccion']
    telefono = data['telefono']
    email = data['email']

    try:
        if cliente_dao.updateCliente(cliente_id, nombre, direccion, telefono, email):
            return jsonify({
                'success': True,
                'data': {'id': cliente_id, 'nombre': nombre, 'direccion': direccion, 'telefono': telefono, 'email': email},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el cliente con el ID proporcionado o no se pudo actualizar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al actualizar cliente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@cliente_api.route('/clientes/<int:cliente_id>', methods=['DELETE'])
def deleteCliente(cliente_id):
    cliente_dao = ClienteDao()

    try:
        if cliente_dao.deleteCliente(cliente_id):
            return jsonify({
                'success': True,
                'mensaje': f'Cliente con ID {cliente_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el cliente con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar cliente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
