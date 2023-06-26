import board
import busio
import digitalio

# CANbus transceiver (TJA1050)
tx = board.IO18
rx = board.IO16
bps = 500000
match_id = 0x540

# Setup CANbus
can = canio.CAN(rx=rx, tx=tx, baudrate=bps, auto_restart=True, silent=True)
listener = can.listen(matches=[canio.Match(match_id)], timeout=0.001)

print(f"Silent: {can.silent}")
print(f"State: {can.state}")

# IO37 is connected to the gate pin of a BS170 MOSFET
# This will control a 12v LED to indicate that the motorcycle
# is in 6th gear
led = digitalio.DigitalInOut(board.IO37)
led.direction = digitalio.Direction.OUTPUT
led.value = False

debug_ignore_ids = ()
debug = 0

gear_map = {
    0: "N",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
}

"""
**********************************************************
There should not be any reason to modify things below here
**********************************************************
"""


def report_gear(msg_id, msg_data):

    # from https://www.triumph675.net/threads/ecu-to-dash-can-bus-message-ids.242889/
    # byte 0 - bits 6...4 - Gear Position - 0 = N, 1-6 = gears 1-6

    # turn the hex string into an integer
    byte_0 = int(msg_data[0], 16)

    # 0x70 is a mask that selects only the bits 6 to 4
    # the >> operator shifts them to the right by 4 positions to align them with the least significant bit
    bits_6_to_4 = (byte_0 & 0x70) >> 4

    gear = gear_map.get(bits_6_to_4, "")
    if gear:
        if msg_id == match_id and len(msg_data) == 7:
            print(f"*********\nGear: {gear}\n*********\n")

    if gear == "6":
        led.value = True
    else:
        led.value = False


def print_message(msg):
    if isinstance(msg, Message) and msg.data:
        msg_data = tuple("0x{:02X}".format(x) for x in msg.data)
        print(f"ID: {hex(msg.id)} Data: {msg_data}")
        report_gear(msg.id, msg_data)


def main_loop():
    while True:
    msg = listener.receive()
    if msg and msg.id and msg.data:
        if msg and not debug:
            print_message(msg)
        elif debug and msg.id not in ignore_ids:
            print_message(msg)


if __name__ == "__main__":
    print(f"baudrate: {mcp.baudrate}\nDebug: {debug}")
    ignore_ids = ()
    if debug:
        ignore_ids = debug_ignore_ids
        match_ids = []
    main_loop()
