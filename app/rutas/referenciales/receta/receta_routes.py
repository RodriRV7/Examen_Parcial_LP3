from flask import Blueprint, render_template

recmod = Blueprint('receta', __name__, template_folder='templates')

@recmod.route('/receta-index')
def recetaIndex():
    return render_template('receta-index.html')