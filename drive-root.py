#!/usr/bin/env python3

from pyroot import Root
import time
import argparse

parser = argparse.ArgumentParser(description='Quick and dirty robot test.')
parser.add_argument('-n', '--name', type=str, help='Name of robot to connect to')
parser.add_argument('-p', '--ser_port', type=str, help='If supplied, serial port to connect to (otherwise use BLE)')
args = parser.parse_args()

command = ""
try:
    if args.ser_port:
        from pyroot import RootSerial
        robot = Root(RootSerial(name = args.name, dev = args.ser_port))
    else:
        from pyroot import RootGATT
        robot = Root(RootGATT(name = args.name))

    print("Press letter (f,b,l,r) to drive robot (t) to turn, (s) to stop, (u or d) raise pen up or down, (m {val}) to move, (a {val}) to rotate, (z) to get robot states, (i) for sniff, (n {str}) to change name, (q) to quit")
    while command != "q" and robot.is_running():
        command = input('> ') # wait for keyboard input
        if command == '':
            continue
        if command == "f":
            print("Drive forward")
            robot.set_motor_speeds(100, 100)
        if command == "b":
            print("Drive backwards")
            robot.set_motor_speeds(-100, -100)
        if command == "r":
            print("Drive right")
            robot.set_motor_speeds(100, 0)
        if command == "l":
            print("Drive left")
            robot.set_motor_speeds(0, 100)
        if command == "s":
            print("Stop")
            robot.set_motor_speeds(0, 0)
        if command == "u":
            print("Pen up")
            robot.set_marker_eraser_pos(robot.marker_up_eraser_up)
        if command == "d":
            print("Pen down")
            robot.set_marker_eraser_pos(robot.marker_down_eraser_up)
        if command[0] == "m":
            try:
                dist = int(command.split()[1])
                print("Moving", dist, 'mm')
                robot.drive_distance(dist)
            except:
                print("Bad command")
        if command[0] == "a":
            try:
                angle = int(command.split()[1])
                print("Rotating", angle, 'decidegrees')
                robot.rotate_angle(angle)
            except:
                print("Bad command")
        if command == "z":
            for s, v in robot.state.items():
                print(s, v)
        if command == 'i':
            robot.set_sniff_mode(not robot.get_sniff_mode())
        if command[0] == "n":
            try:
                name = command.split()[1]
                print("Changed name to", robot.set_name(name))
            except:
                print("Bad command")
        if command == ',':
            for i in range(4):
                robot.drive_distance(100)
                robot.rotate_angle(900)
        if command == '`':
            robot.get_versions(robot.main_board)
            robot.get_versions(robot.color_board)
            robot.get_battery_level()
            robot.get_name()

except (KeyboardInterrupt, TimeoutError) as e:
    print(e)

print("Quitting")
try:
    robot.disconnect()
except NameError: # never connected
    pass
