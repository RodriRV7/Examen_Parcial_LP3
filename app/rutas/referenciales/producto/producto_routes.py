from flask import Blueprint, render_template

prodmod = Blueprint('producto', __name__, template_folder='templates')

@prodmod.route('/producto-index')
def productoIndex():
    return render_template('producto-index.html')