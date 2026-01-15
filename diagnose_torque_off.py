#!/usr/bin/env python3
"""Test if position reads correctly with torque OFF while moving manually."""

import sys
import time
sys.path.insert(0, "/Users/shraavastibhat/lerobot/src")

import scservo_sdk as scs

PORT = "/dev/cu.usbmodem5AA90244191"
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

# Disable torque on motor 1
print("Disabling torque on motor 1 (shoulder_pan)...")
packet_handler.writeTxRx(port_handler, 1, 40, 1, [0])
time.sleep(0.2)

print("\n*** Physically MOVE the shoulder joint by hand! ***")
print("Reading position every second for 10 seconds...\n")

for i in range(10):
    pos = read_2byte(1, 56)
    print(f"  {i+1}: Present Position = {pos}")
    time.sleep(1)

port_handler.closePort()
print("\nIf position stayed ~2047 despite movement, these motors")
print("don't report position when torque is disabled (firmware issue).")
