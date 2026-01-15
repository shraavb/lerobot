#!/usr/bin/env python3
"""Read raw bytes directly from motors to check encoding."""

import sys
sys.path.insert(0, "/Users/shraavastibhat/lerobot/src")

import scservo_sdk as scs

PORT = "/dev/cu.usbmodem5AA90244191"
BAUDRATE = 1000000
PRESENT_POSITION_ADDR = 56
PRESENT_POSITION_LEN = 2

port_handler = scs.PortHandler(PORT)
packet_handler = scs.PacketHandler(0)  # Protocol 0 for STS series

if not port_handler.openPort():
    print("Failed to open port")
    sys.exit(1)

if not port_handler.setBaudRate(BAUDRATE):
    print("Failed to set baudrate")
    sys.exit(1)

print("Reading raw Present_Position bytes from each motor:\n")

for motor_id in range(1, 7):
    motor_names = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper"]
    name = motor_names[motor_id - 1]

    # Read 2 bytes from address 56
    data, result, error = packet_handler.readTxRx(port_handler, motor_id, PRESENT_POSITION_ADDR, PRESENT_POSITION_LEN)

    if result != scs.COMM_SUCCESS:
        print(f"Motor {motor_id} ({name}): Communication error - {packet_handler.getTxRxResult(result)}")
        continue

    if error != 0:
        print(f"Motor {motor_id} ({name}): Error status - {error}")

    # data is a tuple of bytes
    if data:
        raw_bytes = list(data)
        raw_value = raw_bytes[0] + (raw_bytes[1] << 8)  # Little endian

        # Check sign bit (bit 15)
        sign_bit = (raw_value >> 15) & 1
        magnitude = raw_value & 0x7FFF  # Lower 15 bits

        if sign_bit:
            decoded = -magnitude
        else:
            decoded = magnitude

        print(f"Motor {motor_id} ({name}):")
        print(f"  Raw bytes: {raw_bytes}")
        print(f"  Raw value (16-bit): {raw_value}")
        print(f"  Sign bit: {sign_bit}, Magnitude: {magnitude}")
        print(f"  Decoded value: {decoded}")
        print()
    else:
        print(f"Motor {motor_id} ({name}): No data received")

# Also read Min/Max position limits
print("\n--- Position Limits (EPROM) ---\n")
for motor_id in range(1, 7):
    motor_names = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper"]
    name = motor_names[motor_id - 1]

    # Min Position Limit at address 9
    data_min, _, _ = packet_handler.readTxRx(port_handler, motor_id, 9, 2)
    # Max Position Limit at address 11
    data_max, _, _ = packet_handler.readTxRx(port_handler, motor_id, 11, 2)

    if data_min and data_max:
        min_val = data_min[0] + (data_min[1] << 8)
        max_val = data_max[0] + (data_max[1] << 8)
        print(f"Motor {motor_id} ({name}): Min={min_val}, Max={max_val}")

port_handler.closePort()
print("\nDone")
