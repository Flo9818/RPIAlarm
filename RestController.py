from flask import Flask, Response, request, jsonify
from flask_socketio import SocketIO
import threading
from WebSocketController import WebSocketController
from SimpleWebSocketServer import SimpleSSLWebSocketServer, SimpleWebSocketServer, WebSocket
import json
from WebSocketClientInternal import run, getWs, send


app = Flask(__name__)
socketio = SocketIO(app)

client = None
activeUsers = []

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
    return jsonify({'error':'Bad request'}), 400

@app.route("/reset", methods=['PUT'])
def reset():
    if 'Authorization' in request.headers:
        secret = request.headers.get('Authorization')
        if secret != 'Bearer secret':
            return jsonify({'error': 'Wrong credentials'}), 400
        resetUser()
        return jsonify({'success': True}), 200
    return jsonify({'error':'Bad request'}), 400

def checkTalkingUsers(user):
    if user in activeUsers:
        activeUsers.remove(user)
    else:
        activeUsers.append(user)
    triggerAlarm()

def resetUser():
    activeUsers = []
    triggerAlarm()

def triggerAlarm():
    global server
    if len(activeUsers) == 0:
        send(json.dumps({'COMMAND': 'disable'}))
    else:
        send(json.dumps({'COMMAND': 'enable'}))

def rest():
    app.run(ssl_context=('cert.pem', 'key.pem'), port=5000)

def ws():
    server = SimpleSSLWebSocketServer('', 3000, WebSocketController, certfile='cert.pem', keyfile='key.pem')
    #server = SimpleWebSocketServer('', 3000, WebSocketController)
    print('Starting Websocketserver on port ' + str(3000))
    server.serveforever()

def runClient():
    global client
    client = getWs()
    run()

if __name__ == "__main__":
    ws = threading.Thread(target = ws)
    rest = threading.Thread(target = rest)
    client = threading.Thread(target = runClient)
    rest.start()
    ws.start()
    client.start()
