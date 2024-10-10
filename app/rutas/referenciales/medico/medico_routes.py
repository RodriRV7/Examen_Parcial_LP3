from flask import Blueprint, render_template

medmod = Blueprint('medico', __name__, template_folder='templates')

@medmod.route('/medico-index')
def medicoIndex():
    return render_template('medico-index.html')