from flask import Blueprint, render_template

histmod = Blueprint('historiaclinica', __name__, template_folder='templates')

@histmod.route('/historiaclinica-index')
def historiaclinicaIndex():
    return render_template('historiaclinica-index.html')