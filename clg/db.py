from flask import Flask, request, jsonify
from urllib.parse import quote_plus
from flask_sqlalchemy import SQLAlchemy
from clg.validate import Validate
from clg.generate import Generate
import json

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:%s@localhost/college' % quote_plus('password')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class Department(db.Model):

	__tablename__ = "department"

	id = db.Column(db.Integer, primary_key = True)
	dept_name = db.Column(db.String(100))
	budget = db.Column(db.Integer)

	student = db.relationship("Student", back_populates="department")

	def __init__(self, dept_name, budget):
		self.dept_name = dept_name
		self.budget = budget

class Student(db.Model):

	__tablename__ = "student"

	id = db.Column(db.Integer, primary_key = True)
	stud_name = db.Column(db.String(100), primary_key = True)
	dept_id = db.Column(db.Integer, db.ForeignKey("department.id"))

	department = db.relationship("Department", back_populates="student")

	def __init__(self, name, dept_id):
		self.name = name
		self.dept_id = dept_id


@app.route("/")
def root():
	return "Welcome to College Management System"


@app.route("/department/insert", methods = ['POST', 'GET'])
def dept_insert():
	data = request.get_json()
	response = {}
	if Validate.validateJson(data, ["name"]):

		# Check whether the data is already present. If presesnt ignore
		if Validate.isPresent(db, Department, "dept_name", data["name"]):
			response["status"] = "Department already exists"

		else:

			if Validate.validateJson(data, "budget"):
				record = Department(data["name"], data["budget"])

			# No need for budget to be inserted immediately
			else:
				record = Department(data["name"], 0)

			db.session.add(record)
			db.session.commit()

			response["status"] = "Inserted Successfully"

	else:
		response["status"] = "Failed to Insert. Invalid data"

	return response


@app.route("/department/select", methods = ['POST', 'GET'])
def dept_select():
	data = request.get_json()
	response = {}
	if Validate.validateJson(data, ["attribute", "value"]):

		if hasattr(Department, data["attribute"]) is True:
			query = Generate.select(db, Department, data["attribute"], data["value"])

			if query:
				response["name"] = query.dept_name
				response["budget"] = query.budget
				response["status"] = "Success"
			else:
				response["status"] = "No data found"

		else:
			response["status"] = "Attribute Not Found"

	else:
		response["status"] = "No attributes or values"

	return response


@app.route("/department/update", methods = ['POST', 'GET'])
def dept_update():
	data = request.get_json()
	response = {}
	if Validate.validateJson(data, ["name", "budget"]):

		if Validate.isPresent(db, Department, "dept_name", data["name"]):
			query = Generate.select(db, Department, "dept_name", data["name"])
			query.budget = data["budget"]
			db.session.commit()
			response["status"] = "Updated Successfully"

		else:
			response["status"] = "Department does not exist"

	else:
		response["status"] = "Failed to update. Invalid data"

	return response
