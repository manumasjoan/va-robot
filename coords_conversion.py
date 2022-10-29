from operator import invert
from turtle import distance
from xml.etree.ElementTree import tostring
import cv2 as cv
import numpy as np
import sys
import math
from urx import robotiq_two_finger_gripper
import time
import socket
from typing import List
import urx
from detector import read_camera_parameters, get_delta_cam, get_centers






# MAIN
print("------------------------------------------------------------")
print("                     BIENVENIDO                             ")
print("------------------------------------------------------------")

# Conect to robot:
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

def convert(qr_cam, qr_rob, f, p): 

    var_x = p[0] - qr_cam[0]
    var_y = p[1] - qr_cam[1]

    f_var_x = var_x*f[0]
    f_var_y = var_y*f[1]

    return [f_var_x+qr_rob[0], f_var_y+qr_rob[1]]


# PASO 0: obtener parametros de camara --------------------------------

s.send(b"movel(p[0.271, -0.157, 0.040, 0, 3.14, 0], 0.1, 0.2)\n")

time.sleep(5)

# OPEN GRIPPER
urscript = robotiqgrip._get_new_urscript()

rob.send_program(str(urscript._set_gripper_position(165)))



# robotiqgrip.gripper_action(value=165)

# robotiqgrip._get_new_urscript()._set_gripper_position(165)

time.sleep(5)

cmtx, dist = read_camera_parameters()

INPUT_SOURCE = 1

cap = cv.VideoCapture(INPUT_SOURCE)

# qr = cv.QRCodeDetector()

print("Obteniendo parametros de camara...")

delta_camara = [] # hay que calcular --> depende de la posicion de la camara

origin_camara = [] 

timer = 0

while timer < 4:

        ret, img = cap.read()
        if ret == False: break

        delta_camara, origin_camara = get_delta_cam(cmtx, dist, img)
        # delta_camara = [149, -142]
        timer += 1


# PASO 1: Calcular Deltas ---------------------------------

delta_robot = [77, 77] # siempre es igual --> no depende de la camara

origin_robot = [469.10, -462.85] 

tray_robot = [371.36, 166]

fx, fy = [(delta_robot[0]/delta_camara[0]),(delta_robot[1]/delta_camara[1])] # factor de conversion entre las escalas

print("factor de conversion x = ", fx)
print("factor de conversion y = ", fy)

print("coordenadas de origen = ", origin_camara)

# PASO 2: Encontrar piezas

timer = 0

while timer < 5:

        ret, img = cap.read()
        if ret == False: break

        print("Buscando piezas....")

        centers = get_centers(img, origin_camara)
        print(centers)

        timer += 1


# PASO 3: Transformacion de coordenadas

piece_center_camara = centers[0]

piece_center_robot = convert(origin_camara, origin_robot, [fx, fy], piece_center_camara)

print("coords robot: ", piece_center_robot)

# PASO 4: Movimiento de robot

# s.send(b"movel(p[0.465, -0.4606, 0.0155, 0, 3.14, 0], 0.1, 0.2)\n")

# time.sleep(5)

# MOVER A LA POSICION DE LA PIEZA

instruction ="movel(p["+ str(piece_center_robot[0]/1000)+", "+ str(piece_center_robot[1]/1000) +", 0.040, 0, 3.14, 0], 0.1, 0.2)\n"

s.send(str.encode(instruction))

time.sleep(5)

# BAJAR Y AGARRAR LA PIEZA

instruction ="movel(p["+ str(piece_center_robot[0]/1000)+", "+ str(piece_center_robot[1]/1000) +", -0.002, 0, 3.14, 0], 0.1, 0.2)\n"

s.send(str.encode(instruction))

time.sleep(5)

rob.send_program(str(robotiqgrip.gripper_action(255)))

# MOVER ARRIBA

instruction ="movel(p["+ str(piece_center_robot[0]/1000)+", "+ str(piece_center_robot[1]/1000) +", 0.1, 0, 3.14, 0], 0.1, 0.2)\n"

s.send(str.encode(instruction))

time.sleep(5)

# MOVER A LA BANDEJA

instruction ="movel(p["+ str(tray_robot[0]/1000)+", "+ str(tray_robot[1]/1000) +", 0.1, 0, 3.14, 0], 0.1, 0.2)\n"

s.send(str.encode(instruction))

time.sleep(5)

# BAJA LA PIEZA A LA BANDEJA Y LA SUELTA

instruction ="movel(p["+ str(tray_robot[0]/1000)+", "+ str(tray_robot[1]/1000) +", -0.003, 0, 3.14, 0], 0.1, 0.2)\n"

s.send(str.encode(instruction))

time.sleep(5)

rob.send_program(str(robotiqgrip.gripper_action(value=165)))

# SUBE

instruction ="movel(p["+ str(tray_robot[0]/1000)+", "+ str(tray_robot[1]/1000) +", 0.1, 0, 3.14, 0], 0.1, 0.2)\n"

s.send(str.encode(instruction))

time.sleep(5)

print("DONE :)")

# s.send(b"movel(p[0.242, -0.176, 0.08, 0, 3.14, 0], 0.1, 0.1)\n")

time.sleep(2)








