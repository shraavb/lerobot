#!/usr/bin/env python3
"""Check voltage on all follower motors."""

import sys
sys.path.insert(0, "/Users/shraavastibhat/lerobot/src")

import scservo_sdk as scs

PORT = "/dev/cu.usbmodem5AAF2637511"  # Follower arm
BAUDRATE = 1000000

port_handler = scs.PortHandler(PORT)
packet_handler = scs.PacketHandler(0)

port_handler.openPort()
port_handler.setBaudRate(BAUDRATE)

motor_names = {1: "shoulder_pan", 2: "shoulder_lift", 3: "elbow_flex",
               4: "wrist_flex", 5: "wrist_roll", 6: "gripper"}

print("Voltage check on ALL follower motors:\n")

for motor_id in [1, 2, 3, 4, 5, 6]:
    data, result, _ = packet_handler.readTxRx(port_handler, motor_id, 62, 1)
    if result == scs.COMM_SUCCESS and data:
        voltage = data[0] / 10.0
        status = "LOW - needs power!" if voltage < 6.0 else "OK"
        print(f"  Motor {motor_id} ({motor_names[motor_id]}): {voltage:.1f}V  {status}")
    else:
        print(f"  Motor {motor_id} ({motor_names[motor_id]}): No response")

port_handler.closePort()

print("\n" + "="*50)
print("Motors need 7.4V-12V to move.")
print("5V = USB power only (can communicate but not move)")
print("Check the power supply connection to motors 1, 2, 6!")
