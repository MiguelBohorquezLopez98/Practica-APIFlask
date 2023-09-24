from flask import jsonify, request
from flask_restful import Resource, Api

from . import private_bp
from .models import Course
from .schemas import CourseSchema

api = Api(private_bp)
course_schema = CourseSchema()

class CourseResource(Resource):

    def get(self):
        courses = Course.get_all()
        response = course_schema.dump(courses, many=True)
        return response
    
    def post(self):
        data = request.get_json()
        professor = data["professor"]
        title = data["title"]
        description = data["description"]
        url = data["url"]

        course = Course(professor=professor, title=title, description=description, url=url)
        course.save()
        return jsonify(title=course.title, professor=course.professor, id=course.id)
    
    def put(self, id):
        data = request.get_json()
        course = Course.get_by_id(id)
        course.professor = data["professor"]
        course.title = data["title"]
        course.description = data["description"]
        course.url = data["url"]
        course.save()
        response = course_schema.dump(course)
        return response
    
    def delete(self, id):
        course = Course.get_by_id(id)
        course.delete()
        return {"msg": "Deleting"}

api.add_resource(CourseResource, '/')
api.add_resource(CourseResource, '/course/<id>', endpoint="course")