def selectAll(db, table, attribute, value):
	if(attribute == ""):
		return db.session.query(table).all()
	return db.session.query(table).filter(getattr(table, attribute) == value).all()

def selectOne(db, table, attribute, value):
	return db.session.query(table).filter(getattr(table, attribute) == value).first()

def tuples(query):
	response = []
	for q in query:
		response.append(q.as_dict())
	return response
