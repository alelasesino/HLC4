
import mysql.connector
from contextlib import closing
from api.models import Product


"""config = {
    "host": "localhost",
    "user": "root",
    "passwd": "",
    "database": "productos"
}"""

config = {
    "host": "sql7.freemysqlhosting.net",
    "user": "sql7322310",
    "passwd": "zusIgSCSUM",
    "database": "sql7322310"
}


db = mysql.connector.connect(
  host=config["host"],
  user=config["user"],
  passwd=config["passwd"],
  database=config["database"]
)


def products():
    """Obtiene todos los productos
    
    Returns:
        array dictionary -- (ID, NOMBRE, DESCRIPCION, PRECIO, IMAGEN) de los productos
    """
    with closing(db.cursor()) as c:

        sql_query = "SELECT id, nombre, descripcion, precio, imagen FROM producto"
        c.execute(sql_query)

        products = []
        
        for (id, nombre, descripcion, precio, imagen) in c:
            products.append({
                "id": id, 
                "nombre": nombre, 
                "descripcion": descripcion, 
                "precio": precio, 
                "imagen": imagen
            })

    return products


def product(product_id: int):
    """Obtiene los datos de un producto por su id
    
    Arguments:
        product_id {int} -- Id del producto
    
    Returns:
        Product -- Datos del producto seleccionado
    """
    with closing(db.cursor()) as c:

        sql_query = "SELECT id, nombre, descripcion, precio, imagen FROM producto WHERE id = %s"
        c.execute(sql_query, [product_id])
        
        result = c.fetchone()

        if result != None:
            (id, nombre, descripcion, precio, imagen) = result

            product = {
                    "id": id, 
                    "nombre": nombre, 
                    "descripcion": descripcion, 
                    "precio": precio, 
                    "imagen": imagen
                }

            return product


def insert_product(product: dict):
    """Inserta un nuevo producto en la base de datos
    
    Arguments:
        product {dict} -- Producto para insertar
    """
    with closing(db.cursor()) as c:

        sql_query = "INSERT INTO producto(nombre, descripcion, precio, imagen) VALUES(%s, %s, %s, %s)"
        c.execute(sql_query, (product["nombre"], product["descripcion"], product["precio"], product["imagen"]))
        db.commit()


def delete_product(product_id: int):
    """Elimina el producto deseado en la base de datos
    
    Arguments:
        product_id {int} -- Id del producto para borrar
    """
    with closing(db.cursor()) as c:
        
        sql_query = "DELETE FROM producto WHERE id = %s"
        c.execute(sql_query, [product_id])
        db.commit()


def update_product(product: dict):
    """Actualiza el producto deseado en la base de datos
    
    Arguments:
        product {dict} -- Producto para actualizar
    """
    with closing(db.cursor()) as c:
        
        sql_query = "UPDATE producto SET nombre = %s, descripcion = %s, precio = %s, imagen = %s WHERE id = %s"
        c.execute(sql_query, (product["nombre"], product["descripcion"], product["precio"], product["imagen"], product["id"]))
        db.commit()

