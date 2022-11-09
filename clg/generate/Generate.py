def select(db, table, attribute, value):
	return db.session.query(table).filter(getattr(table, attribute) == value).first()
