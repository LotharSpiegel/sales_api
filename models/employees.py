
from flask import g
from flask_restplus import fields
from sales_api.models.base import BaseModel
from sales_api.models.orders import Order, OrderInfo, OrderDetail
from sales_api.models.products import Product

class Employee(BaseModel):
	table_name = 'employees'
	columns = ['EmployeeId', 'EmpLastName', 'EmpFirstName', 'EmpStreetAddress',
			'EmpCity', 'EmpState', 'EmpZipCode', 'EmpAreaCode',
			'EmpPhoneNumber', 'EmpDob', 'ManagerId']
	nice_columns = ['EmployeeId', 'LastName', 'FirstName', 'StreetAddress',
			'City', 'State', 'ZipCode', 'AreaCode',
			'PhoneNumber', 'BirthDate', 'ManagerId']
	column_types = [int, str, str, str,
			str, str, str, int,
			str, str, int]
	id_column = 'EmployeeId'


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
			WHERE o.EmployeeId = %s;
		""".format(columns=', '.join(columns),
					orders_table=Order.table_name,
					order_details_table=OrderDetail.table_name,
					products_table=Product.table_name)

		with g.db.cursor() as cursor:
			cursor.execute(query, (self.EmployeeId,))
			rows = cursor.fetchall()
			results = []
			for row in rows:
				results.append(OrderInfo._instance_factory(row))
			return results