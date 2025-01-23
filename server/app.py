#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():

    articles = db.session.get(Article,id)
    return make_response([article.to_dict() for article in articles])

@app.route('/articles/<int:id>')
def show_article(id):

    session['page_views'] = session.get('page_views',0)
    session['page_views'] += 1

    if session['page_views'] > 3:
        return jsonify({'message': 'Maximum pageview limit reached'}),401
    article = db.session.get(Article,id)
    if not article:
        return make_response({'message':'Article not found'},404)
    return make_response(article.to_dict(), 200)


if __name__ == '__main__':
    app.run(port=5555)
