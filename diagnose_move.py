#!/usr/bin/env python3
"""Test if motors can move and if that wakes up position reading."""

import sys
import time
sys.path.insert(0, "/Users/shraavastibhat/lerobot/src")

import scservo_sdk as scs

PORT = "/dev/cu.usbmodem5AA90244191"
BAUDRATE = 1000000

port_handler = scs.PortHandler(PORT)
packet_handler = scs.PacketHandler(0)

if not port_handler.openPort():
    print("Failed to open port")
    sys.exit(1)

if not port_handler.setBaudRate(BAUDRATE):
    print("Failed to set baudrate")
    sys.exit(1)

def read_position(motor_id):
    data, result, _ = packet_handler.readTxRx(port_handler, motor_id, 56, 2)
    if result == scs.COMM_SUCCESS and data:
        return data[0] + (data[1] << 8)
    return None

def write_2byte(motor_id, address, value):
    low = value & 0xFF
    high = (value >> 8) & 0xFF
    result, error = packet_handler.writeTxRx(port_handler, motor_id, address, 2, [low, high])
    return result == scs.COMM_SUCCESS

# Test with motor 6 (gripper) - safest to move
MOTOR_ID = 6
print(f"Testing with motor {MOTOR_ID} (gripper)\n")

# Read initial position
pos_before = read_position(MOTOR_ID)
print(f"Position before: {pos_before}")

# Check torque status
data, _, _ = packet_handler.readTxRx(port_handler, MOTOR_ID, 40, 1)
torque_status = data[0] if data else None
print(f"Torque enabled: {torque_status} (0=disabled, 1=enabled)")

# Try enabling torque
print("\nEnabling torque...")
result, _ = packet_handler.writeTxRx(port_handler, MOTOR_ID, 40, 1, [1])
time.sleep(0.5)

# Read position again
pos_after_torque = read_position(MOTOR_ID)
print(f"Position after enabling torque: {pos_after_torque}")

# Try writing a goal position (move slightly)
print("\nWriting goal position 2100 (slight move from center)...")
write_2byte(MOTOR_ID, 42, 2100)  # Goal_Position at address 42
time.sleep(1)

pos_after_move = read_position(MOTOR_ID)
print(f"Position after goal command: {pos_after_move}")

# Move back
print("\nWriting goal position 2047 (back to center)...")
write_2byte(MOTOR_ID, 42, 2047)
time.sleep(1)

pos_final = read_position(MOTOR_ID)
print(f"Final position: {pos_final}")

# Disable torque
print("\nDisabling torque...")
packet_handler.writeTxRx(port_handler, MOTOR_ID, 40, 1, [0])

print("\n--- Summary ---")
print(f"Did the gripper physically move? (You should have seen it open/close slightly)")
print(f"If YES but positions stayed ~2047: Encoder issue / power issue")
print(f"If NO movement: Arm is not powered or motor issue")

port_handler.closePort()
