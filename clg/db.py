from flask import Flask, request, jsonify
from urllib.parse import quote_plus
from flask_sqlalchemy import SQLAlchemy
from clg.validate import Validate
from clg.generate import Generate
from clg.lower import Lower
import json
from clg.models.models import db, Department, Student, Faculty, Section, Course, Tutor, Teaches, Takes, Student_attendance, Faculty_attendance, Mark, Time_slot, Classroom

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:%s@localhost/college' % quote_plus('Ish@2002')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/")
def root():
	return "Welcome to College Management System"

#	DEPARTMENT

@app.route("/department/insert", methods = ['POST', 'GET'])
def dept_insert():
	data = request.get_json()
	data = Lower.toLower(data)
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
				record = Department(data["dept_id"],data["name"], 0, data["building"])

			db.session.add(record)
			db.session.commit()

			response["status"] = "Inserted Successfully"

	else:
		response["status"] = "Failed to Insert. Invalid data"

	return response


@app.route("/department/select", methods = ['POST', 'GET'])
def dept_select():
	data = request.get_json()
	data = Lower.toLower(data)
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
	data = Lower.toLower(data)
	response = {}
	if Validate.json(data, ["update_attribute", "new_value", "where_attribute" , "where_value" ]):

		if Validate.isPresent(db, Department, data["where_attribute"] , data["where_value"]):
			if hasattr(Department, data["update_attribute"]) and data["where_attribute"] != "id":
				query = db.session.query(Department).filter( getattr(Department , data["where_attribute"]) == data["where_value"]).first()

				setattr(query, data["update_attribute"], data["new_value"])
				db.session.commit()
				response["status"] = "Updated Successfully"
			else:
				response["status"] = "Attribute Not Found or Invalid Attribute"
		else:
			response["status"] = "Attribute does not exist"

	else:
		response["status"] = "Failed to update. Invalid data"

	return response

#	STUDENT

@app.route("/student/insert", methods = ['POST', 'GET'])
def stud_insert():
	data = request.get_json()
	data = Lower.toLower(data)	
	response = {}
	dataList = ["name", "id" , "dept_id", "sec_id", "mum", "dad", "year", "phone", "gender", "email"]

	if Validate.json(data, dataList):
		if Validate.email(data["email"]):
			if Validate.isPresent(db, Student, "id", data["id"]):
				response["status"] = "Student ID already exists"
			else:		
				query1 = Generate.selectAll(db, Department, "id", data["dept_id"])
				if query1:
					query2 = Generate.selectAll(db, Section, "id", data["sec_id"])
					if query2:
						# name, dept_id, stud_mum, stud_dad, year, phone_no, gender, email
						record = Student(data["id"],data["name"],data["dept_id"],data["sec_id"], data["mum"], data["dad"], data["year"], data["phone"], data["gender"], data["email"])
						db.session.add(record)
						db.session.commit()
						response["status"] = "Inserted Successfully"
					else:
						response["status"] = "Invalid Student ID"
				else:
					response["status"] = "Invalid Department ID"
		else:
			response["status"] = "Invalid Email"
	else:
		response["status"] = "Failed to Insert. Invalid Attribute"

	return response


@app.route("/student/select", methods = ['POST', 'GET'])
def stud_select():
	data = request.get_json()
	data = Lower.toLower(data)
	response = {}
	if Validate.json(data, ["attribute", "value"]):
		# Table should contain the attribute
		if hasattr(Student, data["attribute"]) or (data["attribute"]==""):
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
	data = Lower.toLower(data)
	response = {}
	if Validate.json(data, ["new_value", "update_attribute", "where_attribute", "where_value"]):
		if hasattr(Student, data["update_attribute"]) and data["update_attribute"]!="id":
			if (data["update_attribute"]=="stud_id" and Validate.isPresent(db, Student, "id" , data["new_value"])) or (data["update_attribute"]=="dept_id" and Validate.isPresent(db, Department, "id" , data["new_value"])) or (Validate.isPresent(db, Student, data["where_attribute"] , data["where_value"]) and data["update_attribute"]!="sec_id" and data["update_attribute"]!="dept_id"):
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

#	FACULTY

