#!/usr/bin/env python3
"""Test if follower motors 1, 2, 6 can move."""

import sys
import time
sys.path.insert(0, "/Users/shraavastibhat/lerobot/src")

import scservo_sdk as scs

PORT = "/dev/cu.usbmodem5AAF2637511"  # Follower arm
BAUDRATE = 1000000

port_handler = scs.PortHandler(PORT)
packet_handler = scs.PacketHandler(0)

port_handler.openPort()
port_handler.setBaudRate(BAUDRATE)

def read_2byte(motor_id, address):
    data, result, _ = packet_handler.readTxRx(port_handler, motor_id, address, 2)
    if result == scs.COMM_SUCCESS and data:
        return data[0] + (data[1] << 8)
    return None

def write_2byte(motor_id, address, value):
    low = value & 0xFF
    high = (value >> 8) & 0xFF
    packet_handler.writeTxRx(port_handler, motor_id, address, 2, [low, high])

motor_names = {1: "F1 shoulder_pan", 2: "F2 shoulder_lift", 6: "F6 gripper"}

print("Testing follower motors 1, 2, 6...\n")

for motor_id in [1, 2, 6]:
    name = motor_names[motor_id]

    # Read current position
    pos = read_2byte(motor_id, 56)
    print(f"{name}: Current position = {pos}")

    # Check torque
    data, _, _ = packet_handler.readTxRx(port_handler, motor_id, 40, 1)
    torque = data[0] if data else None
    print(f"  Torque enabled: {torque}")

    # Enable torque
    print(f"  Enabling torque...")
    packet_handler.writeTxRx(port_handler, motor_id, 40, 1, [1])
    time.sleep(0.2)

    # Move slightly (±100 from current position)
    target = pos + 100 if pos < 2048 else pos - 100
    print(f"  Moving to {target}...")
    write_2byte(motor_id, 42, target)
    time.sleep(0.8)

    new_pos = read_2byte(motor_id, 56)
    print(f"  New position = {new_pos}")

    # Move back
    print(f"  Moving back to {pos}...")
    write_2byte(motor_id, 42, pos)
    time.sleep(0.8)

    # Disable torque
    packet_handler.writeTxRx(port_handler, motor_id, 40, 1, [0])
    print()

port_handler.closePort()
print("Done - watch if the follower motors moved!")
