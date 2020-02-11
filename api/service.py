
from flask import Flask, request, redirect, url_for, abort, make_response, render_template
from flask import jsonify
from api import app
from api.models import Product
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
    return jsonify(database.products())


@app.route('/product/<int:product_id>', methods=['GET'])
def product(product_id):
    logging.debug(" GET /product/" + str(product_id))
    return jsonify(database.product(product_id))


@app.route('/product', methods=['POST'])
def insert_product():
    logging.debug(" POST /product")

    product = {
        "nombre": request.form.get('nombre'),
        "descripcion": request.form.get('descripcion'),
        "precio": float(request.form.get('precio')),
        "imagen": request.form.get('imagen')
    }

    database.insert_product(product)

    return jsonify(product)


@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    logging.debug(" PUT /product")

    product = {
        "id": product_id,
        "nombre": request.form.get('nombre'),
        "descripcion": request.form.get('descripcion'),
        "precio": float(request.form.get('precio')),
        "imagen": request.form.get('imagen')
    }

    database.update_product(product)
    
    return jsonify(product)


@app.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    logging.debug(" DELETE /product/" + str(product_id))

    product = database.product(product_id)
    database.delete_product(product_id)

    return jsonify(product)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada...")

