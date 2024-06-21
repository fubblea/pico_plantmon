import secrets
import socket
from time import sleep

import machine
import network
from machine import Pin

from states import State

# These are taken from secrets.py.
# Look at the README for more information.
ssid = secrets.WIFI_SSID
password = secrets.WIFI_PASSWORD

assert (
    ssid is not None
), "Please set the WIFI_SSID in secrets.py. Look at the README for more information."
assert (
    password is not None
), "Please set the WIFI_PASSWORD in secrets.py. Look at the README for more information."


def connect() -> str:
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() is False:
        print("Waiting for connection...")
        sleep(1)

    print("Connected to WLAN at IP address", wlan.ifconfig()[0])
    return wlan.ifconfig()[0]


def open_socket(ip: str) -> socket:
    # Open a socket
    PORT = 80
    address = (ip, PORT)

    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)

    print("Connected to port", PORT)
    print(connection)
    return connection


def webpage(state: str) -> str:
    with open("index.html", "r") as f:
        html = f.read()

        html = html.replace("{{ state }}", state)

    return str(html)


def serve(connection):
    # Get pinouts
    pico_led = Pin(25, Pin.OUT)

    # Start a web server
    state = State.HAPPY

    # Status indicator to indicate that the server is running
    pico_led.off()  # Sometimes need to turn it off first
    pico_led.on()

    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        print(request)

        try:
            request = request.split()[1]
        except IndexError:
            pass

        if request == "/happy?":
            state = State.HAPPY
            print("Happy")
        elif request == "/sad?":
            state = State.SAD
            print("Sad")

        html = webpage(state)
        client.send(html)
        client.close()


try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    print("Exiting...")
    machine.reset()
