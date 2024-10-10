from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.paciente.PacienteDao import PacienteDao

paciente_api = Blueprint('paciente_api', __name__)

# Trae todos los pacientes
@paciente_api.route('/pacientes', methods=['GET'])
def getPacientes():
    paciente_dao = PacienteDao()

    try:
        pacientes = paciente_dao.getPacientes()

        return jsonify({
            'success': True,
            'data': pacientes,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los pacientes: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@paciente_api.route('/pacientes/<int:paciente_id>', methods=['GET'])
def getPaciente(paciente_id):
    paciente_dao = PacienteDao()

    try:
        paciente = paciente_dao.getPacienteById(paciente_id)

        if paciente:
            return jsonify({
                'success': True,
                'data': paciente,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el paciente con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener paciente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo paciente
@paciente_api.route('/pacientes', methods=['POST'])
def addPaciente():
    data = request.get_json()
    paciente_dao = PacienteDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'fecha_nacimiento', 'telefono', 'email']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        nombre = data['nombre']
        fecha_nacimiento = data['fecha_nacimiento']
        telefono = data['telefono']
        email = data['email']
        paciente_id = paciente_dao.guardarPaciente(nombre, fecha_nacimiento, telefono, email)

        if paciente_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': paciente_id, 'nombre': nombre, 'fecha_nacimiento': fecha_nacimiento, 'telefono': telefono, 'email': email},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el paciente. Consulte con el administrador.'}), 500

    except Exception as e:
        app.logger.error(f"Error al agregar paciente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@paciente_api.route('/pacientes/<int:paciente_id>', methods=['PUT'])
def updatePaciente(paciente_id):
    data = request.get_json()
    paciente_dao = PacienteDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'fecha_nacimiento', 'telefono', 'email']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    nombre = data['nombre']
    fecha_nacimiento = data['fecha_nacimiento']
    telefono = data['telefono']
    email = data['email']

    try:
        if paciente_dao.updatePaciente(paciente_id, nombre, fecha_nacimiento, telefono, email):
            return jsonify({
                'success': True,
                'data': {'id': paciente_id, 'nombre': nombre, 'fecha_nacimiento': fecha_nacimiento, 'telefono': telefono, 'email': email},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el paciente con el ID proporcionado o no se pudo actualizar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al actualizar paciente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@paciente_api.route('/pacientes/<int:paciente_id>', methods=['DELETE'])
def deletePaciente(paciente_id):
    paciente_dao = PacienteDao()

    try:
        if paciente_dao.deletePaciente(paciente_id):
            return jsonify({
                'success': True,
                'mensaje': f'Paciente con ID {paciente_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el paciente con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar paciente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
