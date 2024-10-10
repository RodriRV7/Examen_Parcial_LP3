from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.historiaclinica.HistoriaClinicaDao import HistoriaClinicaDao

historia_clinica_api = Blueprint('historia_clinica_api', __name__)

# Trae todas las historias clínicas
@historia_clinica_api.route('/historias_clinicas', methods=['GET'])
def getHistorias():
    historia_clinica_dao = HistoriaClinicaDao()

    try:
        historias = historia_clinica_dao.getHistorias()

        return jsonify({
            'success': True,
            'data': historias,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las historias clínicas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Obtiene una historia clínica por ID
@historia_clinica_api.route('/historias_clinicas/<int:historia_id>', methods=['GET'])
def getHistoria(historia_id):
    historia_clinica_dao = HistoriaClinicaDao()

    try:
        historia = historia_clinica_dao.getHistoriaById(historia_id)

        if historia:
            return jsonify({
                'success': True,
                'data': historia,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la historia clínica con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener historia clínica: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva historia clínica
@historia_clinica_api.route('/historias_clinicas', methods=['POST'])
def addHistoria():
    data = request.get_json()
    historia_clinica_dao = HistoriaClinicaDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['paciente_id', 'descripcion', 'fecha']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        paciente_id = data['paciente_id']
        descripcion = data['descripcion']
        fecha = data['fecha']
        historia_id = historia_clinica_dao.guardarHistoria(paciente_id, descripcion, fecha)

        if historia_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': historia_id, 'paciente_id': paciente_id, 'descripcion': descripcion, 'fecha': fecha},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar la historia clínica. Consulte con el administrador.'}), 500

    except Exception as e:
        app.logger.error(f"Error al agregar historia clínica: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualiza una historia clínica
@historia_clinica_api.route('/historias_clinicas/<int:historia_id>', methods=['PUT'])
def updateHistoria(historia_id):
    data = request.get_json()
    historia_clinica_dao = HistoriaClinicaDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['paciente_id', 'descripcion', 'fecha']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    paciente_id = data['paciente_id']
    descripcion = data['descripcion']
    fecha = data['fecha']

    try:
        if historia_clinica_dao.updateHistoria(historia_id, paciente_id, descripcion, fecha):
            return jsonify({
                'success': True,
                'data': {'id': historia_id, 'paciente_id': paciente_id, 'descripcion': descripcion, 'fecha': fecha},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la historia clínica con el ID proporcionado o no se pudo actualizar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al actualizar historia clínica: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Elimina una historia clínica
@historia_clinica_api.route('/historias_clinicas/<int:historia_id>', methods=['DELETE'])
def deleteHistoria(historia_id):
    historia_clinica_dao = HistoriaClinicaDao()

    try:
        if historia_clinica_dao.deleteHistoria(historia_id):
            return jsonify({
                'success': True,
                'mensaje': f'Historia clínica con ID {historia_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la historia clínica con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar historia clínica: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
