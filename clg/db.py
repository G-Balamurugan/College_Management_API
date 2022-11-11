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

	def __init__(self, name, dept_id, stud_mum, stud_dad, year, phone_no, gender, email):
		self.stud_name = name
		self.dept_id = dept_id
		self.stud_mum = stud_mum
		self.stud_dad = stud_dad
		self.year = year
		self.phone_no = phone_no
		self.gender = gender
		self.email = email

	def as_dict(self):
		return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class Faculty(db.Model):

	__tablename__ = "faculty"

	id = db.Column(db.Integer , primary_key = True)
	facul_name = db.Column(db.String(100) , nullable = False )
	dept_id = db.Column(db.Integer , db.ForeignKey("department.id"))
	qualification = db.Column(db.String(100))
	designation = db.Column(db.String(100))
	gender = db.Column(db.String(10) , nullable = False )
	salary = db.Column(db.Integer)
	phone_no = db.Column(db.Integer)

	#department = db.relationship("Department" , back_populates="faculty")

	def __init___(self, name , dept_id , qualification , designation , gender , salary ,phone_no):
		self.facul_name = name 
		self.dept_id = dept_id 
		self.qualification = qualification
		self.designation = designation
		self.gender = gender 
		self.salary = salary 
		self.phone_no = phone_no

	def as_dict(self) :
		return {c.name : str(getattr(self, c.name)) for c in self.__table__.columns}

class Course(db.Model) :

	__tablename__ = "course"

	id = db.Column(db.Integer, primary_key = True)
	course_name  = db.Column(db.String(100) , nullable = False)
	credits = db.Column(db.Float)

	# department = db.relationship("Department" , back_populates = "course")

	def __init__(self , course_name  , credits) :
		self.course_name = course_name 
		self.credits = credits 

	def as_dict(self) :
		return {c.name : str(getattr(self,c.name)) for c in self.__table__.columns}

