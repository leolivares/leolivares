from flask import Flask, jsonify, abort, request
from pymongo import MongoClient
import sys

# Se recomienda descargar el json de requests para postman, 
# e importarlo en postman para probar las funciones.

app = Flask(__name__)
# MONGODATABASE corresponde al nombre de su base de datos
MONGODATABASE = "AyudantiaDB"
MONGOSERVER = "localhost"
MONGOPORT = 27017
# instanciar el cliente de pymongo para realizar consultas a la base de datos
client = MongoClient(MONGOSERVER, MONGOPORT)

# Decorador defiene la ruta. 
@app.route('/')
def hello_world():
    # Funcion retorna una json en base de su request
    # Se recomienda usar jsonify de Flask para manejar la creacion de json
    # Para hacer un print, necesitan hacerlo de la siguiente manera:
    print(123, file=sys.stdout)
    return jsonify({"status": "ok"})


# Decorador para ruta con metodo GET, solo puede recibir requests tipo GET
# También recibe un variable user como int, para poder usarlo en la función
# Ejemplo: GET a "localhost:5000/sender/2" retorna los mensajes mandados por el usuario 2
@app.route('/sender/<int:user>', methods=['GET'])
def sender(user):
    # Se conecta el cliente de pymongo a la base de datos
    mongodb = client[MONGODATABASE]
    # Se define un "cursor" para la tabla ayudantia de la base de datos
    collection = mongodb.ayudantia
    output = []
    # Aplicamos el query para buscar los mensajes mandados por el usuario recibido en el url
    for s in collection.find({"sender": user}, {"_id": 0}):
        output.append(s)
    # Si la consulta resulta ser vacia, se retorna código HTTP 404,
    # para decir que no se encontró ningún mensaje mandado por el usuario.
    if len(output) == 0:
        return jsonify(), 404
    # Retorna los mensajes 
    else:
        return jsonify(output), 200


# La función recibe una json con los parametros de la insercion,
# No es necesario agregar variables dentro del URL
@app.route('/add_message/', methods=['POST'])
def add_message():
    mongodb = client[MONGODATABASE]
    collection = mongodb.ayudantia
    # Guarda el json en el variable data
    data = request.get_json()
    # Se inserta un nuevo item a la colección de mongo con los
    #  parámetros definidos en el json
    inserted_message = collection.insert_one({
        'message': data["message"],
        'sender': data["sender"],
        'receptant': data["receptant"],
        'date':data["date"],
    })
    # insert_one retorna None si no pudo insertar
    if inserted_message is None:
        return jsonify(), 404
    # Retorna el id del elemento insertado
    else:
        return jsonify({"id": str(inserted_message.inserted_id)}), 200


@app.route('/remove_message/<string:date>', methods=['DELETE'])
def remove_message(date):
    mongodb = client[MONGODATABASE]
    messages = mongodb.ayudantia
    result = messages.delete_one({
        'date': date,
    })
    
    if result.deleted_count == 0:
        return jsonify(), 404
    else:
        return jsonify("Eliminado"), 200


if __name__ == '__main__':
    # Pueden definir su puerto para correr la aplicación
    app.run(port=5000)
