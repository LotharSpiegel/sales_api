# A simple REST API using Flask and Flask-RESTPlus

This example project shows how to use Flask and Flask-RESTPlus (https://flask-restplus.readthedocs.io/en/stable/)
to quickly build a REST Api.

It doesnt use any ORM, but instead shows how to directly incoporate SQL code to access the database and perform the GET, POST and DELETE operations.

## Quicktour

To start the flask server, run server.py which will make the landing page available at http://localhost:5000/api/v1/ (the exact port can vary)

The nice point about using Flask-RESTPlus is that it creates documentation and a nice simple gui to access all api endpoints for us.
In api/api_main.py the flask_restplus.Api instance is defined
and used in server.py together with a standard flask app.

The statement above about not using any ORM was not entirely correct since in models/base.py, the class BaseModel implements a very simple ORM, where a model corresponds one-to-one to a table in the database.
Every model corresponding to a table in the sales database has its own module in the models directory
The corresponding api endpoints are implemented in the api directory.
In api/base.py, there are the base classes BaseListResource and BaseModelResource for lists of objects (for example the list of all customers) or respectively a particular object (a particular customer)



## What do you need to try it out

If you have used Flask (a lightweight Python webframework) before, you should have no problems running this example API locally on your machine.

You will need postgres installed and running.
As example database it uses the postgres sales database from the book 'SQL Queries for Mere Mortals' (http://www.informit.com/store/sql-queries-for-mere-mortals-a-hands-on-guide-to-data-9780321992475)
The 'sales' database needs to be created (using the provided sql scripts).

## What is a REST API?

REST is a type of architecture for Web services:
Resources which are transferred over the HTTP protocol.

### The Main points of REST are:

Use HTTP methods explicitely
get to receive a resource, post to create a resource, put and delete
Stateless: especially the Server is supposed to be stateless
Every two actions are independent from one another. The server is completely oblivious

```json
{
	"data_id": "data",
}```


expose the api endpoint via a clear URIs

`GET /resource_type/resource_identifier`

resource either in XML or JSON format