from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    

class Student(db.Model):

	__tablename__ = "student"

	id = db.Column(db.Integer, primary_key = True)
	stud_name = db.Column(db.String(100))
	sec_id = db.Column(db.Integer, db.ForeignKey("section.id"))
	dept_id = db.Column(db.Integer, db.ForeignKey("department.id"))
	stud_mum = db.Column(db.String(100))
	stud_dad = db.Column(db.String(100))
	year = db.Column(db.Integer)
	phone_no = db.Column(db.String(100))
	gender = db.Column(db.String(10))
	email = db.Column(db.String(100))


	#department = db.relationship("Department", back_populates="student")

	def __init__(self,id, name, dept_id, sec_id, stud_mum, stud_dad, year, phone_no, gender, email):
		self.id = id
		self.stud_name = name
		self.sec_id = sec_id
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

	def __init__(self, id, sec_id, room_no, capacity,build_no) -> None:
		self.id = id
		self.sec_id = sec_id
		self.room_no = room_no
		self.capacity = capacity
		self.build_no = build_no
		
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
 
class Takes(db.Model):
    
    __tablename__ = "takes"
    
    id = db.Column(db.Integer, primary_key = True)
    stud_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    sec_id = db.Column(db.Integer, db.ForeignKey("section.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.id")) 
    semester = db.Column(db.Integer)
    year = db.Column(db.Integer)
    GPA = db.Column(db.Float)
    
    def __init__(self, stud_id , sec_id, course_id, semester, year, GPA) -> None:
        self.stud_id = stud_id
        self.sec_id = sec_id
        self.course_id = course_id
        self.semester = semester
        self.year = year
        self.GPA = GPA
    
    def as_dict(self):
	    return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class Teaches(db.Model):
    
    __tablename__ = "teaches"
    
    id = db.Column(db.Integer, primary_key = True)
    faculty_id = db.Column(db.Integer , db.ForeignKey("faculty.id"))
    sec_id = db.Column(db.Integer, db.ForeignKey("section.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
    semester = db.Column(db.Integer)
    year = db.Column(db.Integer)
    
    def __init__(self,faculty_id, sec_id, course_id, semester, year) -> None:
        self.sec_id = sec_id
        self.faculty_id = faculty_id
        self.course_id = course_id
        self.semester = semester
        self.year = year
    
    def as_dict(self):
	    return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
