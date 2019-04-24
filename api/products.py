from flask import Response, jsonify
import json
from flask_restplus import fields

from sales_api.models.orders import Order, OrderDetail
from sales_api.models.products import Product, Category
from sales_api.api.base import BaseListResource, BaseModelResource
from sales_api.api import api

# https://flask-restplus.readthedocs.io/en/stable/swagger.html


ns = api.namespace('products', description='API endpoints related to Products')

product_model = Product.get_api_model(ns)
product_parser = Product.get_default_parser()

@ns.route('/')
class ProductsApi(BaseListResource):
	model = Product
	resource_name = 'Products'

	@api.response(200, 'Success')
	#@api_requires_auth
	@api.expect(product_parser)
	#@api.marshal_list_with(product_model)
	def get(self):
		"""Returns list of Products."""
		return super().get(parser=product_parser)

@ns.route('/<int:id>')
class ProductApi(BaseModelResource):
	model = Product
	resource_name = 'Product'

	@api.doc(param={'ProductNumber': 'Product Number'})
	@api.marshal_with(product_model)
	def get(self, id):
		"""Returns details of a product."""
		return super().get(id)

@ns.route('/<int:id>/vendors')
class ProductVendorsApi(BaseListResource):
	def get(self, id):
		"""Returns all vendors selling a product."""
		product = Product.get_by_id(id)

		if product is None:
			return {
				'status': 'Product with this Id not found',
			}, 404

		results = product.get_vendors()
		if results is None:
			return {
				'status': 'failed',
			}, 404
		else:
			return [item.as_dict() for item in results], 200