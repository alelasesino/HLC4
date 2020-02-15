
from pymongo import MongoClient
from bson.objectid import ObjectId
from contextlib import closing
from api.models import Product
from api.utils import format_object_id


MONGO_CONFIG = {
    "host": "mongodb+srv://alelasesino:alelasesino@apirest-android-1hwud.mongodb.net/test?retryWrites=true&w=majority",
    "database": "Productos",
    "collection": "Producto"
}


client = MongoClient(MONGO_CONFIG["host"])
db = client[MONGO_CONFIG["database"]]
collection = db[MONGO_CONFIG["collection"]]


def products():
    """Obtiene todos los productos
    
    Returns:
        array dictionary -- (ID, NOMBRE, DESCRIPCION, PRECIO, IMAGEN) de los productos
    """
    product_cursor = collection.find()
    products = []

    for product in product_cursor:
        products.append(format_object_id(product))

    return products


def product(product_id: str):
    """Obtiene los datos de un producto por su id
    
    Arguments:
        product_id {str} -- Id del producto
    
    Returns:
        Product -- Datos del producto seleccionado
    """
    try:
        product = collection.find_one({"_id": ObjectId(product_id)})
    except:
        return None

    return format_object_id(product)


def insert_product(product: dict):
    """Inserta un nuevo producto en la base de datos
    
    Arguments:
        product {dict} -- Producto para insertar
    """
    collection.insert_one(product)


def delete_product(product_id: str):
    """Elimina el producto deseado en la base de datos
    
    Arguments:
        product_id {str} -- Id del producto para borrar
    """
    collection.delete_one({"_id": ObjectId(product_id)})


def update_product(product: dict):
    """Actualiza el producto deseado en la base de datos
    
    Arguments:
        product {dict} -- Producto para actualizar
    """
    new_product = product.copy()
    new_product.pop("id")

    collection.replace_one({"_id": ObjectId(product["id"])}, new_product)

