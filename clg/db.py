from flask import Flask, request, jsonify
from urllib.parse import quote_plus
from flask_sqlalchemy import SQLAlchemy
from clg.validate import Validate
from clg.generate import Generate
import json

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:%s@localhost/college' % quote_plus('bala')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class Department(db.Model):

	__tablename__ = "department"

	id = db.Column(db.Integer, primary_key = True)
	dept_name = db.Column(db.String(100))
	budget = db.Column(db.Integer)
	building = db.Column(db.String(100), nullable = False)

	#student = db.relationship("Student", back_populates="department")
	faculty = db.relationship("Faculty", back_populates="department")

	def __init__(self, id , dept_name, budget, building):
		self.id = id
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


	#department = db.relationship("Department", back_populates="student")

	def __init__(self,id, name, dept_id, stud_mum, stud_dad, year, phone_no, gender, email):
		self.id = id
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
	name = db.Column(db.String(100) , nullable = False )
	dept_id = db.Column(db.Integer , db.ForeignKey("department.id"))
	qualification = db.Column(db.String(100))
	designation = db.Column(db.String(100))
	gender = db.Column(db.String(10) , nullable = False )
	salary = db.Column(db.Integer)
	phone_no = db.Column(db.String(20))

	department = db.relationship("Department" , back_populates="faculty")

	def __init__(self,id, name , dept_id , qualification , designation , gender , salary ,phone_no):
		self.id = id
		self.name = name 
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

	def __init__(self , id , course_name  , credits) :
		self.id = id
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

    def __init__(self, id , course_id, year, semester):
        self.course_id = course_id
        self.year = year
        self.semester = semester
        self.id=id
        
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
        self.midsem2 = midsem2
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
    start_time = db.Column(db.DateTime) 
    end_time = db.Column(db.DateTime) 
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
 
# class Teaches(db.Model):
    
#     __tablename__ = "teaches"
    
#     id = db.Column(db.Integer, primary_key = True)
#     sec_id = db.Column(db.Integer, db.ForeignKey("section.id"))
#     course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
#     semester = db.Column(db.Integer)
#     year = db.Column(db.Integer)
    
#     def __init__(self, sec_id, course_id, semester, year) -> None:
#         self.sec_id = sec_id
#         self.course_id = course_id
#         self.semester = semester
#         self.year = year
    
#     def as_dict(self):
# 	    return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class Takes(db.Model):
    
    __tablename__ = "takes"
    
    id = db.Column(db.Integer, primary_key = True)
    sec_id = db.Column(db.Integer, db.ForeignKey("section.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.id")) 
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
	if Validate.json(data, ["dept_id","name", "building"]):

		# Check whether the data is already present. If presesnt ignore
		if Validate.isPresent(db, Department, "id", data["dept_id"]) or Validate.isPresent(db, Department, "dept_name", data["name"]):
			response["status"] = "Department already exists"
		else:
			if Validate.json(data, ["budget"]):
				# Budget cannot be less than 0
				if(data["budget"] < 0):
					response["status"] = "Invalid budget"
				else:
					record = Department(data["dept_id"],data["name"], data["budget"], data["building"])

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
		if hasattr(Department, data["attribute"]) or (data["attribute"]==""):
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
	dataList = ["name", "id" , "dept_id", "mum", "dad", "year", "phone", "gender", "email"]

	if Validate.json(data, dataList):
		if Validate.email(data["email"]):
			if Validate.isPresent(db, Student, "id", data["id"]):
				response["status"] = "Student ID already exists"
			else:		
				query1 = Generate.selectAll(db, Department, "id", data["dept_id"])
				if query1:
					# name, dept_id, stud_mum, stud_dad, year, phone_no, gender, email
					record = Student(data["id"],data["name"],data["dept_id"], data["mum"], data["dad"], data["year"], data["phone"], data["gender"], data["email"])
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


# @app.route("/student/update", methods = ['POST', 'GET'])
# def stud_update():
# 	data = request.get_json()
# 	response = {}
# 	if Validate.json(data, ["name", "update"]):

