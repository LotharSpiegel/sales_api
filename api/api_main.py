from flask_restplus import Api
import logging

api = Api(version='1.0', title='Sales REST API',
 		description='Documentation for Sales REST API')


log = logging.getLogger(__name__)

@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    #if not settings.FLASK_DEBUG:
    return {'message': message,
    		'error': str(e)}, 500


# @api.errorhandler(NoResultFound)
# def database_not_found_error_handler(e):
# 	log.warning(traceback.format_exc())
# 	return {'message': 'A database result was required but none was found.'}, 404