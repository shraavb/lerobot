#!/usr/bin/env python3
"""Check and disable torque on leader arm."""

import sys
sys.path.insert(0, "/Users/shraavastibhat/lerobot/src")

import scservo_sdk as scs

PORT = "/dev/cu.usbmodem5AA90244191"  # Leader arm
BAUDRATE = 1000000

port_handler = scs.PortHandler(PORT)
packet_handler = scs.PacketHandler(0)

port_handler.openPort()
port_handler.setBaudRate(BAUDRATE)

motor_names = {1: "L1 shoulder_pan", 2: "L2 shoulder_lift", 3: "L3 elbow_flex",
               4: "L4 wrist_flex", 5: "L5 wrist_roll", 6: "L6 gripper"}

print("Checking torque status on leader arm...\n")

for motor_id in [1, 2, 3, 4, 5, 6]:
    data, result, _ = packet_handler.readTxRx(port_handler, motor_id, 40, 1)
    if result == scs.COMM_SUCCESS and data:
        torque = data[0]
        status = "ENABLED (locked)" if torque else "disabled (free)"
        print(f"  {motor_names[motor_id]}: Torque {status}")

print("\nDisabling torque on all leader motors...")
for motor_id in [1, 2, 3, 4, 5, 6]:
    packet_handler.writeTxRx(port_handler, motor_id, 40, 1, [0])

print("Done - leader arm should now move freely by hand")
port_handler.closePort()
