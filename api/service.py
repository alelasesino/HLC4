
from flask import request, redirect, url_for
from flask import jsonify
from api import app
from api.models import Product
from api.utils import to_float, format_object_id, get_tags, token_time_expire, current_milis
from functools import wraps
from flasgger import Swagger, swag_from
#import api.database as database
import api.database_mongo as database
import logging
import jwt

LOG_FILENAME = "service.log"
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

swagger_template = {
    'securityDefinitions': { 
        'ApiKeyAuth': { 
            'type': 'apiKey', 
            'in': 'header', 
            'name': 'Authorization'
        }
    },
    'schemes': ['https','http'],
    'info': {
        'description': 'Servicio REST realizado el 26/02/2020',
        'version': '1.1.2',
        'title': 'Inventario',
        'termsOfService': 'http://swagger.io/terms/',
        'contact': {
            'name': 'the developer',
            'email': 'alejperez99@hotmail.com'
        }
    },
    'externalDocs': {
        'description': 'Developer GitHub',
        'url': 'https://github.com/alelasesino/HLC4'
    }
}

swagger = Swagger(app, template=swagger_template)

def jwt_required(function):

    @wraps(function)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')

        if not auth:
            return jsonify({"error": 1, "message": "Authentication is required!"}), 403

        token = auth.replace("Bearer ", "")

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({"error": 1, "message": "Token is invalid!"}), 403

        return function(*args, **kwargs)

    return decorated


@app.route('/login')
@swag_from('./swagger/authentication/login.yaml')
def login():
    token = jwt.encode({"user": current_milis()},  app.config['SECRET_KEY'])
    return jsonify({"token": token.decode('UTF-8')})


@app.route('/login/<int:expire>')
@swag_from('./swagger/authentication/login_expire.yaml')
def login_expire(expire):
    token = jwt.encode({"user": current_milis(), "exp": token_time_expire(expire)},  app.config['SECRET_KEY']) 
    return jsonify({"token": token.decode('UTF-8')})


@app.route('/')
def root():
    return redirect(url_for('products'))


@app.route('/products', methods=['GET'])
@swag_from('./swagger/product/products.yaml')
@jwt_required
def products():
    logging.debug(" GET /products")

    try:
        products = database.products()
    except Exception as err:
        return error_response([str(err)], 400)

    return jsonify({"error": 0, "data": products})


@app.route('/product/<string:product_id>', methods=['GET'])
@swag_from('./swagger/product/product.yaml')
@jwt_required
def product(product_id):
    logging.debug(" GET /product/" + product_id)

    try:
        product = database.product(product_id)

        if product == None:
            return error_response(["Product not exist!"], 400)

    except Exception as err:
        return error_response([str(err)], 400)

    return jsonify({"error": 0, "data": product})


@app.route('/product', methods=['POST'])
@swag_from('./swagger/product/insert.yaml')
@jwt_required
def insert_product():
    logging.debug(" POST /product")

    product = product_body_request()
    errors = validate_product(product)

    if len(errors) > 0:
        return error_response(errors, 400, product)  

    try:
        database.insert_product(product)
    except Exception as err:
        return error_response([str(err)], 400, product)
    
    return jsonify({"error": 0, "data": format_object_id(product)})


@app.route('/product/<string:product_id>', methods=['PUT'])
@swag_from('./swagger/product/update.yaml')
@jwt_required
def update_product(product_id: str):
    logging.debug(" PUT /product")

    product = product_body_request(product_id)
    errors = validate_product(product)

    try:
        if database.product(product_id) == None:
            errors.append("Product not exist!")

        if len(errors) > 0:
            return error_response(errors, 400, product) 

        database.update_product(product)
    except Exception as err:
        return error_response([str(err)], 400, product)

    return jsonify({"error": 0, "data": format_object_id(product)})


@app.route('/product/<string:product_id>', methods=['DELETE'])
@swag_from('./swagger/product/delete.yaml')
@jwt_required
def delete_product(product_id):
    logging.debug(" DELETE /product/" + str(product_id))

    try:
        product = database.product(product_id)
        
        if database.product(product_id) == None:
            return error_response(["Product not exist!"], 400, product)  

        database.delete_product(product_id)
    except Exception as err:
        return error_response([str(err)], 400, product)

    return jsonify({"error": 0, "data": product})


def error_response(message, error_code=500, data=None):

    error = {
        "error": 1,
        "message": ", ".join(message)
    }

    if(data != None):
        error["data"] = data

    return jsonify(error), error_code


def validate_product(product: dict):
    errors = []

    if product["precio"] == None:
        errors.append("Product price must be a number")

    if product["nombre"] == None or product["nombre"] == "":
        errors.append("Product name cannot be empty")

    if product["descripcion"] == None or product["descripcion"] == "":
        errors.append("Product description cannot be empty")

    return errors


def product_body_request(id=None):

    product = {
        "nombre": request.form.get('nombre'),
        "descripcion": request.form.get('descripcion'),
        "precio": to_float(request.form.get('precio')),
        "imagen": request.form.get('imagen')
    }

    if id != None:
        product["id"] = id

    tags = get_tags(request.form.get('tags'))
    
    if tags != None:
        product["tags"] = tags

    return product

