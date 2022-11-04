from urx import robotiq_two_finger_gripper
import time
import socket
from typing import List
import urx

HOST = "192.168.0.16" # IP del robot
PORT = 30002 # port: 30001, 30002 o 30003, en ambos extremos

rob = urx.Robot(HOST)
robotiqgrip = robotiq_two_finger_gripper.Robotiq_Two_Finger_Gripper(rob)
print("conectando a gripper...")
time.sleep(1)


print("Conectando a IP: ", HOST)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("conectando...")
s.connect((HOST, PORT))
time.sleep(0.5)
print("Conectado con el robot")

print("abrir gripper")
rob.send_program(str(robotiqgrip.open_gripper()))

print("cerrar gripper")
rob.send_program(str(robotiqgrip.close_gripper()))


print("partial")
rob.send_program(str(robotiqgrip.gripper_action(165)))
