from flask import Response, jsonify
import json
from flask_restplus import fields

from sales_api.models.orders import Order, OrderDetail
from sales_api.api.base import BaseListResource, BaseModelResource
from sales_api.api import api

# https://flask-restplus.readthedocs.io/en/stable/swagger.html


ns = api.namespace('orders', description='API endpoints related to Orders')

order_model = Order.get_api_model(ns)
order_parser = Order.get_default_parser()

@ns.route('/')
class OrdersApi(BaseListResource):
	model = Order
	resource_name = 'Orders'

	@api.response(200, 'Success')
	#@api_requires_auth
	@api.expect(order_parser)
	#@api.marshal_list_with(order_model)
	def get(self):
		"""Returns list of Orders."""
		return super().get(parser=order_parser)

@ns.route('/<int:id>')
class OrderApi(BaseModelResource):
	model = Order
	resource_name = 'Order'

	@api.doc(param={'OrderId': 'Order Id'})
	@api.marshal_with(order_model)
	def get(self, id):
		"""Returns details of an Order."""
		return super().get(id)

@ns.route('/<int:id>/details')
class OrderDetailsApi(BaseListResource):
	model = OrderDetail
	resource_name = 'OrderDetails'