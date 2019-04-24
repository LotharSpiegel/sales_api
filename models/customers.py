from flask import g
from flask_restplus import fields
from sales_api.models.base import BaseModel
from sales_api.models.orders import Order, OrderDetail, OrderInfo
from sales_api.models.products import Product
from sales_api.api import api

class Customer(BaseModel):
	table_name = 'customers'
	columns = ['CustomerId', 'CustLastName', 'CustFirstName', 'CustStreetAddress', 'CustCity',
			'CustState', 'CustZipCode', 'CustAreaCode', 'CustPhoneNumber']
	nice_columns = ['CustomerId', 'LastName', 'FirstName', 'StreetAddress', 'City',
			'State', 'ZipCode', 'AreaCode', 'PhoneNumber']
	column_types = [int, str, str, str, str,
			str, str, int, str]
	id_column = 'CustomerId'

	max_values = [None, 25, 25, 50, 30,
			2, 10, None, 8]


	# @classmethod
	# def create(cls, args):
	# 	columns = []
	# 	params = []
	# 	kwargs = {}
	# 	if cls.id_column in args.keys():
	# 		del args[cls.id_column]
	# 	for key, value in args.items():
	# 		column_name = cls.nice_column_to_column(key)
	# 		kwargs[column_name] = value
	# 		columns.append(column_name)
	# 		params.append(cls.adjust_param(column_name=column_name, param=value))
	# 	query = """
	# 		INSERT INTO {table_name}
	# 		({columns})
	# 		VALUES ({params})
	# 		RETURNING
	# 		{id_column};
	# 	""".format(table_name=cls.table_name,
	# 			columns=', '.join(columns),
	# 			params=', '.join(params),
	# 			id_column=cls.id_column)

	# 	with g.db.cursor() as cursor:
	# 		try:
	# 			cursor.execute(query, params)
	# 			g.db.commit()
	# 			id = cursor.fetchone()[0]
	# 			kwargs[cls.id_column] = id
	# 			return cls(**kwargs)
	# 		except psycopg2.Error as e:
	# 			# if e.pgcode == errorcodes.UNIQUE_VIOLATION:
	# 			raise e


	def get_orders(self):
		order_columns = ['o.{}'.format(col) for col in Order.columns]
		columns = []
		columns.extend(order_columns)
		columns.append('od.ProductNumber')
		columns.append('od.QuotedPrice')
		columns.append('od.QuantityOrdered')
		columns.append('p.ProductName')
		query = """
			SELECT {columns}
			FROM {orders_table} as o
			JOIN {order_details_table} as od ON o.OrderNumber = od.OrderNumber
			JOIN {products_table} as p ON p.ProductNumber = od.ProductNumber
			WHERE o.CustomerId = %s;
		""".format(columns=', '.join(columns),
					orders_table=Order.table_name,
					order_details_table=OrderDetail.table_name,
					products_table=Product.table_name)

		with g.db.cursor() as cursor:
			cursor.execute(query, (self.CustomerId,))
			rows = cursor.fetchall()
			results = []
			for row in rows:
				results.append(OrderInfo._instance_factory(row))
			return results