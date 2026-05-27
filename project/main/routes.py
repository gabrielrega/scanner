from flask import Blueprint, render_template
import config

main_bp = Blueprint('main_bp', __name__,
                    template_folder='../templates',
                    static_folder='../static')

@main_bp.route('/')
def index():
    return render_template('index.html', search_terms=config.SEARCH_TERMS)

@main_bp.route('/favicon.ico')
def favicon():
    return '', 204
