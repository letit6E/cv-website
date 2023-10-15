import sys

from flask import Flask, render_template, request, url_for, redirect

from config import SQLITE_DATABASE_NAME
from model import db, db_init, Post

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + SQLITE_DATABASE_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.app = app
db.init_app(app)


@app.route('/')
def hello_world():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('index.html', posts=posts)


@app.route('/yandex_efa2343b15c63d31.html')
def webmaster():
    return render_template('yandex_efa2343b15c63d31.html')


@app.route('/', methods=['GET', 'POST'])
def add_post():
    if request.method == "POST":
        name = request.form.get('name', type=str, default="")
        position = request.form.get('position', type=str, default="")
        text = request.form.get('text', type=str, default="")

        if any(c.isalpha() for c in name) and any(c.isalpha() for c in text):
            p = Post(name=name, position=position, text=text)
            db.session.add(p)
            db.session.commit()

    return redirect(url_for('hello_world'))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "init":
            with app.app_context():
                db_init()
                sys.exit(0)
    app.run(host='0.0.0.0', port=5000, debug=True)
