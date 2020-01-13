# compose_flask/app.py
from flask import Flask
from redis import Redis
from flask_sqlalchemy import SQLAlchemy
from config import DB_URL

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def hello():
    redis.incr('hits')
    return 'This Compose/Flask demo has been viewed %s time(s).' % redis.get('hits')


@app.route('/mysql/<username>')
def mysql_test(username):
    db.create_all()
    admin = User(username=str(username), email='admin@example.com')
    db.session.add(admin)
    db.session.commit()
    res = User.query.filter_by(username=username).first()

    return 'test through, user name is {}'.format(res.username)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)