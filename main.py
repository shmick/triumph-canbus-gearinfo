import board
import busio
import digitalio
import time
import supervisor
from adafruit_mcp2515.canio import Timer, Match, Message
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

ignore_ids = ()
match_id = 0x375
match_ids = [
    Match(address=match_id, mask=match_id),
    Match(address=match_id, mask=match_id),
]

debug = 1


def print_message(msg):
    if isinstance(msg, Message) and msg.data:
        msg_id = hex(msg.id)
        # msg_tuple = tuple(hex(x) for x in msg.data)
        msg_data = tuple("0x{:02x}".format(x) for x in msg.data)
        print(f"ID: {msg_id} Data: {msg_data}")
        # send the data to another function for further processing
        # process_message(msg_id, msg_tuple)


def main_loop():
    with mcp.listen(matches=match_ids, timeout=1) as listener:
        while True:
            try:
                msg = listener.receive()
                if msg and (not debug or hex(msg.id) not in ignore_ids):
                    print_message(msg)
            except TimeoutError:
                pass

            if debug:
                ticks = supervisor.ticks_ms()
                # For debugging only - print occationally to show we're alive
                if t.expired:
                    print(ticks)
                    t.rewind_to(1)


if __name__ == "__main__":
    print(f"baudrate: {mcp.baudrate}\nDebug: {debug}")
    if debug:
        t = Timer(timeout=5)
        match_ids = None
        # While determining what IDs we want to match on, keep expanding the ignore list to cut down on noise
        ignore_ids = ("0x201", "0x202")
    main_loop()