@app.route("/faculty/insert", methods = ['POST', 'GET'])
def faculty_insert():
	data = request.get_json()
	data = Lower.toLower(data)
	response = {}
	dataList = ["name", "id" , "dept_id", "qualification", "designation", "gender", "phone_no"]

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
					record = Faculty(data["id"] , data["name"],data["dept_id"], data["qualification"], data["designation"], data["gender"] , 0, data["phone_no"])
					db.session.add(record)
					db.session.commit()
					response["status"] = "Inserted Successfully"
			else:
				response["status"] = "Invalid department ID"
		
	else:
		response["status"] = "Failed to Insert. Invalid data"

	return response


@app.route("/faculty/select" , methods = ["POST","GET"])
def faculty_select():
	data = request.get_json()
	data = Lower.toLower(data)
	response = {}
	if Validate.json(data , ["attribute" , "value"]) :
		#table should contain the attribute
		if hasattr(Faculty , data["attribute"]) or (data["attribute"]==""):
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


@app.route("/faculty/update", methods = ['POST', 'GET'])
def faculty_update():
	data = request.get_json()
	data = Lower.toLower(data)
	response = {}
	if Validate.json(data, ["update_attribute", "new_value", "where_attribute" , "where_value" ]):

		if hasattr(Faculty, data["update_attribute"]) and data["where_attribute"] != "id":
			if (data["update_attribute"]=="dept_id" and Validate.isPresent(db, Department, "id" , data["new_value"])) or (Validate.isPresent(db, Faculty, data["where_attribute"] , data["where_value"]) and data["update_attribute"]!="dept_id"):
				query = db.session.query(Faculty).filter( getattr(Faculty , data["where_attribute"]) == data["where_value"]).first()
				setattr(query, data["update_attribute"], data["new_value"])
				db.session.commit()
				response["status"] = "Updated Successfully"
			else:
				response["status"] = "Attribute Not Found or Invalid Attribute"

		else:
			response["status"] = "Attribute does not exist"

	else:
		response["status"] = "Failed to update. Invalid data"

	return response

#	SECTION

@app.route("/section/insert" , methods = ["POST" , "GET" ])
def section_insert():
	data = request.get_json()
	data = Lower.toLower(data)
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
	data = Lower.toLower(data)
	response = {}

	if Validate.json(data , ["attribute" , "value"]):

		if hasattr(Section , data["attribute"]) or (data["attribute"]==""):
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


@app.route("/section/update", methods = ['POST', 'GET'])
def section_update():
	data = request.get_json()
	data = Lower.toLower(data)
	response = {}
	if Validate.json(data, ["update_attribute", "new_value", "where_attribute" , "where_value" ]):

		if hasattr(Section, data["update_attribute"]) and data["where_attribute"] != "id":
			if (data["update_attribute"]=="course_id" and Validate.isPresent(db, Course, "course_id" , data["new_value"])) or (Validate.isPresent(db, Section, data["where_attribute"] , data["where_value"]) and data["update_attribute"]!="course_id"):
				query = db.session.query(Section).filter( getattr(Section , data["where_attribute"]) == data["where_value"]).first()
				setattr(query, data["update_attribute"], data["new_value"])
				db.session.commit()
				response["status"] = "Updated Successfully"
			else:
				response["status"] = "Attribute Not Found or Invalid Attribute"
		else:
			response["status"] = "Attribute does not exist"

	else:
		response["status"] = "Failed to update. Invalid data"

	return response

#	CLASSROOM

@app.route("/classroom/insert", methods = ['POST', 'GET'])
def classroom_insert():
	data = request.get_json()
	data = Lower.toLower(data)
	response = {}
	dataList = ["id", "sec_id", "room_no", "capacity", "build_no"]

	if Validate.json(data, dataList):

		if Validate.isPresent(db,Classroom , "id" , data["id"]) :
			response["status"] = "Section already exists "
		else:

			query = Generate.selectAll(db, Section, "id", data["sec_id"])
			if query:
				record = Classroom(data["id"],data["sec_id"], data["room_no"], data["capacity"], data["build_no"])
				db.session.add(record)
				db.session.commit()
				response["status"] = "Inserted Successfully"
			else:
				response["status"] = "Invalid section ID"
		
	else:
		response["status"] = "Failed to Insert. Invalid data"

	return response

