from flask import Flask, request
from urllib.parse import quote_plus
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:%s@localhost/college' % quote_plus('Gowtham@2543')
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
	name = db.Column(db.String(100))
	dep_id = db.Column(db.Integer, db.ForeignKey("department.id"))

	department = db.relationship("Department", back_populates="student")

	def __init__(self, name, dep_id):
		self.name = name
		self.dep_id = dep_id

@app.route("/")
def hello():
	return "hello"

@app.route("/insert", methods = ['POST', 'GET'])
def insert():
	data = request.get_json()
	record = Student(data["name"])
	db.session.add(record)
	db.session.commit()
	return "Inserted Successfully"
