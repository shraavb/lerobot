# SO-100 Motor Configuration Reference

## Ports

| Arm | Port |
|-----|------|
| Follower | `/dev/tty.usbmodem5AAF2637511` |
| Leader | `/dev/tty.usbmodem5AA90244191` |

## Follower Arm Motors

| Motor | Joint | ID | Motor Model | Gear Ratio |
|-------|-------|-----|-------------|------------|
| F1 | shoulder_pan | 1 | ST-3215-C001 (7.4V) | 1:345 |
| F2 | shoulder_lift | 2 | ST-3215-C001 (7.4V) | 1:345 |
| F3 | elbow_flex | 3 | ST-3215-C001 (7.4V) | 1:345 |
| F4 | wrist_flex | 4 | ST-3215-C001 (7.4V) | 1:345 |
| F5 | wrist_roll | 5 | ST-3215-C001 (7.4V) | 1:345 |
| F6 | gripper | 6 | ST-3215-C001 (7.4V) | 1:345 |

Note: Follower arm can also use C018 or C047 (12V) variants.

## Leader Arm Motors

| Motor | Joint | ID | Motor Model | Gear Ratio |
|-------|-------|-----|-------------|------------|
| L1 | shoulder_pan | 1 | ST-3215-C044 (7.4V) | 1:191 |
| L2 | shoulder_lift | 2 | ST-3215-C001 (7.4V) | 1:345 |
| L3 | elbow_flex | 3 | ST-3215-C044 (7.4V) | 1:191 |
| L4 | wrist_flex | 4 | ST-3215-C046 (7.4V) | 1:147 |
| L5 | wrist_roll | 5 | ST-3215-C046 (7.4V) | 1:147 |
| L6 | gripper | 6 | ST-3215-C046 (7.4V) | 1:147 |

Note: Leader arm uses optimized gear ratios for easier manual control.

## Calibration Commands

```bash
# Follower arm
lerobot-calibrate \
    --robot.type=so100_follower \
    --robot.port=/dev/tty.usbmodem5AAF2637511 \
    --robot.id=my_follower_arm

# Leader arm
lerobot-calibrate \
    --teleop.type=so100_leader \
    --teleop.port=/dev/tty.usbmodem5AA90244191 \
    --teleop.id=my_leader_arm
```
