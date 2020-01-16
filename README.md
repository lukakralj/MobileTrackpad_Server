# MobileTrackpad (server)

A weekend project that transforms a phone's screen into a trackpad for a laptop mouse. This repository contain the script that 
needs to be running on the laptop if we want to use the mobile app described in [this repository](https://github.com/lukakralj/MobileTrackpad).

This script should run on most Linux distros. Might even run on MacOS. On Windows? If it does, I owe you a coffee.

### Installation

For this script to run properly make sure the following programs are installed:

  - `ifconfig`: Used to parse the local IP to be used in the mobile app.
  - `ufw` (Uncomplicated Firewall): Used to open a port for the server and then close it when the script is stopped.

There are good odds that these two are already installed by default. But you will also need this:
  - `xdotool`: Used to simulate mouse movements. Install with: `sudo apt-get install xdotool` (Note: it might be some other package manager on other distros).
  
In order to open and close the ports, you will be prompted to enter the root user password.

To start the server, run `python /path/to/mobileTrackpad.py`. Follow the instructions on the screen.
