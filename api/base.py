#from flask_restful import abort
from flask_restplus import Resource, reqparse
from flask import request

#from sale.api import api

class BaseListResource(Resource):
	model = None

	# def init_parser(self):
	# 	if self.model is None:
	# 		self.parser = None
	# 	else:
	# 		self.parser = reqparse.RequestParser()
	# 		for i, col in enumerate(self.model.nice_columns):
	# 			self.parser.add_argument(col, type=self.model.column_types[i])#, location='form')
	# 		return

	# @classmethod
	# def get_default_parser(cls):
	# 	if cls.model is None:
	# 		return None
	# 	else:
	# 		parser = reqparse.RequestParser()
	# 		for i, col in enumerate(cls.model.nice_columns):
	# 			# required=False, help=,choices=..
	# 			parser.add_argument(col, type=cls.model.column_types[i])#, location='form')
	# 		return parser

	def get(self, parser=None):
		#if not hasattr(self, 'parser'):
		#	self.init_parser()
		if parser is None:
			results = self.model.get_all()
		else:
			args = parser.parse_args()
			print('args', args)
			kwargs = {}
			num_args = 0
			for i, col in enumerate(self.model.nice_columns):
				value = args.get(col, None)
				if value is not None:
					kwargs[self.model.columns[i]] = value
					num_args += 1
			# print('num_args', num_args)
			# if num_args == 0:
			# 	results = self.model.get_all()
			# else:
			# 	results = self.model.filter(**kwargs)
			results = self.model.filter(**kwargs)

		if results is None:
			return {
				'status': 'failed',
			}, 404
		else:
			return [item.as_dict() for item in results], 200

class BaseModelResource(Resource):
	model = None
	resource_name = 'BaseModelResource'

	#@api.response(200, 'Success', model)
	#@api.header('Authorization', 'JWT Token', required=True)

	def get(self, id):
		#q = db.session.query(Customer).filter(Customer.customerid == customer_id)
		#q = Customer.query.get(customer_id)
		#Customer.query.filter(Customer.customerid == customer_id)
		#print(q)
		#q = Customer.query.get(customerid=customer_id)

		item = self.model.get_by_id(id)
		if item is None:
			return {
				'status': '{resource_name} with this Id not found'.format(resource_name=self.resource_name),
			}, 404
		# last_name = customer.custlastname

		return {
			#'status': 'success',
			**item.as_dict(),
		}, 200

	# def put(self, id):
	# 	item = self.model.get_by_id(id)
	# 	if item is None:
	# 		return {
	# 			'status': '{resource_name} with this Id not found'.format(resource_name=self.resource_name),
	# 		}, 404

	# 	return None, 204