# 		if Validate.isPresent(db, Department, "dept_name", data["name"]):
# 			if hasattr(Department, data["update"]) and data["update"] != "dept_name":
# 				query = db.session.query(Department).filter_by(dept_name = data["name"]).first()
# 				setattr(query, data["update"], data["value"])
# 				db.session.commit()
# 				response["status"] = "Updated Successfully"
# 			else:
# 				response["status"] = "Attribute Not Found or Invalid Attribute"


# 		else:
# 			response["status"] = "Department does not exist"

# 	else:
# 		response["status"] = "Failed to update. Invalid data"

# 	return response
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route("/student/update", methods = ['POST', 'GET'])
def stud_update():
	data = request.get_json()
	response = {}
	if Validate.json(data, ["new_value", "update_attribute", "where_attribute", "where_value"]):
		if hasattr(Student, data["update_attribute"]) and data["update_attribute"]!="id":
			if (data["update_attribute"]=="dept_id" and Validate.isPresent(db, Department, "id" , data["new_value"])) or Validate.isPresent(db, Student, data["where_attribute"] , data["where_value"]):
				query = db.session.query(Student).filter(getattr(Student,data["where_attribute"])== data["where_value"]).first()
				setattr(query, data["update_attribute"], data["new_value"])
				db.session.commit()
				response["status"] = "Updated Successfully"
			else:
				response["status"] = "Attribute Not Found or Invalid Attribute"
		else:
			response["status"] = "Cannot Modify Primary Key"
	else:
		response["status"] = "Failed to update. Invalid data"
	return response

@app.route("/tutor/update", methods = ['POST', 'GET'])
def tutor_update():
	data = request.get_json()
	response = {}
	if Validate.json(data, ["new_value", "update_attribute", "where_attribute", "where_value"]):
		if hasattr(Tutor, data["update_attribute"]) and data["update_attribute"]!="id":
			if(data["update_attribute"]=="stud_id" and Validate.isPresent(db, Student, "id" , data["new_value"])) or(data["update_attribute"]=="faculty_id" and Validate.isPresent(db, Faculty, "id" , data["new_value"])):
				if Validate.isPresent(db, Tutor, data["where_attribute"] , data["where_value"]):
					query = db.session.query(Tutor).filter(getattr(Tutor,data["where_attribute"])== data["where_value"]).first()
					setattr(query, data["update_attribute"], data["new_value"])
					db.session.commit()
					response["status"] = "Updated Successfully"
				else:
					response["status"] = "Attribute Not Found or Invalid Attribute"
			else:
				response["status"] = "Foreign Key Constraint or Invalid Entry"
		else:
			response["status"] = "Cannot Modify . Invalid Entry"
	else:
		response["status"] = "Failed to update. Invalid data"
	return response

@app.route("/takes/update", methods = ['POST', 'GET'])
def takes_update():
	data = request.get_json()
	response = {}
	if Validate.json(data, ["new_value", "update_attribute", "where_attribute", "where_value"]):
		if hasattr(Takes, data["update_attribute"]) and data["update_attribute"]!="id":
			if Validate.isPresent(db, Takes, data["where_attribute"] , data["where_value"]) or (data["update_attribute"]=="sec_id" and Validate.isPresent(db, Section, "id" , data["new_value"])) or (data["update_attribute"]=="course_id" and Validate.isPresent(db, Course, "id" , data["new_value"])):
				query = db.session.query(Takes).filter(getattr(Takes,data["where_attribute"])== data["where_value"]).first()
				setattr(query, data["update_attribute"], data["new_value"])
				db.session.commit()
				response["status"] = "Updated Successfully"
			
			else:
				response["status"] = "Foreign Key Constraint or Invalid Entry "
		else:
			response["status"] = "Cannot Modify . Invalid Entry"
	else:
		response["status"] = "Failed to update. Invalid data"
	return response

