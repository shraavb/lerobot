#!/usr/bin/env python3
"""Deep diagnostic - check operating mode, firmware, and alternate position registers."""

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

port_handler.setBaudRate(BAUDRATE)

def read_byte(motor_id, address):
    data, result, _ = packet_handler.readTxRx(port_handler, motor_id, address, 1)
    if result == scs.COMM_SUCCESS and data:
        return data[0]
    return None

def read_2byte(motor_id, address):
    data, result, _ = packet_handler.readTxRx(port_handler, motor_id, address, 2)
    if result == scs.COMM_SUCCESS and data:
        return data[0] + (data[1] << 8)
    return None

print("=== Deep Motor Diagnostic ===\n")

for motor_id in [1, 6]:  # Just check motor 1 and 6
    name = "shoulder_pan" if motor_id == 1 else "gripper"
    print(f"--- Motor {motor_id} ({name}) ---")

    # Firmware version
    fw_major = read_byte(motor_id, 0)
    fw_minor = read_byte(motor_id, 1)
    print(f"Firmware: {fw_major}.{fw_minor}")

    # Model number
    model = read_2byte(motor_id, 3)
    print(f"Model Number: {model}")

    # Operating mode (address 33)
    op_mode = read_byte(motor_id, 33)
    print(f"Operating Mode: {op_mode} (0=position, 1=velocity, 2=PWM, 3=step)")

    # Torque enable
    torque = read_byte(motor_id, 40)
    print(f"Torque Enable: {torque}")

    # Goal Position (address 42)
    goal_pos = read_2byte(motor_id, 42)
    print(f"Goal Position: {goal_pos}")

    # Present Position (address 56)
    present_pos = read_2byte(motor_id, 56)
    print(f"Present Position: {present_pos}")

    # Present Velocity (address 58)
    present_vel = read_2byte(motor_id, 58)
    print(f"Present Velocity: {present_vel}")

    # Present Load (address 60)
    present_load = read_2byte(motor_id, 60)
    print(f"Present Load: {present_load}")

    # Lock register (address 55)
    lock = read_byte(motor_id, 55)
    print(f"Lock: {lock}")

    # Moving flag (address 66)
    moving = read_byte(motor_id, 66)
    print(f"Moving: {moving}")

    # Status (address 65)
    status = read_byte(motor_id, 65)
    print(f"Status: {status}")

    print()

# Now let's try moving motor 1 and watch both goal and present position
print("=== Movement Test with Motor 1 ===\n")
motor_id = 1

# Enable torque
packet_handler.writeTxRx(port_handler, motor_id, 40, 1, [1])
time.sleep(0.2)

print("Moving motor 1 through positions 1500, 2000, 2500...")
for goal in [1500, 2000, 2500, 2047]:
    low = goal & 0xFF
    high = (goal >> 8) & 0xFF
    packet_handler.writeTxRx(port_handler, motor_id, 42, 2, [low, high])
    time.sleep(0.8)

    goal_read = read_2byte(motor_id, 42)
    present_read = read_2byte(motor_id, 56)
    print(f"  Goal written: {goal}, Goal read: {goal_read}, Present: {present_read}")

# Disable torque
packet_handler.writeTxRx(port_handler, motor_id, 40, 1, [0])

port_handler.closePort()
print("\nDone")
