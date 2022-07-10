from flask import render_template, request, jsonify
from app import db
from app.errors import bp

def wants_json_response():
    return request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']

@bp.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        return jsonify({'error': 'not found'})
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if wants_json_response():
        return jsonify({'error': 'internal error'})
    return render_template('errors/500.html'), 500