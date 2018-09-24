import websocket
import ssl
import json
#from LedController import LedController

#lc = LedController()

destUri = "ws://vileadgentest.westeurope.cloudapp.azure.com:3000"


def on_message(ws, message):
    try:
        msg = json.loads(message.split('- ')[1])
        if msg['COMMAND'] == 'enable':
            print('Enable')
   #         lc.setEnabled(True)
        elif msg['COMMAND'] == 'disable':
            print('Disable')
  #          lc.setEnabled(False)
    except:
        pass


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print("### opened ###")


ws = websocket.WebSocketApp(destUri,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.on_open = on_open
#ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
ws.run_forever()
