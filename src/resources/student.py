from flask_restful import Resource
from flask import request, jsonify


class Student(Resource):
    # Represents an abstract RESTful resource
    # every resource must inherit from Resource class
    # like (APIView) in django rest framework

    def get(self, name):
        return {"name": name}

    def post(self, name=None):
        return jsonify(student=request.get_json())

    def put(self, name=None):
        return "update nagah"

    def delete(self, name=None):
        return "delete nagah"
