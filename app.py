import json
import sys

from flask import Flask, render_template
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'
PORT_DIR = 'portfolio'

app = Flask(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)
app.config.from_object(__name__)


@app.route('/')
def main():
    posts = [post for post in flatpages if post.path.startswith(POST_DIR)]
    posts.sort(key=lambda item: item['date'], reverse=True)

    cards = [p for p in flatpages if p.path.startswith(PORT_DIR)]
    cards.sort(key=lambda item: item['title'])

    with open('settings.txt', encoding='utf-8') as config:
        data = config.read()
        settings = json.loads(data)

    return render_template(template_name_or_list='index.html', posts=posts, cards=cards, bigheder=True, **settings)


@app.route('/posts/<name>/')
def post(name: str):
    path = '{}/{}'.format(POST_DIR, name)
    print(path)
    post = flatpages.get_or_404(path)
    return render_template(template_name_or_list='post.html', post=post)


@app.route('/portfolio/<name>/')
def card(name):
    path = '{}/{}'.format(PORT_DIR, name)
    card = flatpages.get_or_404(path)
    return render_template('card.html', card=card)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
    else:
        app.run(host='127.0.0.1', port=8000, debug=True)
