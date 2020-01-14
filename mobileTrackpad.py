import eventlet
import socketio
import os

sio = socketio.Server()
app = socketio.WSGIApp(sio)

def moveMouse(dx, dy):
    os.system("xte \"mousermove " + str(dx) + " " + str(dy) + "\"")

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.on("mouse_delta")
def mouse_delta(sid, data):
    moveMouse(data["dx"], data["dy"])

@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(("", 3333)), app)

