from flask import Flask

app = Flask(__name__)

# importar referenciales
from app.rutas.referenciales.ciudad.ciudad_routes import ciumod
from app.rutas.referenciales.pais.pais_routes import paimod
from app.rutas.referenciales.medico.medico_routes import medmod
from app.rutas.referenciales.paciente.paciente_routes import pacimod
from app.rutas.referenciales.cita.cita_routes import citamod
from app.rutas.referenciales.receta.receta_routes import recmod
from app.rutas.referenciales.diagnostico.diagnostico_routes import diagmod
from app.rutas.referenciales.tratamiento.tratamiento_routes import tramod
from app.rutas.referenciales.historiaclinica.historiaclinica_routes import histmod
from app.rutas.referenciales.cliente.cliente_routes import climod
from app.rutas.referenciales.producto.producto_routes import prodmod




# registrar referenciales
modulo0 = '/referenciales'
app.register_blueprint(ciumod, url_prefix=f'{modulo0}/ciudad')
app.register_blueprint(paimod, url_prefix=f'{modulo0}/pais')
app.register_blueprint(medmod, url_prefix=f'{modulo0}/medico')
app.register_blueprint(pacimod, url_prefix=f'{modulo0}/paciente')
app.register_blueprint(citamod, url_prefix=f'{modulo0}/cita')
app.register_blueprint(recmod, url_prefix=f'{modulo0}/receta')
app.register_blueprint(diagmod, url_prefix=f'{modulo0}/diagnostico')
app.register_blueprint(tramod, url_prefix=f'{modulo0}/tratamiento')
app.register_blueprint(histmod, url_prefix=f'{modulo0}/historiaclinica')
app.register_blueprint(climod, url_prefix=f'{modulo0}/cliente')
app.register_blueprint(prodmod, url_prefix=f'{modulo0}/producto')



from app.rutas.referenciales.ciudad.ciudad_api import ciuapi
from app.rutas.referenciales.pais.pais_api import paisapi
from app.rutas.referenciales.medico.medico_api import medicoapi
from app.rutas.referenciales.paciente.paciente_api import paciente_api
from app.rutas.referenciales.cita.cita_api import cita_api
from app.rutas.referenciales.receta.receta_api import receta_api
from app.rutas.referenciales.diagnostico.diagnostico_api import diagapi
from app.rutas.referenciales.tratamiento.tratamiento_api import tratamiento_api
from app.rutas.referenciales.historiaclinica.historiaclinica_api import historia_clinica_api
from app.rutas.referenciales.cliente.cliente_api import cliente_api
from app.rutas.referenciales.producto.producto_api import productoapi


# APIS v1
version1 = '/api/v1'
app.register_blueprint(ciuapi, url_prefix=version1)
app.register_blueprint(paisapi, url_prefix=version1)
app.register_blueprint(medicoapi, url_prefix=version1)
app.register_blueprint(paciente_api, url_prefix=version1)
app.register_blueprint(cita_api, url_prefix=version1)
app.register_blueprint(receta_api, url_prefix=version1)
app.register_blueprint(diagapi, url_prefix=version1)
app.register_blueprint(tratamiento_api, url_prefix=version1)
app.register_blueprint(cliente_api, url_prefix=version1)
app.register_blueprint(productoapi, url_prefix=version1)
