from flask import Response, jsonify
import json
from flask_restplus import fields
from flask_restful import abort
from sales_api.models.customers import Customer
from sales_api.models.orders import Order
from sales_api.models.employees import Employee
from sales_api.api.base import BaseListResource, BaseModelResource
from sales_api.api import api

# https://flask-restplus.readthedocs.io/en/stable/swagger.html


ns = api.namespace('employees', description='API endpoints related to Employees')

employee_model = Employee.get_api_model(ns)
employee_parser = Employee.get_default_parser()
# customer_model = ns.model('Customer', {
# 	#"CustomerId": fields.String(description="Customer Id",)
# 	"LastName": fields.String(description="Last name", required=True),
# })

@ns.route('/')
class EmployeesApi(BaseListResource):
	model = Employee
	resource_name = 'Employee'

	@api.response(200, 'Success')
	#@api_requires_auth
	@api.expect(employee_parser)
	#@api.marshal_list_with(employee_model)
	def get(self):
		"""Returns list of Employees."""
		return super().get(parser=employee_parser)

	@api.response(201, 'Successfully created new Employee.')
	@api.response(409, 'Creating a new Employee failed.')
	@api.expect(employee_model)
	def post(self):
		"""Creates a new Employee."""
		#parser = reqparse.RequestParser()
		#parser.add_argument('')

		self.init_parser()
		if self.parser is None:
			return None
		args = self.parser.parse_args()

		try:
			print('\nargs', args)
			new_employee = Employee.create(args)
		except Exception as e:
			import sys, traceback
			traceback.print_tb(sys.exc_info()[2])
			abort(409, message="Creating a new Employee failed.",
				error=str(e))
		response = jsonify(new_employee.as_dict())
		#jsonify()
		response.status_code = 201
		return response

@ns.route('/<int:id>')
class EmployeeApi(BaseModelResource):
	model = Employee
	resource_name = 'Employee'

	#@api.response(200, 'Success', Employee)
	@api.doc(param={'EmployeeId': 'Employee Id'})
	@api.marshal_with(employee_model)
	def get(self, id):
		"""Returns details of a Employee."""
		return super().get(id)

	# @api.response(204, 'Employee successfully updated.')
	# def put(self):
	# 	"""Updates a Employee's details."""
	# 	return super().put(request.json)

@ns.route('/<int:id>/orders')
class OrdersManagedByEmployeeApi(BaseListResource):
	resource_name = 'Orders made by Employee'

	def get(self, id):
		"""Returns all orders managed by an employee."""
		employee = Employee.get_by_id(id)

		if employee is None:
			return {
				'status': 'Employee with this Id not found',
			}, 404

		results = employee.get_orders()
		if results is None:
			return {
				'status': 'failed',
			}, 404
		else:
			return [item.as_dict() for item in results], 200