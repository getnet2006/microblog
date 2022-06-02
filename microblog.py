from app import db, create_app
from app.models import User, Post, Message, Notification

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message, 'Notification': Notification}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
else:
    gunicorn_app = create_app()