@app.route("/classroom/select" , methods = ["POST" , "GET"])
def classroom_select() :
	data = request.get_json()
	data = Lower.toLower(data)
	response = {}

	if Validate.json(data , ["attribute" , "value"]):

		if hasattr(Classroom , data["attribute"]) or (data["attribute"]==""):
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

@app.route("/classroom/update", methods = ['POST', 'GET'])
def classroom_update():
	data = request.get_json()
	data = Lower.toLower(data)
	response = {}
	if Validate.json(data, ["new_value", "update_attribute", "where_attribute", "where_value"]):
		if hasattr(Classroom, data["update_attribute"]) and (data["update_attribute"]!="id" and data["update_attribute"]!="build_no") :
			if (data["update_attribute"]=="sec_id" and Validate.isPresent(db, Section, "id" , data["new_value"])) or (Validate.isPresent(db, Classroom, data["where_attribute"] , data["where_value"]) and data["update_attribute"]!="sec_id"):
				query = db.session.query(Classroom).filter(getattr(Classroom,data["where_attribute"])== data["where_value"]).first()
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

#	TUTOR

@app.route("/tutor/insert" , methods = ["POST" , "GET" ])
def tutor_insert():
	data = request.get_json()
	data = Lower.toLower(data)
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
	data = Lower.toLower(data)
	response = {}

	if Validate.json(data , ["attribute" , "value"]):

		if hasattr(Tutor , data["attribute"]) or (data["attribute"]==""):
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

@app.route("/tutor/update", methods = ['POST', 'GET'])
def tutor_update():
	data = request.get_json()
	data = Lower.toLower(data)
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

#	TAKES

@app.route("/takes/insert" , methods = ["POST" , "GET" ])
def takes_insert():
	data = request.get_json()
	data = Lower.toLower(data)
	response = {}
	dataList = [ "stud_id","sec_id" , "course_id" , "semester" , "year" , "GPA"]

	if Validate.json(data, dataList):
		query = Generate.selectAll(db, Student, "id", data["stud_id"])
		if query:
			query1 = Generate.selectAll(db, Section, "id", data["sec_id"])
			if query1:
				query2 = Generate.selectAll(db, Course, "id", data["course_id"])
				if query2:
					if data["semester"]>0 and data["year"] > 1950 and data["GPA"] > -1:
						record = Takes(data["stud_id"],data["sec_id"],data["course_id"],data["semester"],data["year"],data["GPA"])
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
			response["status"] = "Invalid Student ID"
	else:
		response["status"] = "Failed to Insert. Invalid data"

	return response

@app.route("/takes/select" , methods = ["POST" , "GET"])
def takes_select() :
	data = request.get_json()
	data = Lower.toLower(data)
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

@app.route("/takes/update", methods = ['POST', 'GET'])
def takes_update():
	data = request.get_json()
	data = Lower.toLower(data)
	response = {}
	if Validate.json(data, ["new_value", "update_attribute", "where_attribute", "where_value"]):
		if hasattr(Takes, data["update_attribute"]) and data["update_attribute"]!="id":
			if (Validate.isPresent(db, Takes, data["where_attribute"] , data["where_value"]) and data["update_attribute"]!="stud_id" and data["update_attribute"]!="course_id" and data["update_attribute"]!="sec_id") or (data["update_attribute"]=="sec_id" and Validate.isPresent(db, Section, "id" , data["new_value"])) or (data["update_attribute"]=="course_id" and Validate.isPresent(db, Course, "id" , data["new_value"])) or (data["update_attribute"]=="stud_id" and Validate.isPresent(db, Student, "id" , data["new_value"])):
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

#	TEACHES

