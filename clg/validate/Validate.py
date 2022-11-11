import re
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def email(e):
	if(re.fullmatch(regex, e)):
		return True
	return False
def json(data, dataList):
	for i in dataList:
		if i not in data:
			return False
	return True

def isPresent(db, table, attribute, value):
	return bool(db.session.query(table).filter(getattr(table, attribute) == value).first())
