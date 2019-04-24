import os

basedir = os.path.abspath(os.path.dirname(__file__))

POSTGRES = {
	'user': 'postgres',
	'pw': os.environ['SALES_PW'],
	'db': 'sales',
	'schema': 'salesorderssample',
	'host': None, # 'localhost',
	'port': None, # '2142',
}

# DATABASE_URI = 'postgresql://{user}:{pw}@{host}:{port}/{db}'.format(
# 		user=POSTGRES['user'], pw=POSTGRES['pw'], host=POSTGRES['host'],
# 		port=POSTGRES['port'], db=POSTGRES['db'])

class Config(object):

	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True
	SECRET_KEY = 'needs-to-be-changed'
	DB_URI = 'postgresql://{user}:{pw}@{host}:{port}/{db}'.format(
		user=POSTGRES['user'], pw=POSTGRES['pw'], host=POSTGRES['host'],
		port=POSTGRES['port'], db=POSTGRES['db'])
	host = POSTGRES.get('host', None)
	if host is None:
		host_value = ''
	else:
		host_value = 'host={host}'.format(host=host)
	port = POSTGRES.get('port', None)
	if port is None:
		port_value = ''
	else:
		port_value = 'port={port}'.format(port=port)
	DB_STRING = '{host_value} {port_value} dbname={dbname} user={user} password={password}'.format(
				host_value=host_value, port_value=port_value, dbname=POSTGRES['db'],
				user=POSTGRES['user'], password=POSTGRES['pw'])
	DB_SCHEMA = POSTGRES['schema']
	# SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{pw}@{host}:{port}/{db}'.format(
	# 	user=POSTGRES['user'], pw=POSTGRES['pw'], host=POSTGRES['host'],
	# 	port=POSTGRES['port'], db=POSTGRES['db'])

	# = os.environ['DATABASE_URI']
	#$ export DATABASE_URL="postgresql://localhost/dbname"
	# add that line to .env file


class ProductionConfig(Config):
	DEBUG = False

class StagingConfig(Config):
	DEVELOPMENT = True
	DEBUG = True

class DevelopmentConfig(Config):
	DEVELOPMENT = True
	DEBUG = True

class TestingConfig(Config):
	TESTING = True