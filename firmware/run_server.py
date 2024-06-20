import secrets
import socket
from time import sleep

import machine
import network
from machine import Pin

from states import State

ssid = secrets.WIFI_SSID
password = secrets.WIFI_PASSWORD

assert ssid is not None
assert password is not None


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
    # Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <body>
                <form action="./happy">
                <input type="submit" value="Be Happy" />
                </form>
                <form action="./sad">
                <input type="submit" value="Be Sad" />
                </form>
                <p><pre>{state}</pre></p>
            </body>
            </html>
            """
    return str(html)


def serve(connection):
    # Get pinouts
    pico_led = Pin(25, Pin.OUT)

    # Start a web server
    state = State.HAPPY

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
            pico_led.on()
            state = State.HAPPY
            print("Happy")
        elif request == "/sad?":
            pico_led.off()
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
