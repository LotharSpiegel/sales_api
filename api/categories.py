from flask import Response, jsonify
import json
from flask_restplus import fields, abort

from sales_api.models.orders import Order, OrderDetail
from sales_api.models.products import Product, Category
from sales_api.api.base import BaseListResource, BaseModelResource
from sales_api.api import api

ns = api.namespace('categories', description='API endpoints related to product categories')

category_model = Category.get_api_model(ns)
category_parser = Category.get_default_parser()

@ns.route('/')
class CategoriesApi(BaseListResource):
	model = Category

	@api.response(200, 'Success')
	@api.expect(category_parser)
	#@api.marshal_list_with(category_model)
	def get(self):
		"""Returns list of product categories."""
		return super().get(parser=category_parser)

	@api.response(201, 'Successfully created new Category.')
	@api.response(409, 'Creating a new Category failed.')
	@api.expect(category_model)
	def post(self):
		"""Creates a new Category."""
		args = category_parser.parse_args()
		# data = request.json
		try:
			new_category = Category.create(args)
		except Exception as e:
			import sys, traceback
			traceback.print_tb(sys.exc_info()[2])
			abort(409, message="Creating a new Category failed.",
				error=str(e))
			#return None, 409

		response = jsonify(new_category.as_dict())
		response.status_code = 201
		return response

@ns.route('/<int:id>')
@api.response(404, 'Category not found.')
class CategoryApi(BaseModelResource):
	model = Category

	@api.doc(param={'CategoryId': 'Category Id'})
	@api.marshal_with(category_model)
	def get(self, id):
		"""Returns details of a product category."""
		return super().get(id)

	@api.expect(category_model)
	#@api.marshal_with(category_model)
	@api.response(204, 'Category successfully updated.')
	@api.response(409, 'Updating the Category failed.')
	def put(self, id):
		"""Updates a product category."""
		#super().update(id)

		args = category_parser.parse_args()
		# data = request.json
		try:
			#print('\nargs', args)
			category = Category.update(id=id, args=args)
		except Exception as e:
			import sys, traceback
			traceback.print_tb(sys.exc_info()[2])
			abort(409, message="Updating the Category failed.",
				error=str(e))
			#return None, 409

		response = jsonify(category.as_dict())
		response.status_code = 204
		return response

@ns.route('/<int:id>/products')
class CategoryProductsApi(BaseListResource):

	@api.doc(param={'CategoryId': 'Category Id'})
	def get(self, id):
		"""Returns all products of a category."""
		category = Category.get_by_id(id)

		if category is None:
			return {
				'status': 'Category with this Id not found',
			}, 404

		results = category.get_products()
		if results is None:
			return {
				'status': 'failed',
			}, 404
		else:
			return [item.as_dict() for item in results], 200