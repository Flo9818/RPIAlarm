from gevent.pywsgi import WSGIServer
from flask import Flask, Response, request, jsonify
import threading
from WebSocketController import WebSocketController
from SimpleWebSocketServer import SimpleSSLWebSocketServer, SimpleWebSocketServer, WebSocket
import json
import datetime
import time
from WebSocketClientInternal import run, getWs, send
import sqlite3

conn = sqlite3.connect('logs.db')

try:
    # Create table
    c = conn.cursor()
    c.execute('''CREATE TABLE logs
                (date text, action text, user text)''')
except sqlite3.OperationalError:
    pass

app = Flask(__name__)

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
        with sqlite3.connect("logs.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO logs VALUES (?,?,?)", (datetime.datetime.fromtimestamp(
                time.time()).strftime('%Y-%m-%d %H:%M:%S'), '', 'reset'))
            con.commit()
        return jsonify({'success': True}), 200
    return jsonify({'error': 'Bad request'}), 400


@app.route('/mutedUsers', methods=['GET'])
def mutedUsers():
    return jsonify({'activeUsers': activeUsers})


@app.route('/log', methods=['GET'])
def log():
    with sqlite3.connect("logs.db") as con:
        cur = con.cursor()
        tmp = []
        for row in cur.execute('SELECT * FROM logs ORDER BY date DESC'):
            tmp.append({"date": row[0], "name": row[1], "action": row[2]})
        return jsonify(tmp)


@app.route('/status', methods=['GET'])
def status():
    return jsonify({'enabled': len(activeUsers) != 0})


@app.route('/clearLogs', methods=['DELETE'])
def clearLogs():
    with sqlite3.connect("logs.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM logs")
        return '', 204


def checkTalkingUsers(user):
    with sqlite3.connect("logs.db") as con:
        cur = con.cursor()
        if user in activeUsers:
            activeUsers.remove(user)
            cur.execute("INSERT INTO logs VALUES (?,?,?)", (datetime.datetime.fromtimestamp(
                time.time()).strftime('%Y-%m-%d %H:%M:%S'), user, 'unmuted'))
            logs.append(createLogEntry(user, 'unmuted'))
        else:
            activeUsers.append(user)
            cur.execute("INSERT INTO logs VALUES (?,?,?)", (datetime.datetime.fromtimestamp(
                time.time()).strftime('%Y-%m-%d %H:%M:%S'), user, 'muted'))
            logs.append(createLogEntry(user, 'muted'))
        con.commit()
    triggerAlarm()


def resetUser():
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
