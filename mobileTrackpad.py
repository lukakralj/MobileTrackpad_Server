import eventlet
import socketio
import socket 
import os
from subprocess import Popen, PIPE

port = 3333 # Set port to use.

# Prerequisites
#   - root access (?)
#   - xdotool: install with: sudo apt-get install xdotool
#   - ifconfig: to parse the local IP
#   - ufw (Uncomplicated Firewall): used to open a port for the server and then close it.

sio = socketio.Server()
app = socketio.WSGIApp(sio)

def moveMouse(dx, dy):
    os.system("xdotool mousemove_relative -- " + str(dx) + " " + str(dy))

def mouseClick():
    os.system("xdotool click 1")

def leftDown():
    os.system("xdotool mousedown 1")

def rightDown():
    os.system("xdotool mousedown 3")

def wheelUp():
    os.system("xdotool click 4")

def wheelDown():
    os.system("xdotool click 5")

# zoom could be simulated with ctrl + click 4/5

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

#--------------------------
# Extract IP
p = Popen(["ifconfig wlo1 | grep \"inet \" | awk -F'[: ]+' '{ print $3 }'"], 
                stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
output, err = p.communicate()

if len(output) > 0 and output[-1] == "\n":
    output = output[:-1]
#--------------------------

print("======================")
print("Welcome!\n")
print("Connect mobile app to:\n - IP: " + str(output) + 
        "\n - Port: " + str(port) + ".")
print("======================\n")

print("\nOpening port: " + str(port) +". Enter root password if prompted.")
p = Popen(["sudo ufw allow " + str(port) + "/tcp"], 
                stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
output, err = p.communicate()
if not err:
    print(output)
    print("Port open.\n")
else: 
    print(err)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(("", port)), app)

print("\nClosing port: " + str(port) +". Enter root password if prompted.")
p = Popen(["sudo ufw delete allow " + str(port) + "/tcp"], 
                stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
output, err = p.communicate()
if not err:
    print(output)
    print("Port closed.\nExiting...")
else: 
    print(err)