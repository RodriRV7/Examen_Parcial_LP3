from flask import Blueprint, render_template

tramod = Blueprint('tratamiento', __name__, template_folder='templates')

@tramod.route('/tratamiento-index')
def tratamientoIndex():
    return render_template('tratamiento-index.html')