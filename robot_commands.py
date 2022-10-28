from urx import robotiq_two_finger_gripper
import time
import socket
from typing import List
import urx
import cv2 as cv

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



# # Conexion con la camara
# print("Conectando con la camara")
# cap = cv.VideoCapture(0, cv.CAP_DSHOW)
# print(cap.isOpened())
# tree = trainingModel.train_model()
# cv.namedWindow('Parameters')
# print("Conectado con la camara")


# # posiciones cargadas
# posiciones = {  "0" : b"movej([-3.2189834753619593, -1.7424808941283167, 1.4784472624408167, -1.4887936872294922, -1.6161873976336878, -0.18661243120302373])\n",
#                 "2" : b"movej([-3.956921402608053, -1.7561424236693324, 2.4691947142230433, -2.2455297909178675, -1.5485871473895472, -0.8221257368670862])\n", 
#                 "1" : b"movej([-3.5026300589190880, -1.0280173772624512, 1.5461886564837855, -2.1145335636534632, -1.6231797377215784, -0.32508117357362920])\n",
#                 "3" : b"movej([-4.226582352315084, -1.4589700521281739, 2.188515011464254, -2.300427099267477, -1.5482633749591272, -1.1085799376117151])\n",
#                 "4" : b"movej([-3.790581528340475, -0.9107036413005372, 1.3540595213519495, -2.0169321499266566, -1.540293041859762, -0.6730135122882288])\n",
#                 "5" : b"movej([-3.8255489508258265, -1.4982145589641114, 1.3549464384662073, -1.4924248021892090, -1.6503947416888636, -0.75999957719911750])\n" }


# coordenadas_camara = {  "3" : (350, 310),
#                         "4" : (15 , 295),
#                         "2" : (365, 135),
#                         "1" : (30 , 110)}


# movimiento de robot

# def move(p) :
#     s.send( posiciones[p])
#     time.sleep(2)


# # deteccion de posiciones ocupadas
# def detect_objects (): 

#     timer = 0

#     while timer < 2:
#         _, frame = cap.read()
#         frame = cv.flip(frame, 1)
#         area_thresh = 300
#         binary_thresh = 100
#         color_img , binary_img, coords = testingModel.load_and_test(tree, frame, area_thresh, binary_thresh )
#         timer += 1
#         print("Se encontraron objetos en las siguientes coordenadas: " + str(coords))

#     return coords

# # verifies if position is occupied

# def is_position_occupied(p) :
#     object_coordinates = detect_objects()
#     offset = 80
#     time.sleep(4)
#     x, y = coordenadas_camara.get(str(p))

#     for c in object_coordinates:
#         if (x < c[0] < x+offset and y < c[1] < y+offset) : return True

#     return False

# MAIN

# Inicio del proceso

print("Bienvenido! Inicializando el proceso...")
rob.send_program(str(robotiqgrip.open_gripper()))
time.sleep(2)



# print("coordenadas del robot:   " + rob.getl())
# s.send(b"movej([-3.8255489508258265, -1.4982145589641114, 1.3549464384662073, -1.4924248021892090, -1.6503947416888636, -0.75999957719911750])\n")

# time.sleep(5)
# s.send(b"movel([0.46500590481655085, -0.46058388788163435, 0.09839999194988708, 0, -3.140227480258244, 0])")
s.send(b"movel(p[0.465, -0.4606, 0.09, 0, 3.14, 0], 0.05, 0.05)\n")
# s.send(b"movel([0, 0, 0,0,0, 0], 1.2, 0.25,0)\n")

time.sleep(5)
# while True:


#     # ELEGIR POSICION DE PARTIDA

#     while True :

       
#         print("Elija de que posicion agarrar un objeto. Ingrese un numero entre [1] y [4]")
#         p_partida = input()
#         if is_position_occupied(p_partida) :
#             move("5")
#             move(p_partida)
#             print("Cerrando gripper")
#             rob.send_program(str(robotiqgrip.close_gripper()))
#             time.sleep(2)
#             move("5")
#             move("0")
#             time.sleep(2)
#             break
#         print("No hay un objeto en esta posicion, elija otra.")

#     while True :

#         print("Elija en que posicion dejar el objeto. Ingrese un numero entre [1] y [4]")
#         p_destino = input()
#         if not is_position_occupied(p_destino) :
#             move("5")
#             move(p_destino)
#             print("Abriendo gripper")
#             rob.send_program(str(robotiqgrip.open_gripper()))
#             time.sleep(2)
#             move("5")
#             move("0")
#             time.sleep(2)
#             break
#         print("Esta posicion ya esta ocupada, elija otra.")

#     print("Ingrese [1] para continuar el proceso, o cualquier otra tecla para finalizarlo:")
#     c = input() 
#     if(c != "1"):
#         break
    

print("Proceso finalizado")