class Section(db.Model):
    
    __tablename__ = "section"

    id = db.Column(db.Integer, primary_key = True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
    year = db.Column(db.Integer)
    semester = db.Column(db.Integer)

    def __init__(self, course_id, year, semester):
        self.course_id = course_id
        self.year = year
        self.semester = semester
        
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
    
class Mark(db.Model):
    
    __tablename__ = "mark"
    
    id = db.Column(db.Integer, primary_key = True)
    stud_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    midsem1 = db.Column(db.Float)
    midsem2 = db.Column(db.Float)
    assgn = db.Column(db.Float)
    total = db.Column(db.Float)
    GPA = db.Column(db.Float)
    percentage = db.Column(db.Float)
    
    def __init__(self , stud_id, midsem1, midsem2, assgn):
        self.stud_id = stud_id
        self.midsem1 = midsem1
        self.midsem2 - midsem2
        self.assgn = assgn
    
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
    
class Student_attendance(db.Model):
    
    __tablename__ = "student_attendance"
    
    id = db.Column(db.Integer, primary_key = True)
    stud_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    total_working_days = db.Column(db.Integer)
    total_present = db.Column(db.Integer)
    total_absent = db.Column(db.Integer)
    percentage = db.Column(db.Float)
    
    def __init__(self, stud_id, total_working_days, total_present, total_absent) -> None:
        self.stud_id = stud_id
        self.total_working_days = total_working_days
        self.total_present = total_present
        self.total_absent= total_absent
    
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class Faculty_attendance(db.Model):
    
    __tablename__ = "faculty_attendance"
    
    id = db.Column(db.Integer, primary_key = True)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"))
    total_working_days = db.Column(db.Integer)
    total_present = db.Column(db.Integer)
    total_absent = db.Column(db.Integer)
    percentage = db.Column(db.Float)
    
    def __init__(self, faculty_id, total_working_days, total_present, total_absent) -> None:
        self.faculty_id = faculty_id
        self.total_working_days = total_working_days
        self.total_present = total_present
        self.total_absent= total_absent
    
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
    
class Classroom(db.Model):
    
    __tablename__ = "classroom"
    
    id = db.Column(db.Integer, primary_key = True)
    sec_id = db.Column(db.Integer, db.ForeignKey("section.id"))
    room_no = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    build_no = db.Column(db.Integer, primary_key = True)
    
    def __init__(self, sec_id, room_no, capacity) -> None:
        self.sec_id = sec_id
        self.room_no = room_no
        self.capacity = capacity
        
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class Time_slot(db.Model):
    
    __tablename__ = "time_slot"
    
    id = db.Column(db.Integer, primary_key = True)
    sec_id = db.Column(db.Integer, db.ForeignKey("section.id"))
    slot = db.Column(db.Integer)
    start_time = db.Column(db.DateTime) #888888888888888888888
    end_time = db.Column(db.DateTime) #88888888888888888888
    day = db.Column(db.String(100), nullable = False)
    
    def __init__(self, sec_id, slot, start_time, end_time, day) -> None:
        self.sec_id = sec_id
        self.slot = slot
        self.start_time = start_time
        self.end_time = end_time
        self.day = day
    
    def as_dict(self):
	    return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class Tutor(db.Model):
    
    __tablename__ = "tutor"
    
    id = db.Column(db.Integer, primary_key = True)
    stud_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"))

    def __init__(self, stud_id, faculty_id) -> None:
        self.stud_id = stud_id
        self.faculty_id = faculty_id
    
    def as_dict(self):
	    return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
 
class Teaches(db.Model):
    
    __tablename__ = "teaches"
    
    id = db.Column(db.Integer, primary_key = True)
    sec_id = db.Column(db.Integer, db.ForeignKey("section.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.id")) #???????????????????????????
    semester = db.Column(db.Integer)
    year = db.Column(db.Integer)
    
    def __init__(self, sec_id, course_id, semester, year) -> None:
        self.sec_id = sec_id
        self.course_id = course_id
        self.semester = semester
        self.year = year
    
    def as_dict(self):
	    return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class Takes(db.Model):
    
    __tablename__ = "takes"
    
    id = db.Column(db.Integer, primary_key = True)
    sec_id = db.Column(db.Integer, db.ForeignKey("section.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.id")) #???????????????????????????
    semester = db.Column(db.Integer)
    year = db.Column(db.Integer)
    GPA = db.Column(db.Float)
    
    def __init__(self, sec_id, course_id, semester, year, GPA) -> None:
        self.sec_id = sec_id
        self.course_id = course_id
        self.semester = semester
        self.year = year
        self.GPA = GPA
    
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
			query = Generate.selectAll(db, Department, data["attribute"], data["value"])

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


@app.route("/student/insert", methods = ['POST', 'GET'])
def stud_insert():
	data = request.get_json()
	response = {}
	dataList = ["name", "dept_id", "mum", "dad", "year", "phone", "gender", "email"]

	if Validate.json(data, dataList):
		if Validate.email(data["email"]):
			query = Generate.selectOne(db, Department, "id", data["dept_id"])
			if query:
				# name, dept_id, stud_mum, stud_dad, year, phone_no, gender, email
				record = Student(data["name"], data["dept_id"], data["mum"], data["dad"], data["year"], data["phone"], 
					data["gender"], data["email"])
				db.session.add(record)
				db.session.commit()
				response["status"] = "Inserted Successfully"
			else:
				response["status"] = "Invalid department ID"
		else:
			response["status"] = "Invalid Email"

	else:
		response["status"] = "Failed to Insert. Invalid data"

	return response


@app.route("/student/select", methods = ['POST', 'GET'])
def stud_select():
	data = request.get_json()
	response = {}
	if Validate.json(data, ["attribute", "value"]):
		# Table should contain the attribute
		if hasattr(Student, data["attribute"]):
			query = Generate.selectAll(db, Student, data["attribute"], data["value"])

			if query: #record found
				response = Generate.tuples(query)
			else:
				response["status"] = "No data found"

		else:
			response["status"] = "Attribute Not Found"

	else:
		response["status"] = "No attributes or values"

	return response


@app.route("/student/update", methods = ['POST', 'GET'])
def stud_update():
	data = request.get_json()
	response = {}
	if Validate.json(data, ["name", "update"]):

		if Validate.isPresent(db, Department, "dept_name", data["name"]):
			if hasattr(Department, data["update"]) and data["update"] != "dept_name":
				query = db.session.query(Department).filter_by(dept_name = data["name"]).first()
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

@app.route("/faculty/insert" , methods = ["POST" , "GET"])
def facul_insert():
	data = request.json()
	response = {}

	if Validate.validateJson(data,["name" , "id" , "dept_id" ,"qualification" , "designation" , "gender" , "phone_no"]):

		#check whether the data is already present .If Present ignore 
		if Validate.isPresent(db , Faculty , "id" , data["id"]) : 
			response["status"] = "Faculty details inserted successfully"

		else :

			if ( data["name"]== " ") or (data["dept_id"] == " ") or (data["qualification"]==" ") or (data["designation"]==" ") or (data["gender"] not in ["Male" , "Female","Others"]) or (len(str(data["phone_no"])) != 10 ) :

				response["status"] = "Invalid attributes" 
			
			else:
				if Validate.validateJson(data , ["salary"]) :
					#salary cannot be less than 0 
					if (data["salary"] < 0 ) :
						response["status"] = "Invalid salary"

					else :
						record = Faculty(data["name"] ,data["dept_id"] ,data["qualification"] , data["designation"] , data["gender"], data["salary"] ,data["phone_no"])
				else :
					record = Faculty(data["name"] ,data["dept_id"] ,data["qualification"] , data["designation"] , data["gender"], 0 ,data["phone_no"])

				db.session.add(record)
				db.session.commit()

				response["status"] = "Inserted Successfully"

	else:
		response["status"] = "Failed to insert. Invalid data"
	
	return response


			# if (data["name"] == " ") :
			# 	response["status"] = "Invalid Name"
			# else:
			# 	if (data["dept_id"] == " ") :
			# 		response["status"] = "Invalid Department ID"
			# 	else:
			# 		if (data["qualification"] == " ") :
			# 			response["status"] = "Invalid qualification"
			# 		else:
			# 			if (data["designation"] == " ") :
			# 				response["status"] = "Inlid "

			#------------------------------------------------
			
			
			# if Validate.validateJson(data , ["salary"]) :
			# 	#salary cannot be less than 0 
			# 	if (data["salary"] < 0 ) :
			# 		response["status"] = "Invalid salary"

			# 	else :
			# 		record = Faculty(data["name"] ,data["dept_id"] ,data["qualification"] , data["designation"] , data["gender"], data["salary"] ,data["phone_no"])
			# else :
			# 	record = Faculty(data["name"] ,data["dept_id"] , data["gender"], 0 ,data["phone_no"])

			# db.session.add(record)
			# db.session.commit()

			# response["status"] = "Inserted Successfully"


@app.route("/faculty/select" , methods = ["POST","GET"])
def facul_select():
	data = request.get_json()
	response = {}
	if Validate.validateJson(data , ["attribute" , "value"]) :
		#table should contain the attribute
		if hasattr(Faculty , data["attribute"]) :
			query = Generate.select(db , Faculty , data["attribute"] , data["value"])

			if query :
				response = Generate.tuples(query)
			else: 
				response["status"] = "No data found"
		else:
			response["status"] = "Attribute Not Found"
	else:
		response["status"] = "No attributes or values"

	return response

@app.route("/faculty/update" , methods = ["POST","GET"])
def facul_update():
	data = request.get_json()
	response = {}

	if Validate.validateJson(data, ["name" , "update"]):

		if Validate.isPresent(db , Faculty , "id" , data["name"]):
			if hasattr(Faculty , data["update"]) and data["update"] != "id" :
				query = db.session.query(Faculty).filter_by(dept_name = data["name"]).first

				setattr(query , data["update"] , data["value"])
				db.session.commit()
				response["status"] = "Updated successfully"
			else:
				response["status"] = "Attribute Not Found or Invalid Attribute"
		else :
			response["status"] = "Faculty  does not exist"
	else:
		response["status"] = "Failed to update. Invalid data"
	
	return response


@app.route("/course/insert" , methods = ["POST" , "GET" ])
def course_insert(self):
	data = request.get_json()
	response = {}

	if Validate.validateJson(data , ["course_id" , "course_name" ]) : 
		#Check whether the data is already present .If present ignore 
		if Validate.isPresent(db, "Course" , "course_id" , data["course_id"]) :
			response["status"] = "Course already exists"
		
		else:

			if (data["course_id"]==" ") or (data["course_name"]==" ") :
				response["status"] = "Invalid values"
			else:
				if Validate.validateJson(data , ["credits"]) :
					if (data["credits"] < 0 ):
						response["status"] = "Invalid Budget"
					else: 
						record = Course(data["course_id"] , data["course_name"] , data["credits"] )
				else: 
					record = Course(data["course_id"] , data["course_name"] , 0 )

				db.session.add(record)
				db.session.commit()

				response["status"] = "Inserted Successfully"
	else:
		response["status"] = "Failed to Insert. Invalid data"

	return response


@app.route("/course/select" , methods = ["POST" , "GET"])
def course_select(self) :
	data = request.get_json()
	response = {}

	if Validate.validateJson(data , ["attribute" , "value"]):

		if hasattr(Course , data["attribute"]) :
			query = Generate.select(db , Course , data["attribute"] , data["value"]) 

			if query :
				response = Generate.tuples(query)
			else:
				response["status"] = "No data found"
		else: 
			response["status"] = "Attribute not found "
	
	else:
		response["status"] = "No attributes or values"

	return response

@app.route("/course/update" , methods = ["POST" , "GET"])
def course_update(self) : 
	data = request.get_json()
	response = {}

	if Validate.validateJson(data , ["name" , "update"]) :

		if Validate.isPresent(db, Course , "course_name", data["name"]) :
			if hasattr(Course , data["update"]) and data["update"]!="course_id" :
				query = db.session.query(Course).filter_by(course_name = data["name"]).first
				setattr(query , data["update"] , data["value"])
				db.session.commit()
				response["status"] = "Updated Successfully"

			else: 
				response["status"] = "Attribute not found or Invalid attribute"
		else:
			response["status"] = "Course does not exist"

	else:
		response["status"] = "Failed to Update"
	
	return response
