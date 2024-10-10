from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.pais.PaisDao import PaisDao

paisapi = Blueprint('paisapi', __name__)

# Trae todos los países
@paisapi.route('/paises', methods=['GET'])
def getPaises():
    paisdao = PaisDao()

    try:
        paises = paisdao.getPaises()

        return jsonify({
            'success': True,
            'data': paises,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los países: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


@paisapi.route('/paises/<int:pais_id>', methods=['GET'])
def getPais(pais_id):
    paisdao = PaisDao()

    try:
        pais = paisdao.getPaisById(pais_id)

        if pais:
            return jsonify({
                'success': True,
                'data': pais,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el país con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener país: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


# Agrega un nuevo país
@paisapi.route('/paises', methods=['POST'])
def addPais():
    data = request.get_json()
    paisdao = PaisDao()

    # Validar que el JSON no esté vacío y tenga la propiedad 'descripcion'
    if 'descripcion' not in data or not data['descripcion'].strip():
        return jsonify({
            'success': False,
            'error': 'El campo "descripcion" es obligatorio y no puede estar vacío.'
        }), 400

    try:
        descripcion = data['descripcion'].upper()
        pais_id = paisdao.guardarPais(descripcion)
        
        if pais_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': pais_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el país. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar país: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


@paisapi.route('/paises/<int:pais_id>', methods=['PUT'])
def updatePais(pais_id):
    data = request.get_json()
    paisdao = PaisDao()

    # Validar que el JSON no esté vacío y tenga la propiedad 'descripcion'
    if 'descripcion' not in data or not data['descripcion'].strip():
        return jsonify({
            'success': False,
            'error': 'El campo "descripcion" es obligatorio y no puede estar vacío.'
        }), 400

    descripcion = data['descripcion']

    try:
        if paisdao.updatePais(pais_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': pais_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el país con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar país: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


@paisapi.route('/paises/<int:pais_id>', methods=['DELETE'])
def deletePais(pais_id):
    paisdao = PaisDao()

    try:
        if paisdao.deletePais(pais_id):
            return jsonify({
                'success': True,
                'mensaje': f'País con ID {pais_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el país con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar país: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
