import os
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import json
import requests

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

todos = {}
notifi = {}

class tbl_task_detail(db.Model):
    __tablename__ = 'tbl_task_detail'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    status = db.Column(db.String(20))

    def __repr__(self):
        return '<Role %r>' % self.name


class TodoSimple(Resource):
    def get(self, todo_id):
        taskList = {}
        tasks = tbl_task_detail.query.all()
        for task in tasks:
            taskList[task.id] = {
                "id": task.id,
                "title": task.title,
                "status": task.status
            }
        return jsonify(taskList)

    def post(self, todo_id):
        result = request.form['data']
        task_row = tbl_task_detail(title=result, status='Incomplete')
        db.session.add(task_row)
        db.session.commit()
        notifi["Status"] = "Done"
        return jsonify(notifi)


    def put(self, todo_id):
        update_task = tbl_task_detail.query.filter_by(id=request.form['data']).first()
        update_task.status = 'Completed'
        db.session.commit()
        notifi["Status"] = "Done"
        return jsonify(notifi)

    def delete(self, todo_id):
        db.session.delete(tbl_task_detail.query.filter_by(id=request.form['data']).first())
        db.session.commit()
        notifi["Status"] = "Done"
        return jsonify(notifi)


api.add_resource(TodoSimple, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80, debug=True)
    