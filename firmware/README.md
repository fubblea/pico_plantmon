# Board Firmware

This is the firmware for the [Raspberry Pi Pico W](https://www.raspberrypi.org/products/raspberry-pi-pico/) board.

## Building

To build the firmware, you need to have the MicroPython installed on the board. You can find instructions on how to do that [here](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/0).

## Usage

### Create a secrets file

Create a new file called `secrets.py` in the same directory as the `run_server.py` file.

This file should contain the following variables:

```python
WIFI_SSID = "Your WIFI SSID"
WIFI_PASSWORD = "Your WIFI Password"
```

### Upload the firmware and run the server

Upload all the files to the board and run the `run_server.py` file.

The server will start on port 80 of the IP address that is assigned to the board.