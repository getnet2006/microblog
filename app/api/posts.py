from email.quoprimime import body_check
from flask import request, jsonify, url_for
from app.api import bp
from app.api.errors import bad_request
from app.models import Post, User
from app.api.tokens import token_auth
from app import db


@bp.get('/posts')
@token_auth.login_required
def get_posts():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Post.to_collection_dict(Post.query, page, per_page, 'api.get_posts')
    return jsonify(data)

@bp.get('/posts/<int:id>')
@token_auth.login_required
def get_post(id):
    return jsonify(Post.query.get_or_404(id).to_dict())

@bp.get('/posts_by/<int:id>')
@token_auth.login_required
def post_by_self(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Post.to_collection_dict(user.posts, page, per_page, 'api.post_by_self', id=id)
    return jsonify(data)

@bp.get('/followed_posts/<int:id>')
@token_auth.login_required
def followed_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    resource = user.only_followed_posts()
    data = Post.to_collection_dict(resource, page, per_page, 'api.followed_posts', id=id)
    return jsonify(data)

@bp.post('/posts/<int:id>')
@token_auth.login_required
def create_post(id):
    if token_auth.current_user().id != id:
        return bad_request('You can only create posts for yourself.')
    data = request.get_json() or ()
    if 'body' not in data:
        return bad_request('must include body field')
    post = Post(body = data['body'], author = User.query.get_or_404(id))
    db.session.add(post)
    db.session.commit()
    response = jsonify(post.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_post', id=post.id)
    return response