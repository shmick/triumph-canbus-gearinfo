import board
import busio
import digitalio
from adafruit_mcp2515.canio import Message, Match
from adafruit_mcp2515 import MCP2515 as CAN


cs = digitalio.DigitalInOut(board.IO5)
cs.switch_to_output()
# D5/IO7 = SCK, D7/IO11 = MOSI, D6/IO9 = MISO
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
mcp = CAN(spi, cs, baudrate=1000000)

match_id = 0x540
match_ids = [
    Match(address=match_id, mask=0x7FF),
    Match(address=match_id, mask=0x7FF),
]

debug_ignore_ids = ()
debug = 0

"""
**********************************************************
There should not be any reason to modify things below here
**********************************************************
"""


def report_gear(msg_id, msg_data):
    gear_map = {
        0: "N",
        1: "1",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
    }

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


def print_message(msg):
    if isinstance(msg, Message) and msg.data:
        msg_data = tuple("0x{:02X}".format(x) for x in msg.data)
        print(f"ID: {hex(msg.id)} Data: {msg_data}")
        report_gear(msg.id, msg_data)


def main_loop():
    with mcp.listen(matches=match_ids, timeout=0.1) as listener:
        while True:
            msg = listener.receive()
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