@app.route("/student_attendance/update", methods = ['POST', 'GET'])
def student_attendance_update():
	data = request.get_json()
	response = {}
	if Validate.json(data, ["new_value", "update_attribute", "where_attribute", "where_value"]):
		if hasattr(Student_attendance, data["update_attribute"]) and data["update_attribute"]!="id":
			if (data["update_attribute"]=="stud_id" and Validate.isPresent(db, Student, "id" , data["new_value"])) or Validate.isPresent(db, Student_attendance, data["where_attribute"] , data["where_value"]):
				query = db.session.query(Student_attendance).filter(getattr(Student_attendance,data["where_attribute"])== data["where_value"]).first()
				setattr(query, data["update_attribute"], data["new_value"])
				db.session.commit()
				response["status"] = "Updated Successfully"
			else:
				response["status"] = "Attribute Not Found or Invalid Attribute"
		else:
			response["status"] = "Cannot Modify . Invalid Entry"
	else:
		response["status"] = "Failed to update. Invalid data"
	return response

@app.route("/faculty_attendance/update", methods = ['POST', 'GET'])
def faculty_attendance_update():
	data = request.get_json()
	response = {}
	if Validate.json(data, ["new_value", "update_attribute", "where_attribute", "where_value"]):
		if hasattr(Faculty_attendance, data["update_attribute"]) and data["update_attribute"]!="id":
			if (data["update_attribute"]=="faculty_id" and Validate.isPresent(db, Facullty, "id" , data["new_value"])) or Validate.isPresent(db, Faculty_attendance, data["where_attribute"] , data["where_value"]):
				query = db.session.query(Faculty_attendance).filter(getattr(Faculty_attendance,data["where_attribute"])== data["where_value"]).first()
				setattr(query, data["update_attribute"], data["new_value"])
				db.session.commit()
				response["status"] = "Updated Successfully"
			else:
				response["status"] = "Attribute Not Found or Invalid Attribute"
		else:
			response["status"] = "Cannot Modify . Invalid Entry"
	else:
		response["status"] = "Failed to update. Invalid data"
	return response
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route("/faculty/insert", methods = ['POST', 'GET'])
def faculty_insert():
	data = request.get_json()
	response = {}
	dataList = ["name","id" , "dept_id", "qualification", "designation", "gender", "phone_no"]

	if Validate.json(data, dataList):
		if Validate.isPresent(db, Faculty, "id", data["id"]):
				response["status"] = "Facullty ID already exists"
		else:
			query = Generate.selectAll(db, Department, "id", data["dept_id"])
			if query:
				# name, dept_id, stud_mum, stud_dad, year, phone_no, gender, email
				if Validate.json(data , ["salary"]):
					if (data["salary"]<0) :
						response["status"] = "Invalid Salary"
					else: 
						record = Faculty(data["id"],data["name"],data["dept_id"], data["qualification"], data["designation"], data["gender"] , data["salary"] , data["phone_no"])
						db.session.add(record)
						db.session.commit()
						response["status"] = "Inserted Successfully"
				else :
					record = Faculty(data["name"],data["dept_id"], data["qualification"], data["designation"], data["gender"] , 0, data["phone_no"])
					db.session.add(record)
					db.session.commit()
					response["status"] = "Inserted Successfully"
			else:
				response["status"] = "Invalid department ID"
		
	else:
		response["status"] = "Failed to Insert. Invalid data"

	return response


@app.route("/faculty/select" , methods = ["POST","GET"])
def facul_select():
	data = request.get_json()
	response = {}
	if Validate.json(data , ["attribute" , "value"]) :
		#table should contain the attribute
		if hasattr(Faculty , data["attribute"]) :
			query = Generate.selectAll(db , Faculty , data["attribute"] , data["value"])

			if query :
				response = Generate.tuples(query)
			else: 
				response["status"] = "No data found"
		else:
			response["status"] = "Attribute Not Found"
	else:
		response["status"] = "No attributes or values"

	return response

# @app.route("/faculty/update" , methods = ["POST","GET"])
# def facul_update():
# 	data = request.get_json()
# 	response = {}

# 	if Validate.json(data, ["name" , "update"]):

# 		if Validate.isPresent(db , Faculty , "id" , data["name"]):
# 			if hasattr(Faculty , data["update"]) and data["update"] != "id" :
# 				query = db.session.query(Faculty).filter_by(dept_name = data["name"]).first

# 				setattr(query , data["update"] , data["value"])
# 				db.session.commit()
# 				response["status"] = "Updated successfully"
# 			else:
# 				response["status"] = "Attribute Not Found or Invalid Attribute"
# 		else :
# 			response["status"] = "Faculty  does not exist"
# 	else:
# 		response["status"] = "Failed to update. Invalid data"
	
