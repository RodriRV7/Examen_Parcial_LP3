from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.receta.RecetaDao import RecetaDao

receta_api = Blueprint('receta_api', __name__)

# Obtener todas las recetas
@receta_api.route('/recetas', methods=['GET'])
def getRecetas():
    receta_dao = RecetaDao()

    try:
        recetas = receta_dao.getRecetas()

        return jsonify({
            'success': True,
            'data': recetas,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las recetas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Obtener una receta por ID
@receta_api.route('/recetas/<int:receta_id>', methods=['GET'])
def getReceta(receta_id):
    receta_dao = RecetaDao()

    try:
        receta = receta_dao.getRecetaById(receta_id)

        if receta:
            return jsonify({
                'success': True,
                'data': receta,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la receta con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener receta: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agregar una nueva receta
@receta_api.route('/recetas', methods=['POST'])
def addReceta():
    data = request.get_json()
    receta_dao = RecetaDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['paciente', 'medico', 'descripcion', 'fecha']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        paciente = data['paciente'].strip()
        medico = data['medico'].strip()
        descripcion = data['descripcion'].strip()
        fecha = data['fecha']

        receta_id = receta_dao.guardarReceta(paciente, medico, descripcion, fecha)

        if receta_id:
            return jsonify({
                'success': True,
                'data': {'id': receta_id, 'paciente': paciente, 'medico': medico, 'descripcion': descripcion, 'fecha': fecha},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar la receta. Consulte con el administrador.'
            }), 500

    except Exception as e:
        app.logger.error(f"Error al agregar receta: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualizar una receta existente
@receta_api.route('/recetas/<int:receta_id>', methods=['PUT'])
def updateReceta(receta_id):
    data = request.get_json()
    receta_dao = RecetaDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['paciente', 'medico', 'descripcion', 'fecha']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    paciente = data['paciente'].strip()
    medico = data['medico'].strip()
    descripcion = data['descripcion'].strip()
    fecha = data['fecha']

    try:
        if receta_dao.updateReceta(receta_id, paciente, medico, descripcion, fecha):
            return jsonify({
                'success': True,
                'data': {'id': receta_id, 'paciente': paciente, 'medico': medico, 'descripcion': descripcion, 'fecha': fecha},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la receta con el ID proporcionado o no se pudo actualizar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al actualizar receta: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Eliminar una receta
@receta_api.route('/recetas/<int:receta_id>', methods=['DELETE'])
def deleteReceta(receta_id):
    receta_dao = RecetaDao()

    try:
        if receta_dao.deleteReceta(receta_id):
            return jsonify({
                'success': True,
                'mensaje': f'Receta con ID {receta_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la receta con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar receta: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
