FROM python:3.7

COPY RestController.py .
COPY WebSocketClientInternal.py .
COPY WebSocketController.py .

RUN pip install flask-cors git+https://github.com/dpallot/simple-websocket-server.git gevent flask websocket-client

EXPOSE 5000
EXPOSE 3000

ENTRYPOINT exec python RestController.py