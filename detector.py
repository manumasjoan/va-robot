from operator import invert
from turtle import distance
import cv2 as cv
import numpy as np
import sys
import math


def read_camera_parameters(filepath = 'camera_parameters/intrinsic.dat'):

    inf = open(filepath, 'r')

    cmtx = []
    dist = []

    #ignore first line
    line = inf.readline()
    for _ in range(3):
        line = inf.readline().split()
        line = [float(en) for en in line]
        cmtx.append(line)

    #ignore line that says "distortion"
    line = inf.readline()
    line = inf.readline().split()
    line = [float(en) for en in line]
    dist.append(line)

    #cmtx = camera matrix, dist = distortion parameters
    return np.array(cmtx), np.array(dist)

def get_qr_coords(cmtx, dist, points):

    #Selected coordinate points for each corner of QR code.
    qr_edges = np.array([[0,1,0],
                         [1,1,0],
                         [1,0,0],
                         [0,0,0]], dtype = 'float32').reshape((4,1,3))

    #determine the orientation of QR code coordinate system with respect to camera coorindate system.
    ret, rvec, tvec = cv.solvePnP(qr_edges, points, cmtx, dist)

    #Define unit xyz axes. These are then projected to camera view using the rotation matrix and translation vector.
    unitv_points = np.array([[0,0,0], [1,0,0], [0,1,0], [0,0,1]], dtype = 'float32').reshape((4,1,3))
    if ret:
        points, jac = cv.projectPoints(unitv_points, rvec, tvec, cmtx, dist)
        return points, rvec, tvec

    #return empty arrays if rotation and translation values not found
    else: return [], [], []

def show_axes(cmtx, dist, img):
    qr = cv.QRCodeDetector()

    #ret_qr, points = qr.detect(img)
    ret_qr, points = qr.detect(cv.bitwise_not(img))

    if ret_qr:
        #axis_points devuelve las coordenadas de las 4 puntas del QR
        # #rvec vector de rotacion
        #tvec vector de traslacion 
        axis_points, rvec, tvec = get_qr_coords(cmtx, dist, points)


        #BGR color format
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0,0,0)]

        #check axes points are projected to camera view.
        if len(axis_points) > 0:
            axis_points = axis_points.reshape((4,2))

            origin = (int(axis_points[0][0]),int(axis_points[0][1]) )
            #cv.line(img, origin, (int(axis_points[1][0]),int(axis_points[1][1]) ), (255,255,0), 5)
            #print("distance1"+ str(distance))
            #print("distance2"+ str(distance2))

            show_centers(img,origin)

            # for p, c in zip(axis_points[1:], colors[:3]):
            #     #este p son los puntos 
            #     p = (int(p[0]), int(p[1]))
                
            #     #Sometimes qr detector will make a mistake and projected point will overflow integer value. We skip these cases. 
            #     if origin[0] > 5*img.shape[1] or origin[1] > 5*img.shape[1]:break
            #     if p[0] > 5*img.shape[1] or p[1] > 5*img.shape[1]:break

            #     cv.line(img, origin, p, c, 5)
def get_binary_image(image, value):
    gray_image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    ret, threshold = cv.threshold(gray_image, value, 255, cv.THRESH_BINARY_INV)
    return threshold
    
def get_denoised_image(binary):
    structuring_element = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    morph_open = cv.morphologyEx(binary, cv.MORPH_OPEN, structuring_element)
    morph_close = cv.morphologyEx(binary, cv.MORPH_CLOSE, structuring_element)
    return morph_close

def get_biggest_contour(contours):
    max_cnt = contours[1]
    for cnt in contours:
        # print(cnt)
        if cv.contourArea(cnt) > cv.contourArea(max_cnt):
            max_cnt = cnt
    return max_cnt

def show_centers(img, origin):

    # #Aplico threshold a la imagen
    # gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    # _,th= cv.threshold(gray,150,255, cv.THRESH_BINARY)

    # #Aplico operaciones morfologicas
    # kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (4,4))
    # opening = cv.morphologyEx(th, cv.MORPH_OPEN, kernel)
    # closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)

     #original image
    #ret, original_image = webcam.read()
    # cv.imshow('Original', original_image)

    #binary image
    # binary_value = cv.getTrackbarPos('Binary_Trackbar', 'Binary')
    binary_image = get_binary_image(img, 200)
    cv.imshow('Binary', binary_image)

    #denoised image
    denoised_image = get_denoised_image(binary_image)
    cv.imshow('Denoised', denoised_image)

    #contours
    _, contours, _ = cv.findContours(denoised_image, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    #Busco los contornos
   # _, contornos, _ = cv.findContours(closing, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    #filtro los contornos
    contornos_filtrados = [] #inicializo la variable de contornos filtrados
    for c in contours:
        area = cv.contourArea(c)
        if area > 500 and area < 2000:
            
            #en un vector voy guardando los contornos, el append lo que hace es ir agregando el ultimo contorno y lo escribe
            contornos_filtrados.append(c)
            pto = c
            M = cv.moments(pto)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            if(math.dist(origin,[cX,cY])>300):
                print("punto   ",cX,cY)
                print("origen   ",origin)

                cv.drawContours(image=img, contours=[c], contourIdx=-1, color=(0, 255, 0), thickness=3)
                cv.line(img, origin, [cX,cY], (0, 255, 0), 5)

   
    #ejemplo con un solo punto 
    # if(len(contornos_filtrados)>0):
    #     pto = contornos_filtrados[0]
    #     M = cv.moments(pto)
    #     cX = int(M["m10"] / M["m00"])
    #     cY = int(M["m01"] / M["m00"])
    #     cv.line(img, origin, [cX,cY], (0, 255, 0), 5)
    #     print("------")
    #     print("distancia en x:"+ str(cX-origin[0]))
    #     print("distancia en Y:"+ str(cY-origin[1]))
    #     print("------")

        #cv.circle(img, (cX, cY), 1, (0, 255, 0), 5)


    #en un vector voy guardando los centroides, el append lo que hace es ir guardando los valores y escribirlos al final
    # Coordenadas_X = []
    # Coordenadas_Y = []
    # for d in contornos_filtrados:
    #         M = cv.moments(d)
    #         cX = int(M["m10"] / M["m00"])
    #         cY = int(M["m01"] / M["m00"])
    #         cv.circle(img, (cX, cY), 1, (0, 255, 0), 5)
    #         Coordenadas_X.append(cX)
    #         Coordenadas_Y.append(cY)

        cv.imshow('Binary', cv.bitwise_not(img))


def execute(cmtx, dist, in_source):
    cap = cv.VideoCapture(in_source)

    qr = cv.QRCodeDetector()

    while True:
        ret, img = cap.read()
        if ret == False: break

        show_axes(cmtx, dist, img)
        #show_centers(img)

        cv.imshow('frame', img)

        k = cv.waitKey(20)
        if k == 27: break #27 is ESC key.

    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':

    #read camera intrinsic parameters.
    cmtx, dist = read_camera_parameters()

    input_source = 'media/test.mp4'
    if len(sys.argv) > 1:
        input_source = int(sys.argv[1])

    execute(cmtx, dist, input_source)
