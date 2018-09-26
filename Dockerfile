FROM python:3.7

RUN pip install flask-cors git+https://github.com/dpallot/simple-websocket-server.git gevent flask websocket-client

CMD ["python app.py"]