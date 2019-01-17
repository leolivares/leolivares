from flask import Flask, jsonify, abort, request
from pymongo import MongoClient, TEXT
import datetime
import sys

app = Flask(__name__)
MONGODATABASE = "Entrega4"
MONGOSERVER = "localhost"
MONGOPORT = 27017
client = MongoClient(MONGOSERVER, MONGOPORT)


@app.route('/')
def hello_world():
    return jsonify({"status": "ok"})


@app.route('/message/<int:message>', methods=['GET'])
def get_message(message):
    mongodb = client[MONGODATABASE]
    messages = mongodb.messages

    output = []
    for s in messages.find({"id": message}, {"_id": 0}):
        output.append(s)

    if len(output) == 0:
        return jsonify(), 404
    else:
        return jsonify(output), 200


@app.route('/user_info/<int:user>', methods=['GET'])
def user_info(user):
    mongodb = client[MONGODATABASE]
    messages = mongodb.messages
    users = mongodb.usuarios

    output = []
    for s in users.find({"id_usuario": user}, {"_id": 0}):
        output.append(s)

    if len(output) == 0:
        return jsonify(), 404
    else:

        searched_user = output[0]
        msgs = list()
        for l in messages.find({"sender": user}, {"_id": 0}):
            msgs.append(l)

        searched_user["messages"] = msgs

        return jsonify(searched_user), 200


@app.route('/user1/<int:user1>/user2/<int:user2>', methods=['GET'])
def get_messages(user1, user2):
    mongodb = client[MONGODATABASE]
    messages = mongodb.messages

    output = []
    for msg1 in messages.find({"sender": user1, "receptant": user2}, {"_id": 0}):
        output.append(msg1)

    for msg2 in messages.find({"sender": user2, "receptant": user1}, {"_id": 0}):
        output.append(msg2)

    if len(output) == 0:
        return jsonify(), 404
    else:
        return jsonify(output), 200


@app.route('/new_message', methods=['POST'])
def new_message():
    mongodb = client[MONGODATABASE]
    messages = mongodb.messages

    new_id = messages.find().sort([("_id", -1)]).limit(1)[0]['id'] + 1
    now = datetime.datetime.now()

    data = request.get_json()

    new_msg = messages.insert_one({
        'message': data['message'],
        'sender': data['sender'],
        'receptant': data['receptant'],
        'lat': data['lat'],
        'long': data['long'],
        'id': new_id,
        'date': now.strftime("%Y-%m-%d")
    })

    if new_message is None:
        return jsonify(), 404
    else:
        return jsonify({"id": str(new_id)}), 200


@app.route('/delete_message/<int:id>', methods=['DELETE'])
def delete_message(id):
    mongodb = client[MONGODATABASE]
    messages = mongodb.messages

    result = messages.delete_one({
        'id': id,
    })

    if result.deleted_count == 0:
        return jsonify(), 404
    else:
        return jsonify("Mensaje Eliminado"), 200


@app.route('/search_text/<string:user>/<string:query>', methods=['GET'])
def text_search(user, query):
    '''
    Debe recibir 2 strings, el usuario y el query.
    En el informe se explica detalladamente como realizar la consulta.
    Cada frase debe ser separada por un '-'
    Si el usuario entregado es -1, busca en toda la base de datos.
    :return:
    '''
    mongodb = client[MONGODATABASE]
    messages = mongodb.messages

    data = request.get_json()

    all_phrases = query.split("-")

    must_phrases = [x[1:] for x in all_phrases if x[0] == '1']
    could_phrases = [x[1:] for x in all_phrases if x[0] == '2']
    dont_phrases = [x[1:] for x in all_phrases if x[0] == '3']

    index_name = "message"
    if index_name not in messages.index_information():
        messages.create_index([('message', TEXT)])

    search_msg = ""
    for phrase in must_phrases:
        search_msg += '\"' + phrase + '\"' + " "
    for phrase in could_phrases:
        search_msg += phrase + " "
    for phrase in dont_phrases:
        search_msg += "-" + phrase + " "
    search_msg = search_msg.strip(" ")

    output = []
    if int(user) == -1:
        for msg in messages.find({'$text': {'$search': search_msg}}, {'_id': 0}):
            output.append(msg)

    else:
        for msg in messages.find({'$and': [{'sender': int(user),'$text': {'$search': search_msg}}]}, {'_id': 0}):
            output.append(msg)

    if len(output) == 0:
        return jsonify(), 404
    else:
        return jsonify(output), 200



if __name__ == '__main__':
    app.run(port=5000)