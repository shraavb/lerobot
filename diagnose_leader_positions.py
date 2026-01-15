#!/usr/bin/env python3
"""Test leader arm motor positions - especially L1, L2, L6."""

import sys
import time
sys.path.insert(0, "/Users/shraavastibhat/lerobot/src")

import scservo_sdk as scs

PORT = "/dev/cu.usbmodem5AA90244191"  # Leader arm
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

motor_names = {1: "L1 shoulder_pan", 2: "L2 shoulder_lift", 3: "L3 elbow_flex",
               4: "L4 wrist_flex", 5: "L5 wrist_roll", 6: "L6 gripper"}

print("Reading leader arm positions...")
print("Move L1 (base), L2 (shoulder), and L6 (gripper) and watch if values change\n")

for i in range(10):
    print(f"Read {i+1}:")
    for motor_id in [1, 2, 3, 4, 5, 6]:
        pos = read_2byte(motor_id, 56)  # Present_Position
        print(f"  {motor_names[motor_id]}: {pos}")
    print()
    time.sleep(1)

port_handler.closePort()