@app.route("/teaches/insert" , methods = ["POST" , "GET" ])
def teaches_insert():
	data = request.get_json()
	data = Lower.toLower(data)
	response = {}
	dataList = ["faculty_id","sec_id" , "course_id" , "semester" , "year"]

	if Validate.json(data, dataList):
		query = Generate.selectAll(db, Faculty, "id", data["faculty_id"])
		if query:
			query1 = Generate.selectAll(db, Section, "id", data["sec_id"])
			if query1:
				query2 = Generate.selectAll(db, Course, "id", data["course_id"])
				if query2:
					if data["semester"]>0 and data["year"] > 1950:
						record = Teaches(data["faculty_id"],data["sec_id"],data["course_id"],data["semester"],data["year"])
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
			response["status"] = "Invalid Faculty ID"
	else:
		response["status"] = "Failed to Insert. Invalid data"

	return response


@app.route("/teaches/select" , methods = ["POST" , "GET"])
def teaches_select() :
	data = request.get_json()
	data = Lower.toLower(data)
	response = {}

	if Validate.json(data , ["attribute" , "value"]):

		if hasattr(Teaches , data["attribute"]) or data["attribute"]=="":
			query = Generate.selectAll(db , Teaches , data["attribute"] , data["value"]) 

			if query :
				response = Generate.tuples(query)
			else:
				response["status"] = "No data found"
		else: 
			response["status"] = "Attribute not found "
	else:
		response["status"] = "No attributes or values"

	return response

@app.route("/teaches/update", methods = ['POST', 'GET'])
def teaches_update():
	data = request.get_json()
	data = Lower.toLower(data)
	response = {}
	if Validate.json(data, ["new_value", "update_attribute", "where_attribute", "where_value"]):
		if hasattr(Teaches, data["update_attribute"]) and data["update_attribute"]!="id":
			if (Validate.isPresent(db, Teaches, data["where_attribute"] , data["where_value"]) and data["update_attribute"]!="faculty_id" and data["update_attribute"]!="course_id" and data["update_attribute"]!="sec_id") or (data["update_attribute"]=="sec_id" and Validate.isPresent(db, Section, "id" , data["new_value"])) or (data["update_attribute"]=="course_id" and Validate.isPresent(db, Course, "id" , data["new_value"])) or (data["update_attribute"]=="faculty_id" and Validate.isPresent(db, Faculty, "id" , data["new_value"])):
				query = db.session.query(Teaches).filter(getattr(Teaches,data["where_attribute"])== data["where_value"]).first()
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

#	TIME_SLOT

@app.route("/time_slot/select" , methods = ["POST" , "GET"])
def time_slot_select() :
	data = request.get_json()
	data = Lower.toLower(data)
	response = {}

	if Validate.json(data , ["attribute" , "value"]):

		if hasattr(Time_slot , data["attribute"]) or (data["attribute"]==""):
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

@app.route("/time_slot/insert", methods = ['POST', 'GET'])
def timeslot_insert():
	data = request.get_json()
	data = Lower.toLower(data)
	response = {}
	dataList = ["sec_id", "slot", "start_time", "end_time" , "day"]

	if Validate.json(data, dataList):
		query = Generate.selectAll(db, Section, "id", data["sec_id"])
		if query:
			
			record = Time_slot(data["sec_id"],data["slot"], data["start_time"], data["end_time"], data["day"])
			db.session.add(record)
			db.session.commit()
			response["status"] = "Inserted Successfully"
		else:
			response["status"] = "Invalid section ID"
		
	else:
		response["status"] = "Failed to Insert. Invalid data"

	return response

@app.route("/time_slot/update", methods = ['POST', 'GET'])
def time_slot_update():
	data = request.get_json()
	data = Lower.toLower(data)
	response = {}
	if Validate.json(data, ["new_value", "update_attribute", "where_attribute", "where_value"]):
		if hasattr(Time_slot, data["update_attribute"]) and (data["update_attribute"]!="id") :
			if (data["update_attribute"]=="sec_id" and Validate.isPresent(db, Section, "id" , data["new_value"])) or (Validate.isPresent(db, Time_slot, data["where_attribute"] , data["where_value"]) and data["update_attribute"]!="sec_id"):
				query = db.session.query(Time_slot).filter(getattr(Time_slot,data["where_attribute"])== data["where_value"]).first()
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

#	MARK

