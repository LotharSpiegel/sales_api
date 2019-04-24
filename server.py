from flask import Flask, g, Blueprint
import markdown
import os
import psycopg2

from config import DevelopmentConfig, Config
from sales_api.api import api
from sales_api.api.categories import ns as categories_namespace
from sales_api.api.customers import ns as customers_namespace
from sales_api.api.employees import ns as employees_namespace
from sales_api.api.orders import ns as orders_namespace
from sales_api.api.products import ns as products_namespace

#from resources import *#CustomerApi, CustomersApi, OrderApi, OrdersApi

app = Flask(__name__)

def initialize_app_and_api(app):
	app.config.from_object(DevelopmentConfig)
	api_v1_blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')
	#_api = Api(api_v1)
	api.init_app(api_v1_blueprint)

	#api = swagger.docs(_api, apiVersion='0.1')
	#add_api_resources(api)
	add_api_namespaces(api)
	app.register_blueprint(api_v1_blueprint)


def add_api_namespaces(api):
	api.add_namespace(customers_namespace)
	api.add_namespace(orders_namespace)
	api.add_namespace(employees_namespace)
	api.add_namespace(products_namespace)
	api.add_namespace(categories_namespace)
#api = Api(app)

#base_url = '/sales/api/v1.0'
#def add_resource(resource, url_tail, endpoint):
#	api.add_resource(resource, base_url+url_tail, endpoint=endpoint)

#add_resource(CustomersApi, '/customers', endpoint='customers')
# def add_api_resources(api):

# 	api.add_resource(CustomersApi, '/customers')
# 	api.add_resource(CustomerApi, '/customers/<int:id>')
# 	api.add_resource(OrdersMadeByCustomerApi, '/customers/<int:id>/orders')

# 	api.add_resource(OrdersApi, '/orders')
# 	api.add_resource(OrderApi, '/orders/<int:id>')

# 	api.add_resource(OrderDetailsApi, '/order_details')

# 	api.add_resource(CategoriesApi, '/categories')
# 	api.add_resource(CategoryApi, '/categories/<int:id>')

# 	api.add_resource(ProductsApi, '/products')
# 	api.add_resource(ProductApi, '/products/<int:id>')
# 	api.add_resource(VendorsForProductApi, '/products/<int:id>/vendors')
# 	api.add_resource(ProductsBestSellingApi, '/products/bestselling')

# 	api.add_resource(VendorsApi, '/vendors')
# 	api.add_resource(VendorApi, '/vendors/<int:id>')

# 	api.add_resource(ProductVendorsApi, '/product_vendors')

# 	api.add_resource(EmployeesApi, '/employees')
# 	api.add_resource(EmployeeApi, '/employees/<int:id>')



@app.route("/")
def index():
	with open('README.md', 'r') as markdown_file:
		content = markdown_file.read()
		return markdown.markdown(content)


@app.before_request
def before_request():
	try:
		g.db = psycopg2.connect(Config.DB_STRING,
			options='-c search_path={schema}'.format(schema=Config.DB_SCHEMA))
		#psycopg2.connect(DATABASE_URI) # os.environ['DATABASE_URI']
	except Exception as e:
		# show error page
		raise e
	else:
		print('Successfully connected to db')

@app.teardown_request
def teardown_request(exception):
	if hasattr(g, 'db'):
		g.db.close()


def main():
	initialize_app_and_api(app)
	app.run(debug=True) # debug=True

if __name__ == '__main__':
	main()
