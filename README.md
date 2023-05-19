Using [CircuitPython](https://circuitpython.org/) on a [Wemos S2 Mini](https://circuitpython.org/board/lolin_s2_mini/) with an inexpensive MCP2515 CAN Bus module (eBay, Amazon, etc ) to read the gear selection on a 2012 Triumph Thunderbird

The CAN Bus message ID is `0x540`

The selected gear is located in the first byte of the message data, using the binary value of bits 6 to 4 

|Gear| Hex Range | Binary Range        |Bits 6-4|
|:-:|:----------:|:-------------------:|:------:|
| N |0x00 - 0x0F | 00000000 - 00001111 |  000  |
| 1 |0x10 - 0x1F | 00010000 - 00011111 |  001  |
| 2 |0x20 - 0x2F | 00100000 - 00101111 |  010  |
| 3 |0x30 - 0x3F | 00110000 - 00111111 |  011  |
| 4 |0x40 - 0x4F | 01000000 - 01001111 |  100  |
| 5 |0x50 - 0x5F | 01010000 - 01011111 |  101  |
| 6 |0x60 - 0x6F | 01100000 - 01101111 |  110  |

An example of a message for 5th gear

`ID: 0x540 Data: ('0x5C', '0x2C', '0x01', '0x00', '0x00', '0x00', '0x00')`

The first byte shows `0x5C` which is in the range of `0x50` to `0x5F`

Credit to DickC on the [triumph675.net](https://www.triumph675.net/threads/ecu-to-dash-can-bus-message-ids.242889/) forum
