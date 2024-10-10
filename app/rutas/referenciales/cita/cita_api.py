from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.cita.CitaDao import CitaDao

cita_api = Blueprint('cita_api', __name__)

# Trae todas las citas
@cita_api.route('/citas', methods=['GET'])
def getCitas():
    cita_dao = CitaDao()

    try:
        citas = cita_dao.getCitas()

        return jsonify({
            'success': True,
            'data': citas,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las citas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@cita_api.route('/citas/<int:cita_id>', methods=['GET'])
def getCita(cita_id):
    cita_dao = CitaDao()

    try:
        cita = cita_dao.getCitaById(cita_id)

        if cita:
            return jsonify({
                'success': True,
                'data': cita,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la cita con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener cita: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva cita
@cita_api.route('/citas', methods=['POST'])
def addCita():
    data = request.get_json()
    cita_dao = CitaDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre_paciente', 'nombre_medico', 'fecha', 'hora', 'motivo']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        nombre_paciente = data['nombre_paciente'].upper()
        nombre_medico = data['nombre_medico'].upper()
        fecha = data['fecha']
        hora = data['hora']
        motivo = data['motivo'].upper()

        cita_id = cita_dao.guardarCita(nombre_paciente, nombre_medico, fecha, hora, motivo)
        if cita_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': cita_id, 'nombre_paciente': nombre_paciente, 'nombre_medico': nombre_medico, 'fecha': fecha, 'hora': hora, 'motivo': motivo},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar la cita. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar cita: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@cita_api.route('/citas/<int:cita_id>', methods=['PUT'])
def updateCita(cita_id):
    data = request.get_json()
    cita_dao = CitaDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre_paciente', 'nombre_medico', 'fecha', 'hora', 'motivo']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    nombre_paciente = data['nombre_paciente']
    nombre_medico = data['nombre_medico']
    fecha = data['fecha']
    hora = data['hora']
    motivo = data['motivo']

    try:
        if cita_dao.updateCita(cita_id, nombre_paciente.upper(), nombre_medico.upper(), fecha, hora, motivo.upper()):
            return jsonify({
                'success': True,
                'data': {'id': cita_id, 'nombre_paciente': nombre_paciente, 'nombre_medico': nombre_medico, 'fecha': fecha, 'hora': hora, 'motivo': motivo},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la cita con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar cita: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@cita_api.route('/citas/<int:cita_id>', methods=['DELETE'])
def deleteCita(cita_id):
    cita_dao = CitaDao()

    try:
        # Usar el retorno de eliminarCita para determinar el éxito
        if cita_dao.deleteCita(cita_id):
            return jsonify({
                'success': True,
                'mensaje': f'Cita con ID {cita_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la cita con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar cita: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
