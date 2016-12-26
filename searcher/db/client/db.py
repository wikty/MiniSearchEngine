import sqlite3
from .db_config import SQLiteDBConfig

class SQLiteDB(object):
	def __init__(self, config={}):
		self.sqlite_file = SQLiteDBConfig['db']
		self.debug = SQLiteDBConfig['debug']
		if config:
			if config.get('db', None) is not None:
				self.sqlite_file = config.get('db')
			if config.get('debug', None) is not None:
				self.debug = config.get('debug')
		self.client = sqlite3.connect(self.sqlite_file)

	def __del__(self):
		self.client.close()

	def close(self):
		self.client.close()

	def sql(self, q):
		cursor = self.client.cursor()
		results = cursor.execute(q)
		self.client.commit()
		return results

	def create_table(self, tbl_name, fields, extra=''):
		'''
			fields = {'field_name': 'field_type'}
		'''
		cursor = self.client.cursor()

		sql = 'CREATE TABLE IF NOT EXISTS {table} ({fields})'
		fds = ['id INTEGER PRIMARY KEY AUTOINCREMENT']
		for field_name, field_type in fields.items():
			if field_type == 'i':
				field_name = '%s INTEGER' % field_name
			elif field_type == 'f':
				field_name = '%s FLOAT' % field_name
			elif field_type == 'S':
				field_name = '%s TEXT' % field_name
			else:
				field_name = '%s VARCHAR(255)' % field_name
			fds.append(field_name)
		if extra:
			fds.append(extra)
		sql = sql.format(table=tbl_name, fields=', '.join(fds))
		
		if self.debug:
			print('SQL:', sql)
		
		cursor.execute(sql)
		self.client.commit()

	def select_table(self, tbl_name, fields=[], where_condition=''):
		'''
			fields = [name1, name2,...]
		'''
		cursor = self.client.cursor()
		if fields:
			fields = ', '.join(fields)
		else:
			fields = '*'
		sql = 'SELECT {fields} FROM {table}'.format(table=tbl_name, fields=fields)

		if where_condition:
			sql += ' WHERE {condition}'.format(condition=where_condition)

		if self.debug:
			print('SQL:', sql)

		results = cursor.execute(sql)
		return [row for row in results]

	def count_table(self, tbl_name, where={}):
		'''
			where = {'field_name': '>30'}
		'''
		cursor = self.client.cursor()
		if where:
			where = ' '.join([field_name+where[field_name] for field_name in where])
		else:
			where = ''

		sql = 'SELECT COUNT(*) FROM {table}'.format(table=tbl_name)
		if where:
			sql += ' WHERE {where}'.format(where=where)

		if self.debug:
			print('SQL:', sql)

		cursor.execute(sql)
		result = cursor.fetchone()
		return result[0] if result else None

	def insert_table(self, tbl_name, fields={}):
		'''
			fields = {'field_name': 'field_value'}
		'''
		cursor = self.client.cursor()

		sql = 'INSERT INTO {table} ({keys}) VALUES ({values})'
		sql = sql.format(
			table=tbl_name,
			keys= ', '.join(fields.keys()),
			values=', '.join(['?']*len(fields.keys()))
		)
		
		if self.debug:
			print('SQL:', sql)

		cursor.execute(sql, list(fields.values()))
		self.client.commit()
		return cursor.lastrowid

	def delete_table(self, tbl_name):
		cursor = self.client.cursor()

		sql = 'DROP TABLE IF EXISTS {table}'.format(table=tbl_name)

		if self.debug:
			print('SQL:', sql)

		cursor.execute(sql)
		self.client.commit()

	def update_table(self, tbl_name, fields, where_condition=''):
		'''
			fields = {
				'field_name': 'field_value', # assign to the field
				'field_name': '++field_value' # add into the field
			}

			where_condition = 'username="wikty"'
		'''
		cursor = self.client.cursor()

		fds = []
		for field_name, field_value in fields.items():
			field_name = str(field_name)
			field_value = str(field_value)
			if field_value.startswith('++'):
				fds.append(field_name+'='+field_name+'+'+field_value[2:])
			else:
				fds.append(field_name+'='+field_value)
		sql = 'UPDATE {table} SET {fields}'.format(
			table=tbl_name,
			fields=' '.join(fds)
		)
		
		if where_condition:
			sql += ' WHERE {condition}'.format(condition=where_condition)
		
		if self.debug:
			print('SQL:', sql)

		cursor.execute(sql)
		self.client.commit()
		return cursor.rowcount

	# def increment_table(self, tbl_name, field_name, , n=1):
	# 	'''
	# 		field_name = 'age'
	# 		equal_condition = ['another_field_name', 'value']
	# 	'''
	# 	cursor = self.client.cursor()

	# 	sql = 'SELECT {field} FROM {table} WHERE {condition}'.format(
	# 		table=tbl_name,
	# 		field=field_name,
	# 		condition=where_condition
	# 	)

	# 	cursor.execute(sql)
	# 	result = cursor.fetchone()
	# 	count = result[0] if result else None

	# 	if count is None:
	# 		fields = {}
	# 		fields[field_name] = n
	# 		self.insert_table(tbl_name, fields)
	# 	else:
	# 		n = count+n
	# 		sql = 'UPDATE {table} SET {field} = {n} WHERE {field}{condition}'.format(
	# 			table=tbl_name,
	# 			field=field_name,
	# 			condition=where_condition,
	# 			n=n
	# 		)
	# 		cursor.execute(sql)
	# 		self.client.commit()
	# 	return n