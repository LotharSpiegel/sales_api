from flask import Response, jsonify
import json
from flask_restplus import fields, reqparse
from flask_restful import abort
from sales_api.models.customers import Customer
from sales_api.models.orders import Order
from sales_api.api.base import BaseListResource, BaseModelResource
from sales_api.api import api

# https://flask-restplus.readthedocs.io/en/stable/swagger.html


ns = api.namespace('customers', description='API endpoints related to Customers')

customer_model = Customer.get_api_model(ns)
customer_parser = Customer.get_default_parser()


@ns.route('/')
class CustomersApi(BaseListResource):
	model = Customer
	resource_name = 'Customers'

	@api.response(200, 'Success')
	#@api_requires_auth
	@api.expect(customer_parser)
	#@api.marshal_list_with(customer_model) customer_model has no Id..
	def get(self):
		"""Returns list of Customers."""
		return super().get(parser=customer_parser)

	@api.response(201, 'Successfully created new Customer.')
	@api.response(409, 'Creating a new Customer failed.')
	@api.expect(customer_model)
	def post(self):
		"""Creates a new Customer."""
		args = customer_parser.parse_args()
		# data = request.json
		try:
			#print('\nargs', args)
			new_customer = Customer.create(args)
		except Exception as e:
			import sys, traceback
			traceback.print_tb(sys.exc_info()[2])
			abort(409, message="Creating a new Customer failed.",
				error=str(e))
			#return None, 409

		response = jsonify(new_customer.as_dict())
		response.status_code = 201
		return response

@ns.route('/<int:id>')
class CustomerApi(BaseModelResource):
	model = Customer
	resource_name = 'Customer'

	#@api.response(200, 'Success', Customer)
	@api.doc(param={'CustomerId': 'Customer Id'})
	@api.marshal_with(customer_model)#Customer.api_model)#Customer.api_model
	def get(self, id):
		"""Returns details of a customer."""
		return super().get(id)

	# @api.response(204, 'Customer successfully updated.')
	# def put(self):
	# 	"""Updates a customer's details."""
	# 	return super().put(request.json)

	#def delete(self, id):

@ns.route('/<int:id>/orders')
class OrdersMadeByCustomerApi(BaseListResource):
	resource_name = 'Orders made by Customer'

	def get(self, id):
		"""Returns all orders made by a customer"""
		customer = Customer.get_by_id(id)

		if customer is None:
			return {
				'status': 'Customer with this Id not found',
			}, 404

		results = customer.get_orders()
		if results is None:
			return {
				'status': 'failed',
			}, 404
		else:
			return [item.as_dict() for item in results], 200