from flask import g
from flask_restplus import fields

from sales_api.models.base import BaseModel
from sales_api.models.vendors import Vendor, ProductVendor

class Category(BaseModel):
	table_name = 'categories'
	columns = ['CategoryId', 'CategoryDescription']
	nice_columns = ['CategoryId', 'Description']
	column_types = [int, str]
	id_column = 'CategoryId'

	def get_products(self):
		product_columns = ['p.{}'.format(col) for col in Product.columns]
		columns = []
		columns.extend(product_columns)
		query = """
			SELECT {columns}
			FROM {products_table} as p
			WHERE p.CategoryId = %s;
		""".format(products_table=Product.table_name, columns=', '.join(columns))

		with g.db.cursor() as cursor:
			cursor.execute(query, (self.CategoryId,))
			rows = cursor.fetchall()
			results = []
			for row in rows:
				results.append(Product._instance_factory(row))
			return results

class Product(BaseModel):
	table_name = 'products'
	columns = ['ProductNumber', 'ProductName', 'ProductDescription',
			'RetailPrice', 'QuantityOnHand', 'CategoryId']
	nice_columns = ['ProductNumber', 'Name', 'Description', 'RetailPrice', 'QuantityOnHand', 'CategoryId']
	column_types = [int, str, str, float, int, int]
	id_column = 'ProductNumber'

	def get_vendors(self):
		vendor_columns = ['v.{}'.format(col) for col in Vendor.columns]
		columns = []
		columns.extend(vendor_columns)
		columns.append('pv.WholesalePrice')
		columns.append('pv.DaysToDeliver')
		query = """
			SELECT {columns}
			FROM {vendors_table} as v
			JOIN {product_vendors_table} as pv ON v.VendorId = pv.VendorId
			JOIN {products_table} as p ON p.ProductNumber = pv.ProductNumber
			WHERE p.ProductNumber = %s;
		""".format(columns=', '.join(columns),
					vendors_table=Vendor.table_name,
					product_vendors_table=ProductVendor.table_name,
					products_table=Product.table_name)

		with g.db.cursor() as cursor:
			cursor.execute(query, (self.ProductNumber,))
			rows = cursor.fetchall()
			results = []
			for row in rows:
				results.append(VendorProductInfo._instance_factory(row))
			return results

	@classmethod
	def get_bestselling(cls):
		columns = ['p.ProductNumber', 'p.ProductName', 'SUM(od.QuantityOrdered)']
		query = """
			SELECT {columns}
			FROM {products_table} AS p
			JOIN {order_details_table} AS od ON p.ProductNumber = od.ProductNumber
			GROUP BY p.ProductNumber
			ORDER BY SUM(od.QuantityOrdered) DESC;
		""".format(columns=', '.join(columns),
					products_table=Product.table_name,
					order_details_table=OrderDetail.table_name)
		# Note: products which were not sold at all do not show up in the result list!

		with g.db.cursor() as cursor:
			cursor.execute(query)
			rows = cursor.fetchall()
			results = []
			for row in rows:
				res = {}
				res['ProductNumber'] = int(row[0])
				res['ProductName'] = row[1]
				res['Ordered in Total'] = int(row[2])
				results.append(res)
			return results