@app.route("/mark/insert" , methods = ["POST" , "GET" ])
def mark_insert():
	data = request.get_json()
	data = Lower.toLower(data)
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
	data = Lower.toLower(data)
	response = {}

	if Validate.json(data , ["attribute" , "value"]):

		if hasattr(Mark , data["attribute"]) or (data["attribute"]==""):
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


@app.route("/mark/update", methods = ['POST', 'GET'])
def mark_update():
	data = request.get_json()
	data = Lower.toLower(data)
	response = {}
	if Validate.json(data, ["update_attribute", "new_value", "where_attribute" , "where_value" ]):

		if hasattr(Mark, data["update_attribute"]) and data["where_attribute"] != "id":
			if (data["update_attribute"]=="stud_id" and Validate.isPresent(db, Student, "stud_id" , data["new_value"])) or (Validate.isPresent(db, Mark, data["where_attribute"] , data["where_value"]) and data["update_attribute"]!="stud_id"):
				query = db.session.query(Mark).filter( getattr(Mark , data["where_attribute"]) == data["where_value"]).first()

				setattr(query, data["update_attribute"], data["new_value"])
				db.session.commit()
				response["status"] = "Updated Successfully"
			else:
				response["status"] = "Attribute Not Found or Invalid Attribute"
		else:
			response["status"] = "Attribute does not exist"

	else:
		response["status"] = "Failed to update. Invalid data"

	return response

#	STUDENT_ATTENDANCE

@app.route("/student_attendance/insert" , methods = ["POST" , "GET" ])
def student_attendance_insert():
	data = request.get_json()
	data = Lower.toLower(data)
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
	data = Lower.toLower(data)
	response = {}

	if Validate.json(data , ["attribute" , "value"]):

		if hasattr(Student_attendance , data["attribute"]) or (data["attribute"]==""):
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

@app.route("/student_attendance/update", methods = ['POST', 'GET'])
def student_attendance_update():
	data = request.get_json()
	data = Lower.toLower(data)
	response = {}
	if Validate.json(data, ["new_value", "update_attribute", "where_attribute", "where_value"]):
		if hasattr(Student_attendance, data["update_attribute"]) and data["update_attribute"]!="id":
			if (data["update_attribute"]=="stud_id" and Validate.isPresent(db, Student, "id" , data["new_value"])) or (Validate.isPresent(db, Student_attendance, data["where_attribute"] , data["where_value"]) and data["update_attribute"]!="stud_id"):
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

#	FACULTY_ATTENDANCE

@app.route("/faculty_attendance/insert" , methods = ["POST" , "GET" ])
def faculty_attendance_insert():
	data = request.get_json()
	data = Lower.toLower(data)
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
	data = Lower.toLower(data)
	response = {}

	if Validate.json(data , ["attribute" , "value"]):

		if hasattr(Faculty_attendance , data["attribute"]) or (data["attribute"]==""):
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

@app.route("/faculty_attendance/update", methods = ['POST', 'GET'])
def faculty_attendance_update():
	data = request.get_json()
	data = Lower.toLower(data)
	response = {}
	if Validate.json(data, ["new_value", "update_attribute", "where_attribute", "where_value"]):
		if hasattr(Faculty_attendance, data["update_attribute"]) and data["update_attribute"]!="id":
			if (data["update_attribute"]=="faculty_id" and Validate.isPresent(db, Faculty, "id" , data["new_value"])) or (Validate.isPresent(db, Faculty_attendance, data["where_attribute"] , data["where_value"]) and data["update_attribute"]!="faculty_id"):
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

#	COURSE

@app.route("/course/insert" , methods = ["POST" , "GET" ])
def course_insert():
	data = request.get_json()
	data = Lower.toLower(data)
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
	data = Lower.toLower(data)
	response = {}

	if Validate.json(data , ["attribute" , "value"]):

		if hasattr(Course , data["attribute"]) or (data["attribute"]==""):
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

