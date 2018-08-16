import os
from flask import Flask, render_template, redirect, request, url_for, jsonify
from requests import put, get, post, delete
# from flask_pymongo import PyMongo
# from bson.json_util import dumps
# from bson.objectid import ObjectId

app = Flask(__name__)




@app.route('/')
def index():
    tasks =get('http://127.0.0.1:95/todo1').json()
    return render_template('mongo_index.html', tasks = tasks)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        status = post('http://127.0.0.1:95/todo1', data={'data':str(request.form.getlist('task')[0])}).json()
    if status["Status"] == "Done":
        return redirect(url_for('index'))
    else:
        return "Sorry network Problem"

@app.route('/deletes/<t_id>')
def deletes(t_id):
    if t_id == 0:
        return redirect(url_for('index'))
    status = delete('http://127.0.0.1:95/todo1', data={'data':str(t_id)}).json()
    if status == "Done":
        return redirect(url_for('index'))
    else:
        return "Sorry network Problem"

@app.route('/done/<t_id>')
def done(t_id):
    if t_id == 0:
        return redirect(url_for('index'))
    status = put('http://127.0.0.1:95/todo1', data={'data':str(t_id)}).json()
    if status == "Done":
        return redirect(url_for('index'))
    else:
        return "Sorry network Problem"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=96, debug=True)

