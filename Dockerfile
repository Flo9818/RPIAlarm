FROM python:3.7

COPY RestController.py .
COPY WebSocketClientInternal.py .
COPY WebSocketController.py .

RUN pip install flask-cors git+https://github.com/dpallot/simple-websocket-server.git gevent flask websocket-client

CMD ["python RestController.py"]