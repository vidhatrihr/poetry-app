from flask import Flask, render_template, request
from functools import lru_cache
import requests

app = Flask(__name__)


@lru_cache
def get_json(url):
  return requests.get(url).json()


@app.route('/')
def index():
  data = get_json('https://poetrydb.org/author')
  return render_template('index.html', data=data)


@app.route('/search')
def search():
  """ http://localhost:5000/search?title=... """
  title = request.args.get('title')
  data = get_json(f'https://poetrydb.org/title/{title}/author,title')
  error = False
  if type(data) == dict:
    error = True
  return render_template('search.html', title=title, data=data, error=error)


@app.route('/titles/<author>')
def titles(author):
  data = get_json(f'https://poetrydb.org/author/{author}/title')
  return render_template('titles.html', author=author, data=data)


@app.route('/read/<author>/<title>')
def read(author, title):
  data = get_json(f'https://poetrydb.org/author,title/{author}:abs;{title}:abs')
  go_back = request.args.get('go_back', f'/titles/{author}')
  return render_template('read.html', author=author, title=title, poetry=data[0], go_back=go_back)


if __name__ == '__main__':
  app.run(debug=True)
