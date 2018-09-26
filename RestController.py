import datetime
import json
import threading
import time

from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from SimpleWebSocketServer import (SimpleSSLWebSocketServer,
                                   SimpleWebSocketServer, WebSocket)

from WebSocketClientInternal import getWs, run, send
from WebSocketController import WebSocketController

app = (Flask(__name__))
cors = CORS(app)

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
        user = request.args.get('user')
        resetUser()
        createLogEntry(user, 'reset')
        return jsonify({'success': True}), 200
    return jsonify({'error': 'Bad request'}), 400


@app.route('/mutedUsers', methods=['GET'])
def mutedUsers():
    return jsonify({'activeUsers': activeUsers})


@app.route('/status', methods=['GET'])
def status():
    return jsonify({'enabled': len(activeUsers) != 0})


@app.route('/log', methods=['GET'])
def log():
    global logs
    return jsonify(logs)


@app.route('/clearLogs', methods=['PUT'])
def clearLogs():
    global logs
    logs = []
    return '', 204


def checkTalkingUsers(user):
    if user in activeUsers:
        activeUsers.remove(user)
        createLogEntry(user, 'unmuted')
    else:
        activeUsers.append(user)
        createLogEntry(user, 'muted')
    triggerAlarm()


def resetUser():
    global activeUsers, lastCommand
    activeUsers = []
    send(json.dumps({'COMMAND': 'disable'}))
    lastCommand = 'disable'


def triggerAlarm():
    global server, lastCommand
    if len(activeUsers) == 0:
        if lastCommand == 'enable':
            send(json.dumps({'COMMAND': 'disable'}))
            lastCommand = 'disable'
        elif lastCommand == 'disable':
            send(json.dumps({'COMMAND': 'enable'}))
    else:
        if lastCommand == 'disable':
            send(json.dumps({'COMMAND': 'enable'}))
            lastCommand = 'enable'


def rest():
    server = WSGIServer(('0.0.0.0', 5000), app)
    print('Start REST server')
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
    global logs
    logs.append({"user": user, "action": action, "date": datetime.datetime.fromtimestamp(
        time.time()).strftime('%Y-%m-%d %H:%M:%S')})


if __name__ == "__main__":
    ws = threading.Thread(target=ws)
    rest = threading.Thread(target=rest)
    client = threading.Thread(target=runClient)
    ws.start()
    rest.start()
    client.start()
