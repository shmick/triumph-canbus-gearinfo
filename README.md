# triumph-canbus-gearinfo

Using a Wemos S2 Mini and an inexpensive MCP2515 CAN Bus module to read the gear selection on a 2012 Triumph Thunderbird

The CAN Bus message ID is `0x540`

The gear data is located in the first byte of the message

|    Range   | Gear |
|:----------:|:--:|
|0x00 - 0x0F | N |
|0x10 - 0x1F | 1 |
|0x20 - 0x2F | 2 |
|0x30 - 0x3F | 3 |
|0x40 - 0x4F | 4 |
|0x50 - 0x5F | 5 |
|0x60 - 0x6F | 6 |
