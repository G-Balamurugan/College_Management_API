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
	dept_name = db.Column(db.String(100), nullable = False)
	budget = db.Column(db.Integer)
	building = db.Column(db.String(100), nullable = False)

	student = db.relationship("Student", back_populates="department")

	def __init__(self, dept_name, budget, building):
		self.dept_name = dept_name
		self.budget = budget
		self.building = building

	def as_dict(self):
		return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class Student(db.Model):

	__tablename__ = "student"

	id = db.Column(db.Integer, primary_key = True)
	stud_name = db.Column(db.String(100))
	dept_id = db.Column(db.Integer, db.ForeignKey("department.id"))
	stud_mum = db.Column(db.String(100))
	stud_dad = db.Column(db.String(100))
	year = db.Column(db.Integer)
	phone_no = db.Column(db.String(100))
	gender = db.Column(db.String(10))
	email = db.Column(db.String(100))


	department = db.relationship("Department", back_populates="student")

	def __init__(self, name, dept_id, stud_mum, stud_dad):
		self.name = name
		self.dept_id = dept_id
		self.stud_mum = stud_mum
		self.stud_dad = stud_dad
		self.year = year
		self.phone_no = phone_no
		self.gender = gender
		self.email = email

	def as_dict(self):
		return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

@app.route("/")
def root():
	return "Welcome to College Management System"


@app.route("/department/insert", methods = ['POST', 'GET'])
def dept_insert():
	data = request.get_json()
	response = {}
	if Validate.json(data, ["name", "building"]):

		# Check whether the data is already present. If presesnt ignore
		if Validate.isPresent(db, Department, "dept_name", data["name"]):
			response["status"] = "Department already exists"

		else:
			if Validate.json(data, ["budget"]):
				# Budget cannot be less than 0
				if(data["budget"] < 0):
					response["status"] = "Invalid budget"
				else:
					record = Department(data["name"], data["budget"], data["building"])

			# No need for budget to be inserted immediately
			else:
				record = Department(data["name"], 0, data["building"])

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
	if Validate.json(data, ["attribute", "value"]):
		# Table should contain the attribute
		if hasattr(Department, data["attribute"]):
			query = Generate.select(db, Department, data["attribute"], data["value"])

			if query: #record found
				response = Generate.tuples(query)
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
	if Validate.json(data, ["name", "update"]):

		if Validate.isPresent(db, Department, "dept_name", data["name"]):
			if hasattr(Department, data["update"]) and data["update"] != "dept_name":
				query = db.session.query(Department).filter_by(dept_name = data["name"]).first()
				# query. = data["budget"]
				setattr(query, data["update"], data["value"])
				db.session.commit()
				response["status"] = "Updated Successfully"
			else:
				response["status"] = "Attribute Not Found or Invalid Attribute"


		else:
			response["status"] = "Department does not exist"

	else:
		response["status"] = "Failed to update. Invalid data"

	return response
