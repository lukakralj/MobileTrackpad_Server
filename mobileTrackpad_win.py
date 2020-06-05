import eventlet
import socketio
import pyautogui 


port = 3333 # Set port to use.


sio = socketio.Server()
app = socketio.WSGIApp(sio)

def moveMouse(dx, dy):
    pyautogui.moveRel(dx, dy, 0)

def mouseClick():
    pyautogui.click(button='left')

@sio.event
def connect(sid, environ):
    print('======connected')

@sio.on("mouse_delta")
def mouse_delta(sid, data):
    moveMouse(data["dx"], data["dy"])

@sio.on("mouse_click")
def mouse_delta(sid, data):
    mouseClick()

@sio.event
def disconnect(sid):
    print('======disconnected')

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(("", port)), app)


