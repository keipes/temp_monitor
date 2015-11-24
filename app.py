from bottle import run, template, Bottle, abort, static_file, request
import gevent
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
from gevent.lock import Semaphore
import time
from client.dynamostream import DynamoStreamClient
from client.dynamo import DynamoClient
import json
import Queue
import traceback
import sys
import pprint
import util

app = Bottle()
host = 'localhost'
host = '0.0.0.0'
port = 8080

socket_queues = []
queue_list = []
old_items = []

@app.route('/')
def index():
    return static_file('html/index.html', root=".")

@app.route('/websocket')
def handle_websocket():
    print('socket connection')
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Websocket route')
    queue = register_queue()
    queue.put({
        'type': 'max_temp',
        'temperature': dc.get_max_temp()
    })
    queue.put({
        'type': 'min_temp',
        'temperature': dc.get_min_temp()
    })
    sem = Semaphore()
    gevent.spawn(process, wsock, queue, sem)
    while True:
        try:
            msg = wsock.receive()
            data = json.loads(msg)
            print(data)
            if data['type'] == 'maxTempSet':
                dc.record_max_temp(data['data'])
            elif data['type'] == 'minTempSet':
                dc.record_min_temp(data['data'])
            else:
                pprint.pprint(data)
        except WebSocketError as e:
            print(e)
            traceback.print_tb(sys.exc_info()[2])
            break
    wsock.close()
    deregister_queue(queue)

def process(ws, queue, sem):
    while True:
        with sem:
            try:
                data = json.dumps(queue.get_nowait())
                ws.send(data)
            except Queue.Empty:
                gevent.sleep(1)

def register_queue():
    queue = Queue.Queue()
    for item in old_items:
        queue.put(item)
    queue_list.append(queue)
    return queue

def deregister_queue(queue):
    queue_list.remove(queue)

@app.route('/js/<path:path>')
def js(path):
    return static_file(path, root='js')

@app.route('/css/<path:path>')
def css(path):
    return static_file(path, root='css')

def main():
    dsc = DynamoStreamClient(queue_list, old_items, util.get_temp_hist_arn(force_prod=True))
    dsc.start()
    dsc_misc = DynamoStreamClient(queue_list, old_items, util.misc_arn)
    dsc_misc.start()
    global dc
    dc = DynamoClient('miscellaneous')
    try:
        server = WSGIServer((host, port), app, handler_class=WebSocketHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('keyboard interrupt')
    dsc.stop()
    dsc_misc.stop()

if __name__ == '__main__':
    main()
