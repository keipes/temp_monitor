from bottle import run, template, Bottle, abort, static_file, request
import gevent
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
import time
from client.dynamostream import DynamoStreamClient
import json
import Queue

app = Bottle()
host = 'localhost'
port = 8080

_queue = None

@app.route('/')
def index():
    return static_file('html/index.html', root=".")

@app.route('/websocket')
def handle_websocket():
    print('websocket')
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Websocket route')
    while True:
        try:
            while True:
                data = json.dumps(_queue.get_nowait())
                print('post')
                wsock.send(data)
        except Queue.Empty:
            gevent.sleep(1)
        except WebSocketError:
            break

@app.route('/js/<path:path>')
def js(path):
    return static_file(path, root='js')

def main():
    dsc = DynamoStreamClient()
    global _queue
    _queue = dsc.get_queue()
    print(_queue)
    dsc.start()
    print('got queue')
    try:
        server = WSGIServer((host, port), app, handler_class=WebSocketHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('keyboard interrupt')
    dsc.stop()

if __name__ == '__main__':
    main()
