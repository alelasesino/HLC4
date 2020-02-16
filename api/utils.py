import datetime
import time as _time

def to_float(price: str):
    try:
        return float(price)
    except:
        return None


def get_tags(tags: str):
    if tags != None:
        return tags.split(";")
    return None

def format_object_id(product):

    if product == None: 
        return None

    if "_id" in product:
        object_id = product["_id"]
        product["_id"] = str(object_id)

    return product


def token_time_expire(seconds=0):
    return datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds)


def current_milis():
    return int(round(_time.time() * 1000))
