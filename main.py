import board
import busio
import digitalio
import time
import supervisor

from adafruit_mcp2515.canio import Timer, Match
from adafruit_mcp2515.canio import RemoteTransmissionRequest, Message
from adafruit_mcp2515 import MCP2515 as CAN

# LoLin S2 board pins
# D0 = board.IO5 < CS
# D1 = IO35
# D2 = IO33
# D3 = IO18
# D4 = IO16
# D5 = IO7 < SCK
# D6 = IO9 < MISO
# D7 = IO11 < MOSI
# D8 = IO13


def blink_LED(num_blinks):
    led = digitalio.DigitalInOut(board.LED)
    led.direction = digitalio.Direction.OUTPUT

    for i in range(num_blinks):
        led.value = True
        start_time = time.monotonic()
        while (time.monotonic() - start_time) < 0.5:
            pass
        led.value = False
        start_time = time.monotonic()
        while (time.monotonic() - start_time) < 0.5:
            pass


blink_LED(2)

cs = digitalio.DigitalInOut(board.IO5)
cs.switch_to_output()
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

can_baudrate = 500000
can_baudrate = 1000000  # needed for Subaru

mcp = CAN(spi, cs, baudrate=can_baudrate)

print("baudrate:", mcp.baudrate)
print("state:", mcp.state)
print("Watching for received codes")


match_ids = [Match(address=0x375, mask=0x375), Match(address=0x375, mask=0x375)]
ignore_ids = ()

debug = True

if debug:
    match_ids = None
    # While determining what IDs we want to match on, keep expanding the ignore list to cut down on noise
    ignore_ids = ("0x201", "0x202")


def print_message(msg):
    msg_id = hex(msg.id)
    print(f"ID: {msg_id}")
    if isinstance(msg, Message):
        if msg.data:
            message_str = ",".join(f"0x{i:02X}" for i in msg.data)
            message_list = [hex(i) for i in msg.data]
            print(f"Data: {message_str}\nList: {message_list}")


print(f"Debug: {debug}")

t = Timer(timeout=5)
next_message = None
message_num = 0
while True:
    # For debugging only - print occationally to show we're alive
    if t.expired:
        print(supervisor.ticks_ms())
        t.rewind_to(1)
    with mcp.listen(matches=match_ids, timeout=1) as listener:
        if listener.in_waiting():
            msg = listener.receive()
            if not debug:
                print_message(msg)
            elif debug and hex(msg.id) not in ignore_ids:
                print_message(msg)
