import email
from os import abort
from flask import jsonify, request, url_for
from app.api import bp
from app.models import User, Post
from app.api.errors import bad_request
from app import db
from app.api.auth import token_auth


@bp.get('/users/<int:id>')
@token_auth.login_required
def get_user(id):
    email = request.args.get('email', False)
    return jsonify(User.query.get_or_404(id).to_dict(email))

@bp.get('/users')
@token_auth.login_required
def get_users():
    email = request.args.get('email', False)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 100, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users', email=email)
    return jsonify(data)

@bp.get('/users/<int:id>/followers')
@token_auth.login_required
def get_followers(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(user.followers, page, per_page, 'api.get_followers', id=id)
    return jsonify(data)

@bp.get('/users/<int:id>/followed')
@token_auth.login_required
def get_followed(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(user.followed, page, per_page, 'api.get_followed', id=id)
    return jsonify(data)

@bp.post('/users')
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@bp.put('/users/<int:id>')
@token_auth.login_required
def update_user(id):
    if token_auth.current_user().id != id:
        return bad_request('Only the user can update their own profile')
    data = request.get_json() or {}
    user = User.query.get_or_404(id)
    if 'username' in data and data['username'] != user.username and User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict(include_email=True))

