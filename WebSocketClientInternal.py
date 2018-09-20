import websocket
import ssl

destUri = "wss://localhost:3000";
ws = None

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("### opened ###")

def send(message):
    global ws
    ws.send(message)

def getWs():
    global ws
    ws = websocket.WebSocketApp(destUri,
        on_message = on_message,
        on_error = on_error,
        on_close = on_close)
    ws.on_open = on_open
    return ws

def run():
    global ws
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})