import os
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import requests

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://z:21-Pilots@ds131698.mlab.com:31698/flask_assignment"
mongo = PyMongo(app)
api = Api(app)

todos = {}
notifi = {}

class TodoSimple(Resource):
    def get(self, todo_id):
        tasks = mongo.db.todo_tbl.find()
        tasklist = {}
        i=0
        for task in tasks:
            tasklist[i] = {
                "id": str(task['_id']),
                "title": task['title'],
                "status": task['status']
            }
            i += 1
        return jsonify(tasklist)

    def post(self, todo_id):
        mongo.db.todo_tbl.insert({'title': str(request.form['data']), 'status': 'Incomplete'})
        notifi["Status"] = "Done"
        return jsonify(notifi)


    def put(self, todo_id):
        updateTask = mongo.db.todo_tbl.find_one({'_id': ObjectId(request.form['data'])})
        updateTask['status'] = 'Completed'
        mongo.db.todo_tbl.save(updateTask)
        return "Done"

    def delete(self, todo_id):
        mongo.db.todo_tbl.delete_one({'_id': ObjectId(request.form['data'])})
        return "Done"


api.add_resource(TodoSimple, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=95, debug=True)
    
    