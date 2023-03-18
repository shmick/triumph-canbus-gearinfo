import board
import busio
import digitalio
import time
from adafruit_mcp2515.canio import Timer, Match
from adafruit_mcp2515.canio import RemoteTransmissionRequest, Message
from adafruit_mcp2515 import MCP2515 as CAN

# LoLin S2 board pins
# D0 = IO5 < CS
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

match = [Match(address=0x375), Match(address=0x375)]
# match = None

t = Timer(timeout=1)
next_message = None
message_num = 0
while True:
    # For debugging only - print occationally to show we're alive
    if t.expired:
        print(".", end="")
        t.rewind_to(1)
    with mcp.listen(match, timeout=0.1) as listener:
        message_count = listener.in_waiting()

        if message_count == 0:
            continue

        next_message = listener.receive()
        message_num = 0
        while not next_message is None:
            message_num += 1

            msg = next_message

            # if hex(msg.id) not in ["0x201"]:
            if hex(msg.id) in ["0x375"]:
                print("ID:", hex(msg.id), end=",")
                if isinstance(msg, Message):
                    if len(msg.data) > 0:
                        print("Data:", end="")
                        message_str = ",".join(["0x{:02X}".format(i) for i in msg.data])
                        # message_hex = ["0x{:02X}".format(i) for i in msg.data]
                        message_list = [hex(i) for i in msg.data]

                        print(message_str)
                        print(" list: ", message_list)

            #    making an assumption that it's the last field
            #    reportgear(message_list[7])

            next_message = listener.receive()