@app.route("/course/update", methods = ['POST', 'GET'])
def course_update():
	data = request.get_json()
	data = Lower.toLower(data)
	response = {}
	if Validate.json(data, ["new_value", "update_attribute", "where_attribute", "where_value"]):
		if hasattr(Course, data["update_attribute"]) and data["update_attribute"]!="id":
			query = db.session.query(Course).filter(getattr(Course,data["where_attribute"])== data["where_value"]).first()
			setattr(query, data["update_attribute"], data["new_value"])
			db.session.commit()
			response["status"] = "Updated Successfully"
		else:
			response["status"] = "Cannot Modify . Invalid Entry"
	else:
		response["status"] = "Failed to update. Invalid data"
	return response

#	ADMISSION ENTRY FOR STUDENT

@app.route("/admission/insert", methods = ['POST', 'GET'])
def admission_insert():
	data = request.get_json()
	data = Lower.toLower(data)
	response = {}
	dataList = ["name", "id" , "dept_id", "mum", "dad", "year", "phone", "gender", "email", "sec_id" ,"course_id" , "faculty_id" , "semester" ,"year"] 

	if Validate.json(data, dataList):
		if Validate.email(data["email"]):
			if Validate.isPresent(db, Student, "id", data["id"]):
				response["status"] = "Student ID already exists"
			else:		
				query1 = Generate.selectAll(db, Department, "id", data["dept_id"])
				query4 = Generate.selectAll(db, Course, "id", data["course_id"])
				
				if query1:
					query2 = Generate.selectAll(db, Section, "id", data["sec_id"])
					if query2:
						# name, dept_id, stud_mum, stud_dad, year, phone_no, gender, email
						record = Student(data["id"],data["name"],data["dept_id"],data["sec_id"], data["mum"], data["dad"], data["year"], data["phone"], data["gender"], data["email"])
					else:
						# Default Section is set as 1 
						record = Student(data["id"],data["name"],data["dept_id"],1, data["mum"], data["dad"], data["year"], data["phone"], data["gender"], data["email"])
					db.session.add(record)
					db.session.commit()
			
					query3 = Generate.selectAll(db, Faculty, "id", data["faculty_id"])
					if query3:
						# Entry in Tutor Table	
						record = Tutor(data["id"],data["faculty_id"])
						db.session.add(record)
						db.session.commit()

					else:
						response["status"] = "Inavlid Entry of Section Allocation"
					
					# Entry in Takes Table
					# GPA is intialised to 0
					record = Takes(data["id"],data["sec_id"],data["course_id"],data["semester"],data["year"],0)
					db.session.add(record)
					db.session.commit()

					# Entry in Student_Attendance Table
					record = Student_attendance(data["id"],100,0,0)
					db.session.add(record)
					db.session.commit()
					response["status"] = "Inserted Successfully"

				else:
					response["status"] = "Invalid department Foreign Key Constraint"
		else:
			response["status"] = "Invalid Email"

	else:
		response["status"] = "Failed to Insert. Invalid data"

	return response

@app.route("/hod/access", methods = ['POST', 'GET'])
def hod_access():
	# data = request.get_json()
	response = []
	hodQuery = Generate.selectAll(db, Faculty, "designation", "hod")
	for i in hodQuery:
		lst=[]
		facQuery = Generate.selectAll(db, Faculty, "dept_id", i.dept_id)
		lst.append(i.as_dict())
		# print(i.as_dict())
		for j in facQuery:
			if j.designation != "hod":
				lst.append(j.as_dict())
		response.append(lst)
	# response["status"] = "Invalid Email"
	return response

@app.route("/student_details/access", methods = ['POST', 'GET'])
def student_details_access():
	# data = request.get_json()
	response = []
	stud_query = Generate.selectAll(db, Student, "", "_")
	for i in stud_query:
		#print(i.id,type(i))
		temp=i.as_dict()
		#print(temp)

		attendance_details = Generate.selectOne(db, Student_attendance, "stud_id", i.id)
		if attendance_details:
			temp["total_working_days"] = attendance_details.total_working_days
			temp["total_present"] = attendance_details.total_present
			temp["total_absent"] = attendance_details.total_absent

		mark_details = Generate.selectOne(db, Mark, "stud_id", i.id)
		if mark_details:
			temp["midsem1 mark"] = mark_details.midsem1
			temp["midsem2 mark"] = mark_details.midsem2
			temp["assignment"] = mark_details.assgn
		response.append(temp)

	return response