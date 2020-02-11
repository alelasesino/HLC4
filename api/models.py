
class Product:
    """Modelo de un producto
    """
    def __init__(self, id:int, nombre:str, descripcion:str, precio:float, imagen:str):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.imagen = imagen

    @classmethod
    def new_product(cls):
        return cls(-1, '', '', 0, '')

