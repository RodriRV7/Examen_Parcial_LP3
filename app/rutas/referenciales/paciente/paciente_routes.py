from flask import Blueprint, render_template

pacimod = Blueprint('paciente', __name__, template_folder='templates')

@pacimod.route('/paciente-index')
def pacienteIndex():
    return render_template('paciente-index.html')