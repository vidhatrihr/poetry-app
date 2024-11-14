from flask import Flask, render_template
import requests

app = Flask(__name__)


@app.route('/')
def index():
  data = requests.get('https://poetrydb.org/author').json()
  return render_template('index.html', data=data)


@app.route('/titles/<author>')
def titles(author):
  data = requests.get(f'https://poetrydb.org/author/{author}/title').json()
  return render_template('titles.html', author=author, data=data)


@app.route('/read/<author>/<title>')
def read(author, title):
  data = requests.get(f'https://poetrydb.org/author,title/{author}:abs;{title}:abs').json()
  return render_template('read.html', author=author, title=title, poetry=data[0])


if __name__ == '__main__':
  app.run(debug=True)
