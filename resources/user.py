from flask_restful import Resource


class Foo(Resource):
	def get(self, username):
		return {'hell': username }

	def post(self):
		return {'hell': '2'}


class Foo1(Resource):
	def get(self):
		return {'hell': '3'}

	def post(self):
		return {'hell': '4'}