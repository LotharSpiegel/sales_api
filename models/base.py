from flask import g
from flask_restplus import fields, reqparse
import psycopg2

class BaseModel:
	table_name = ''
	columns = []
	nice_columns = []
	column_types = []
	id_column = ''

	def __init__(self, **kwargs):
		for column in self.__class__.columns:
			setattr(self, column, kwargs.get(column, None))

	# https://flask-restplus.readthedocs.io/en/stable/parsing.html
	@classmethod
	def get_default_parser(cls):
		parser = reqparse.RequestParser()
		for i, col in enumerate(cls.nice_columns):
			if cls.columns[i] != cls.id_column:
				parser.add_argument(col, type=cls.column_types[i], required=False)
		return parser

	@classmethod
	def get_api_model(cls, name_space):
		_fields = {}
		if hasattr(cls, 'max_values'):
			for i, col in enumerate(cls.nice_columns):
				if cls.columns[i] == cls.id_column:
					continue
				if cls.column_types[i] == str:
					_fields[col] = fields.String(description=col,
										max_length=cls.max_values[i], required=False)
				elif cls.column_types[i] == int:
					_fields[col] = fields.Integer(description=col,
										max=cls.max_values[i], required=False)
				elif cls.column_types[i] == float:
					_fields[col] = fields.Float(description=col,
										max=cls.max_values[i], required=False)
		else:
			for i, col in enumerate(cls.nice_columns):
				if cls.columns[i] == cls.id_column:
					continue
				if cls.column_types[i] == str:
					_fields[col] = fields.String(description=col, required=False)
				elif cls.column_types[i] == int:
					_fields[col] = fields.Integer(description=col, required=False)
				elif cls.column_types[i] == float:
					_fields[col] = fields.Float(description=col, required=False)
		return name_space.model(cls.__name__, _fields)

	@classmethod
	def get_column_type(cls, column_name):
		# handle index errors..
		return cls.column_types[cls.columns.index(column_name)]

	@classmethod
	def nice_column_to_column(cls, nice_column_name):
		index = cls.nice_columns.index(nice_column_name)
		return cls.columns[index]

	@classmethod
	def adjust_param(cls, column_name, param):
		if param is None:
			return 'NULL'
		column_type = cls.get_column_type(column_name)
		if column_type == str:
			return '\'{}\''.format(str(param))
		else:
			return str(param)

	def as_dict(self):
		d = {}
		for i, column in enumerate(self.__class__.columns):
			value = getattr(self, column, None)
			d[self.__class__.nice_columns[i]] = self.column_types[i](value) if value else None
		return d

	@classmethod
	def _instance_factory(cls, row):
		kwargs = {}
		for i, column in enumerate(cls.columns):
			kwargs[column] = row[i]
		print('kwargs', kwargs)
		return cls(**kwargs)

	@classmethod
	def _fetchall(cls, cursor):
		rows = cursor.fetchall()
		results = []
		for row in rows:
			results.append(cls._instance_factory(row))
		return results

	@classmethod
	def get_all(cls):
		query = """
			SELECT {columns}
			FROM {table_name};
		""".format(columns=', '.join(cls.columns),
					table_name=cls.table_name)

		with g.db.cursor() as cursor:
			print(query)
			cursor.execute(query)
			results = cls._fetchall(cursor)
			#print(results)
			return results

	@classmethod
	def get_by_id(cls, id):
		if cls.id_column is None:
			return None

		query = """
			SELECT {columns}
			FROM {table_name}
			WHERE {id_column} = %s;
		""".format(columns=', '.join(cls.columns),
					table_name=cls.table_name,
					id_column=cls.id_column)

		print(query)

		with g.db.cursor() as cursor:
			cursor.execute(query, (id,))
			row = cursor.fetchone()
			if row is None:
				return None
			return cls._instance_factory(row)

	@classmethod
	def filter(cls, **kwargs):
		filters = []
		args = []
		for key, value in kwargs.items():

			filters.append('{} = %s'.format(key))
			args.append(value)
		if len(filters) > 0:
			where_clause = ' AND '.join(filters)
		else:
			return cls.get_all()

		query = """
			SELECT {columns}
			FROM {table_name}
			WHERE {where_clause};
		""".format(columns=', '.join(cls.columns),
				table_name=cls.table_name,
				where_clause=where_clause)

		with g.db.cursor() as cursor:
			cursor.execute(query, args)
			return cls._fetchall(cursor)

	@classmethod
	def update(cls, id, args):
		#columns = []
		#params = []
		kwargs = {}
		set_dict = {}
		if cls.id_column in args.keys():
			del args[cls.id_column]
		for key, value in args.items():
			column_name = cls.nice_column_to_column(key)
			kwargs[column_name] = value
			#columns.append(column_name)
			#params.append()
			set_dict[column_name] = cls.adjust_param(column_name=column_name, param=value)
		set_strings = ['{column_name}={value}'.format(
						column_name=key, value=value) for key, value in set_dict.items()]
		updates = ', '.join(set_strings)
		where_clause = '{id_column}={id_value}'.format(id_column=cls.id_column, id_value=id)
		query = """
			UPDATE {table_name}
			SET {updates}
			WHERE {where_clause};
		""".format(table_name=cls.table_name,
				updates=updates,
				where_clause=where_clause)
		print(query)
		with g.db.cursor() as cursor:
			try:
				cursor.execute(query)#, params)
				g.db.commit()
				kwargs[cls.id_column] = id
				return cls(**kwargs)
			except psycopg2.Error as e:
				# if e.pgcode == errorcodes.UNIQUE_VIOLATION:
				raise e

	@classmethod
	def create(cls, args):
		columns = []
		params = []
		kwargs = {}
		if cls.id_column in args.keys():
			del args[cls.id_column]
		for key, value in args.items():
			column_name = cls.nice_column_to_column(key)
			kwargs[column_name] = value
			columns.append(column_name)
			params.append(cls.adjust_param(column_name=column_name, param=value))
		query = """
			INSERT INTO {table_name}
			({columns})
			VALUES ({params})
			RETURNING
			{id_column};
		""".format(table_name=cls.table_name,
				columns=', '.join(columns),
				params=', '.join(params),
				id_column=cls.id_column)
		print(query)
		with g.db.cursor() as cursor:
			try:
				cursor.execute(query) # params
				g.db.commit()
				id = cursor.fetchone()[0]
				kwargs[cls.id_column] = id
				return cls(**kwargs)
			except psycopg2.Error as e:
				# if e.pgcode == errorcodes.UNIQUE_VIOLATION:
				raise e