# 	return response

#..............................................................................................
@app.route("/section/insert" , methods = ["POST" , "GET" ])
def section_insert():
	data = request.get_json()
	response = {}
	dataList = ["sec_id","course_id" , "year" , "semester"]

	if Validate.json(data, dataList):
		query = Generate.selectAll(db, Course, "id", data["course_id"])
		if query:
			if Validate.isPresent(db, Section, "id", data["sec_id"]):
				response["status"] = "Section ID already exists"
			else:
				if data["semester"]>0 and data["year"] > 1950:
					record = Section(data["sec_id"],data["course_id"],data["year"],data["semester"])
					db.session.add(record)
					db.session.commit()
					response["status"] = "Inserted Successfully"
				else:
					response["status"] = "Invalid values"
		else:
			response["status"] = "Invalid Course ID"
	else:
		response["status"] = "Failed to Insert. Invalid data"

	return response

@app.route("/section/select" , methods = ["POST" , "GET"])
def section_select() :
	data = request.get_json()
	response = {}

	if Validate.json(data , ["attribute" , "value"]):

		if hasattr(Section , data["attribute"]) :
			query = Generate.selectAll(db , Section , data["attribute"] , data["value"]) 

			if query :
				response = Generate.tuples(query)
			else:
				response["status"] = "No data found"
		else: 
			response["status"] = "Attribute not found "
	
	else:
		response["status"] = "No attributes or values"

	return response

@app.route("/classroom/select" , methods = ["POST" , "GET"])
def classroom_select() :
	data = request.get_json()
	response = {}

	if Validate.json(data , ["attribute" , "value"]):

		if hasattr(Classroom , data["attribute"]) :
			query = Generate.selectAll(db , Classroom , data["attribute"] , data["value"]) 

			if query :
				response = Generate.tuples(query)
			else:
				response["status"] = "No data found"
		else: 
			response["status"] = "Attribute not found "
	
	else:
		response["status"] = "No attributes or values"

	return response

@app.route("/tutor/insert" , methods = ["POST" , "GET" ])
def tutor_insert():
	data = request.get_json()
	response = {}
	dataList = ["stud_id" , "faculty_id"]

	if Validate.json(data, dataList):
		query1 = Generate.selectAll(db, Student, "id", data["stud_id"])
		if query1:
			query2 = Generate.selectAll(db, Faculty, "id", data["faculty_id"])
			if query2:
				record = Tutor(data["stud_id"],data["faculty_id"])
				db.session.add(record)
				db.session.commit()
				response["status"] = "Inserted Successfully"
			else:
				response["status"] = "Invalid Faculty ID"
		else:
			response["status"] = "Invalid Student ID"
	else:
		response["status"] = "Failed to Insert. Invalid data"

	return response

@app.route("/tutor/select" , methods = ["POST" , "GET"])
def tutor_select() :
	data = request.get_json()
	response = {}

	if Validate.json(data , ["attribute" , "value"]):

		if hasattr(Tutor , data["attribute"]) :
			query = Generate.selectAll(db , Tutor , data["attribute"] , data["value"]) 

			if query :
				response = Generate.tuples(query)
			else:
				response["status"] = "No data found"
		else: 
			response["status"] = "Attribute not found "
	
	else:
		response["status"] = "No attributes or values"

	return response

@app.route("/takes/insert" , methods = ["POST" , "GET" ])
def takes_insert():
	data = request.get_json()
	response = {}
	dataList = ["sec_id" , "course_id" , "semester" , "year" , "GPA"]

	if Validate.json(data, dataList):
		query1 = Generate.selectAll(db, Section, "id", data["sec_id"])
		if query1:
			query2 = Generate.selectAll(db, Course, "id", data["course_id"])
			if query2:
				if data["semester"]>0 and data["year"] > 1950 and data["GPA"] > -1:
					record = Takes(data["sec_id"],data["course_id"],data["semester"],data["year"],data["GPA"])
					db.session.add(record)
					db.session.commit()
					response["status"] = "Inserted Successfully"
				else:
					response["status"] = "Invalid values"
			else:
				response["status"] = "Invalid Course ID"
		else:
			response["status"] = "Invalid Section ID"
	else:
		response["status"] = "Failed to Insert. Invalid data"

	return response

