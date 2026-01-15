#!/usr/bin/env python3
"""Test ALL follower motors to see which ones respond."""

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

motor_names = {1: "shoulder_pan", 2: "shoulder_lift", 3: "elbow_flex",
               4: "wrist_flex", 5: "wrist_roll", 6: "gripper"}

print(f"Testing ALL follower motors on {PORT}...\n")

results = {}

for motor_id in [1, 2, 3, 4, 5, 6]:
    name = motor_names[motor_id]
    print(f"--- Motor {motor_id} ({name}) ---")

    # Read current position
    pos = read_2byte(motor_id, 56)
    print(f"  Current position: {pos}")

    if pos is None:
        print(f"  FAILED to read position!")
        results[motor_id] = "NO RESPONSE"
        continue

    # Enable torque
    packet_handler.writeTxRx(port_handler, motor_id, 40, 1, [1])
    time.sleep(0.1)

    # Try to move
    target = 2048  # Move toward center
    print(f"  Moving to {target}...")
    write_2byte(motor_id, 42, target)
    time.sleep(0.5)

    new_pos = read_2byte(motor_id, 56)
    moved = abs(new_pos - pos) > 10 if new_pos else False
    print(f"  New position: {new_pos} (moved: {moved})")

    # Move back
    write_2byte(motor_id, 42, pos)
    time.sleep(0.5)

    # Disable torque
    packet_handler.writeTxRx(port_handler, motor_id, 40, 1, [0])

    results[motor_id] = "OK" if moved else "NO MOVEMENT"
    print()

print("=== SUMMARY ===")
for motor_id, status in results.items():
    name = motor_names[motor_id]
    symbol = "✓" if status == "OK" else "✗"
    print(f"  {symbol} Motor {motor_id} ({name}): {status}")

port_handler.closePort()
