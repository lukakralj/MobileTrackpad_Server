#!/usr/bin/env python2

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


############## MOUSE CONTROL FUNCTIONS ##############

def performMouseDelta(dx, dy):
    # PyAutoGui is lagging too much. xte seems to be working slightly faster than xdotool
    #os.system("xdotool mousemove_relative -- " + str(dx) + " " + str(dy))
    os.system("xte \"mousermove " + str(dx) + " " + str(dy) + "\"")

def performLeftClick():
    os.system("xte \"mouseclick 1\"")

def performRightClick():
    os.system("xte \"mouseclick 3\"")

def performLeftDown():
    os.system("xte \"mousedown 1\"")

def performLeftUp():
    os.system("xte \"mouseup 1\"")

def performScrollUp(amount):
    for _ in range(amount):
        os.system("xte \"mouseClick 4\"")

def performScrollDown(amount):
    for _ in range(amount):
        os.system("xte \"mouseClick 5\"")

# zoom could be simulated with ctrl + click 4/5

############## ENDPOINTS SETUP ##############


@sio.event
def connect(sid, environ):
    print('======connected')

@sio.on("mouseDelta")
def mouseDelta(sid, data):
    performMouseDelta(data["dx"], data["dy"])

@sio.on("leftClick")
def leftClick(sid, data):
    performLeftClick()

@sio.on("rightClick")
def rightClick(sid, data):
    performRightClick()

@sio.on("leftDown")
def leftDown(sid, data):
    performLeftDown()

@sio.on("leftUp")
def leftUp(sid, data):
    performLeftUp()

@sio.on("scrollUp")
def scrollUp(sid, data):
    performScrollUp(data["amount"])
    
@sio.on("scrollDown")
def scrollDown(sid, data):
    performScrollDown(data["amount"])

# TODO: add horizontal scroll (buttons 6 and 7?)

@sio.event
def disconnect(sid):
    print('======disconnected')


############## SERVER SETUP  ##############

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