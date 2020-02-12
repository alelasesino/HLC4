
from flask import request, redirect, url_for
from flask import jsonify
from api import app
from api.models import Product
from api.utils import to_float
import api.database as database
import logging


LOG_FILENAME = "service.log"
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)


@app.route('/')
def root():
    return redirect(url_for('products'))


@app.route('/products', methods=['GET'])
def products():
    logging.debug(" GET /products")

    try:
        products = database.products()
    except Exception as err:
        return error_response([str(err)], 400)

    return jsonify(products)


@app.route('/product/<int:product_id>', methods=['GET'])
def product(product_id):
    logging.debug(" GET /product/" + str(product_id))

    try:
        product = database.product(product_id)

        if product == None:
            return error_response(["Product not exist!"], 400)

    except Exception as err:
        return error_response([str(err)], 400)

    return jsonify(product)


@app.route('/product', methods=['POST'])
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

    return jsonify({"error": 0, "data": product})


@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
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

    return jsonify({"error": 0, "data": product})


@app.route('/product/<int:product_id>', methods=['DELETE'])
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

    return product

