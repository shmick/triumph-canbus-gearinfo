import time
import board
import busio
import canio

tx_pin = board.IO16  # TX pin of TJA1050
rx_pin = board.IO18  # RX pin of TJA1050
bps = 500000

# Create a CAN bus instance
can = canio.CAN(rx=rx_pin, tx=tx_pin, baudrate=bps, auto_restart=True)

# Define the CAN message to transmit
tx_message = canio.Message(
    id=0x540,  # ID you want to transmit
    data=bytes([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]),
    extended=False,  # Set to True if you're using an extended ID
)

# Timer setup
transmit_interval = 1.0  # 1 second
last_transmit_time = time.monotonic()


# Set up the listener
listener = can.listen(timeout=0.001)

# Main loop
try:
    while True:
        # Check if it's time to transmit
        current_time = time.monotonic()
        if current_time - last_transmit_time >= transmit_interval:
            # Transmit the message
            can.send(tx_message)
            print(
                f"Transmitted message ID 0x{tx_message.id:X} with data: {tx_message.data}"
            )

            # Update the last transmit time
            last_transmit_time = current_time
        
        message = listener.receive()
        if message is not None:
            print(f"Received message ID: 0x{message.id:X} Data: {message.data}")


except KeyboardInterrupt:
    pass
