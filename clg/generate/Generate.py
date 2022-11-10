def select(db, table, attribute, value):
	return db.session.query(table).filter(getattr(table, attribute) == value).all()

def count(query):
	count = 0
	for i in query:
		count += 1
	return count

def tuples(query):
	response = {}
	i= 1
	for q in query:
		temp = "{0}".format(i)
		print(type(q.__dict__))
		response[temp] = q.as_dict()
		i += 1
	response["count"] = count(query)
	return response
