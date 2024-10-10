from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.medico.MedicoDao import MedicoDao  # Asumiendo que el MedicoDao está en esta ruta

medicoapi = Blueprint('medicoapi', __name__)

# Obtener todos los médicos
@medicoapi.route('/medicos', methods=['GET'])
def getMedicos():
    medicodao = MedicoDao()

    try:
        medicos = medicodao.getMedicos()

        return jsonify({
            'success': True,
            'data': medicos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los médicos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Obtener un médico por ID
@medicoapi.route('/medicos/<int:medico_id>', methods=['GET'])
def getMedico(medico_id):
    medicodao = MedicoDao()

    try:
        medico = medicodao.getMedicoById(medico_id)

        if medico:
            return jsonify({
                'success': True,
                'data': medico,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el médico con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener médico: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agregar un nuevo médico
@medicoapi.route('/medicos', methods=['POST'])
def addMedico():
    data = request.get_json()
    medicodao = MedicoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'especialidad', 'telefono', 'email']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        nombre = data['nombre']
        especialidad = data['especialidad']
        telefono = data['telefono']
        email = data['email']
        medico_id = medicodao.guardarMedico(nombre, especialidad, telefono, email)

        if medico_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': medico_id, 'nombre': nombre, 'especialidad': especialidad, 'telefono': telefono, 'email': email},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el médico. Consulte con el administrador.'}), 500

    except Exception as e:
        app.logger.error(f"Error al agregar médico: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualizar un médico por ID
@medicoapi.route('/medicos/<int:medico_id>', methods=['PUT'])
def updateMedico(medico_id):
    data = request.get_json()
    medicodao = MedicoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'especialidad', 'telefono', 'email']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    nombre = data['nombre']
    especialidad = data['especialidad']
    telefono = data['telefono']
    email = data['email']

    try:
        if medicodao.updateMedico(medico_id, nombre, especialidad, telefono, email):
            return jsonify({
                'success': True,
                'data': {'id': medico_id, 'nombre': nombre, 'especialidad': especialidad, 'telefono': telefono, 'email': email},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el médico con el ID proporcionado o no se pudo actualizar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al actualizar médico: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Eliminar un médico por ID
@medicoapi.route('/medicos/<int:medico_id>', methods=['DELETE'])
def deleteMedico(medico_id):
    medicodao = MedicoDao()

    try:
        if medicodao.deleteMedico(medico_id):
            return jsonify({
                'success': True,
                'mensaje': f'Médico con ID {medico_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el médico con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar médico: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
