from gevent.pywsgi import WSGIServer
from flask import Flask, Response, request, jsonify
import threading
from WebSocketController import WebSocketController
from SimpleWebSocketServer import SimpleSSLWebSocketServer, SimpleWebSocketServer, WebSocket
import json
import datetime
import time
from WebSocketClientInternal import run, getWs, send
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

client = None
activeUsers = []
lastCommand = 'disable'
logs = []


@app.route("/trigger", methods=['PUT'])
def trigger():
    if 'Authorization' in request.headers:
        secret = request.headers.get('Authorization')
        if secret != 'Bearer secret':
            return jsonify({'error': 'Wrong credentials'}), 400

        user = request.args.get('user')
        if user:
            checkTalkingUsers(user)
            return jsonify({'success': True}), 200
    return jsonify({'error': 'Bad request'}), 400


@app.route("/reset", methods=['PUT'])
def reset():
    if 'Authorization' in request.headers:
        secret = request.headers.get('Authorization')
        if secret != 'Bearer secret':
            return jsonify({'error': 'Wrong credentials'}), 400
        resetUser()
        return jsonify({'success': True}), 200
    return jsonify({'error': 'Bad request'}), 400


@app.route('/mutedUsers', methods=['GET'])
def mutedUsers():
    return jsonify({'activeUsers': activeUsers})


@app.route('/status', methods=['GET'])
def status():
    return jsonify({'enabled': len(activeUsers) != 0})


def checkTalkingUsers(user):
    if user in activeUsers:
        activeUsers.remove(user)
    else:
        activeUsers.append(user)
    triggerAlarm()


def resetUser():
    global activeUsers
    activeUsers = []
    send(json.dumps({'COMMAND': 'disable'}))
    lastCommand = 'disable'


def triggerAlarm():
    global server, lastCommand
    if len(activeUsers) == 0:
        if lastCommand == 'enable':
            send(json.dumps({'COMMAND': 'disable'}))
            lastCommand = 'disable'
    else:
        if lastCommand == 'disable':
            send(json.dumps({'COMMAND': 'enable'}))
            lastCommand = 'enable'


def rest():
    server = WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
    #app.run(host='0.0.0.0', port=5000)


def ws():
    #server = SimpleSSLWebSocketServer('', 3000, WebSocketController, certfile='cert.pem', keyfile='key.pem')
    server = SimpleWebSocketServer('0.0.0.0', 3000, WebSocketController)
    print('Starting Websocketserver on port ' + str(3000))
    server.serveforever()


def runClient():
    global client
    client = getWs()
    run()


def createLogEntry(user, action):
    return {"user": user, "action": action, "time": datetime.datetime.fromtimestamp(
        time.time()).strftime('%Y-%m-%d %H:%M:%S')}


if __name__ == "__main__":
    ws = threading.Thread(target=ws)
    rest = threading.Thread(target=rest)
    client = threading.Thread(target=runClient)
    rest.start()
    ws.start()
    client.start()
