from flask import g
from flask_restplus import fields

from sales_api.models.base import BaseModel
#from sale.api.api import api

class Order(BaseModel):
	table_name = 'orders'
	columns = ['OrderNumber', 'OrderDate', 'ShipDate', 'CustomerId', 'EmployeeId', 'OrderTotal']
	nice_columns = ['OrderNumber', 'OrderDate', 'ShipDate', 'CustomerId', 'EmployeeId', 'OrderTotal']
	column_types = [int, str, str, int, int, float]
	id_column = 'OrderNumber'

class OrderDetail(BaseModel):
	"""An m2m junction table between orders(OrderNumber) and products(ProductNumber)"""
	table_name = 'order_details'
	columns = ['OrderNumber', 'ProductNumber', 'QuotedPrice', 'QuantityOrdered']
	nice_columns = ['OrderNumber', 'ProductNumber', 'QuotedPrice', 'QuantityOrdered']
	column_types = [int, int, float, int]
	id_column = None


class OrderInfo:
	def __init__(self, order, QuotedPrice, QuantityOrdered, ProductName):
		self.order = order
		self.QuotedPrice = QuotedPrice
		self.QuantityOrdered = QuantityOrdered
		self.ProductName = ProductName

	@classmethod
	def _instance_factory(cls, row):
		order_row = row[:-3]
		order = Order._instance_factory(order_row)
		return cls(order=order, QuotedPrice=row[-3], QuantityOrdered=row[-2], ProductName=row[-1])

	def as_dict(self):
		d = {}
		d.update(self.order.as_dict())
		d['QuotedPrice'] = float(self.QuotedPrice)
		d['QuantityOrdered'] = int(self.QuantityOrdered)
		d['ProductName'] = self.ProductName
		return d