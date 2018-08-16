import os
from flask import Flask, render_template, redirect, request, url_for
from requests import put, get, post, delete

app = Flask(__name__)


@app.route('/')
def index():
    # tasks = tbl_task_detail.query.all()
    tasks =get('http://127.0.0.1:80/todo1').json()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        status = post('http://127.0.0.1:80/todo1', data={'data':str(request.form.getlist('task')[0])}).json()
    if status["Status"] == "Done":
        return redirect(url_for('index'))
    else:
        return "Sorry network Problem"
    return redirect(url_for('index'))


@app.route('/deletes/<t_id>')
def deletes(t_id):
    if t_id == 0:
        return redirect(url_for('index'))
    status = delete('http://127.0.0.1:80/todo1', data={'data':str(t_id)}).json()
    if status["Status"] == "Done":
        return redirect(url_for('index'))
    else:
        return "Sorry network Problem"


@app.route('/done/<t_id>')
def done(t_id):
    if t_id == 0:
        return redirect(url_for('index'))
    status = put('http://127.0.0.1:80/todo1', data={'data':str(t_id)}).json()
    if status["Status"] == "Done":
        return redirect(url_for('index'))
    else:
        return "Sorry network Problem"


if __name__ == '__main__':
    app.run(debug=True)