@app.route("/takes/select" , methods = ["POST" , "GET"])
def takes_select() :
	data = request.get_json()
	response = {}

	if Validate.json(data , ["attribute" , "value"]):

		if hasattr(Takes , data["attribute"]) or data["attribute"]=="":
			query = Generate.selectAll(db , Takes , data["attribute"] , data["value"]) 

			if query :
				response = Generate.tuples(query)
			else:
				response["status"] = "No data found"
		else: 
			response["status"] = "Attribute not found "
	else:
		response["status"] = "No attributes or values"

	return response

@app.route("/time_slot/select" , methods = ["POST" , "GET"])
def time_slot_select() :
	data = request.get_json()
	response = {}

	if Validate.json(data , ["attribute" , "value"]):

		if hasattr(Time_slot , data["attribute"]) :
			query = Generate.selectAll(db , Time_slot , data["attribute"] , data["value"]) 

			if query :
				response = Generate.tuples(query)
			else:
				response["status"] = "No data found"
		else: 
			response["status"] = "Attribute not found "
	
	else:
		response["status"] = "No attributes or values"

	return response

# @app.route("/teaches/insert" , methods = ["POST" , "GET" ])
# def teaches_insert():
# 	data = request.get_json()
# 	response = {}
# 	dataList = ["sec_id" , "course_id" , "semester" , "year" ]

# 	if Validate.json(data, dataList):
# 		query1 = Generate.selectAll(db, Section, "id", data["sec_id"])
# 		if query1:
# 			query2 = Generate.selectAll(db, Course, "id", data["course_id"])
# 			if query2:
# 				if data["semester"]>0 and data["year"] > 1950:
# 					record = Teaches(data["sec_id"],data["course_id"],data["semester"],data["year"])
# 					db.session.add(record)
# 					db.session.commit()
# 					response["status"] = "Inserted Successfully"
# 				else:
# 					response["status"] = "Invalid values"
# 			else:
# 				response["status"] = "Invalid Course ID"
# 		else:
# 			response["status"] = "Invalid Section ID"
# 	else:
# 		response["status"] = "Failed to Insert. Invalid data"

# 	return response

# @app.route("/teaches/select" , methods = ["POST" , "GET"])
# def teaches_select() :
# 	data = request.get_json()
# 	response = {}

# 	if Validate.json(data , ["attribute" , "value"]):

# 		if hasattr(Teaches , data["attribute"]) :
# 			query = Generate.selectAll(db , Teaches , data["attribute"] , data["value"]) 

# 			if query :
# 				response = Generate.tuples(query)
# 			else:
# 				response["status"] = "No data found"
# 		else: 
# 			response["status"] = "Attribute not found "
	
# 	else:
# 		response["status"] = "No attributes or values"

# 	return response

@app.route("/mark/insert" , methods = ["POST" , "GET" ])
def mark_insert():
	data = request.get_json()
	response = {}
	dataList = ["stud_id" , "midsem1" , "midsem2" , "assgn" ]

	if Validate.json(data, dataList):
		query = Generate.selectAll(db, Student, "id", data["stud_id"])
		if query:
			if data["midsem1"] > -1 and data["midsem2"] > -1 and data["assgn"] > -1:
				record = Mark(data["stud_id"],data["midsem1"],data["midsem2"],data["assgn"])
				db.session.add(record)
				db.session.commit()
				response["status"] = "Inserted Successfully"
			else:
				response["status"] = "Invalid values"
		else:
			response["status"] = "Invalid Student ID"
	else:
		response["status"] = "Failed to Insert. Invalid data"

	return response

@app.route("/mark/select" , methods = ["POST" , "GET"])
def mark_select() :
	data = request.get_json()
	response = {}

	if Validate.json(data , ["attribute" , "value"]):

		if hasattr(Mark , data["attribute"]) :
			query = Generate.selectAll(db , Mark , data["attribute"] , data["value"]) 
			if query :
				response = Generate.tuples(query)
			else:
				response["status"] = "No data found"
		else: 
			response["status"] = "Attribute not found "
	
	else:
		response["status"] = "No attributes or values"

	return response

