FROM python:3

ADD RestController.py /
ADD WebSocketClientInternal.py /
ADD cert.pem /
ADD key.pem /
ADD WebSocketController.py /

RUN pip install flask websocket-client gevent git+https://github.com/dpallot/simple-websocket-server.git

EXPOSE 5000
EXPOSE 3000

CMD [ "python", "RestController.py" ]