@app.route("/student_attendance/insert" , methods = ["POST" , "GET" ])
def student_attendance_insert():
	data = request.get_json()
	response = {}
	dataList = ["stud_id" , "total_working_days" , "total_present" , "total_absent"]

	if Validate.json(data, dataList):
		query = Generate.selectAll(db, Student, "id", data["stud_id"])
		if query:
			if data["total_working_days"]>0 and data["total_present"] > -1 and data["total_absent"] > -1:
				record = Student_attendance(data["stud_id"],data["total_working_days"],data["total_present"],data["total_absent"])
				db.session.add(record)
				db.session.commit()
				response["status"] = "Inserted Successfully"
			else:
				response["status"] = "Invalid values"
		else:
			response["status"] = "Invalid Student ID"
	else:
		response["status"] = "Failed to Insert. Invalid data"

	return response

@app.route("/student_attendance/select" , methods = ["POST" , "GET"])
def student_attendance_select() :
	data = request.get_json()
	response = {}

	if Validate.json(data , ["attribute" , "value"]):

		if hasattr(Student_attendance , data["attribute"]) :
			query = Generate.selectAll(db , Student_attendance , data["attribute"] , data["value"]) 

			if query :
				response = Generate.tuples(query)
			else:
				response["status"] = "No data found"
		else: 
			response["status"] = "Attribute not found "
	
	else:
		response["status"] = "No attributes or values"

	return response

@app.route("/faculty_attendance/insert" , methods = ["POST" , "GET" ])
def faculty_attendance_insert():
	data = request.get_json()
	response = {}
	dataList = ["faculty_id" , "total_working_days" , "total_present" , "total_absent"]

	if Validate.json(data, dataList):
		query = Generate.selectAll(db, Faculty, "id", data["faculty_id"])
		if query:
			if data["total_working_days"]>0 and data["total_present"] > -1 and data["total_absent"] > -1:
				record = Faculty_attendance(data["faculty_id"],data["total_working_days"],data["total_present"],data["total_absent"])
				db.session.add(record)
				db.session.commit()
				response["status"] = "Inserted Successfully"
			else:
				response["status"] = "Invalid values"
		else:
			response["status"] = "Invalid Faculty ID"
	else:
		response["status"] = "Failed to Insert. Invalid data"

	return response

@app.route("/faculty_attendance/select" , methods = ["POST" , "GET"])
def faculty_attendance_select() :
	data = request.get_json()
	response = {}

	if Validate.json(data , ["attribute" , "value"]):

		if hasattr(Faculty_attendance , data["attribute"]) :
			query = Generate.selectAll(db , Faculty_attendance , data["attribute"] , data["value"]) 

			if query :
				response = Generate.tuples(query)
			else:
				response["status"] = "No data found"
		else: 
			response["status"] = "Attribute not found "
	
	else:
		response["status"] = "No attributes or values"

	return response

#..............................................................................................

@app.route("/course/insert" , methods = ["POST" , "GET" ])
def course_insert():
	data = request.get_json()
	response = {}
	dataList = ["id","credit" , "course_name"]

	if Validate.json(data, dataList):
		if Validate.isPresent(db, Course , "course_name" , data["course_name"]) :
			response["status"] = "Course already exists"
		else:
			if data["course_name"]!="" and data["credit"]>0:
				record = Course(data["id"],data["course_name"],data["credit"])
				db.session.add(record)
				db.session.commit()
				response["status"] = "Inserted Successfully"
			else:
				response["status"] = "Invalid values"
	else:
		response["status"] = "Failed to Insert. Invalid data"

	return response

@app.route("/course/select" , methods = ["POST" , "GET"])
def course_select() :
	data = request.get_json()
	response = {}

	if Validate.json(data , ["attribute" , "value"]):

		if hasattr(Course , data["attribute"]) :
			query = Generate.selectAll(db , Course , data["attribute"] , data["value"]) 

			if query :
				response = Generate.tuples(query)
			else:
				response["status"] = "No data found"
		else: 
			response["status"] = "Attribute not found "
	
	else:
		response["status"] = "No attributes or values"

	return response
