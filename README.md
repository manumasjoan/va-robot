# Requerimientos 
Previo a comenzar con la instalación, se deberían cumplir los siguientes requerimientos:
 * Tener Python 3.8 y PIP3 instalados.
 * Una cámara web que se pueda conectar a la computadora.
 * Cobot UR5e.
# Pasos
Una vez cumplidos los requerimientos, se puede continuar con la instalación:
## Instalación 
 1. Clonar el repositorio.
 2. __Instalar dependencias__: en consola, entrar a la carpeta correspondiente al proyecto y utilizar el comando `pip3 install` para las siguientes dependencias:
  * cv2
  * numpy
  * urx
 3. __Corrección de dependencia del gripper__: hay un error en la dependencia que impide el funcionamiento correcto del programa. Para corregirla:
  * Entrar al archivo robotiq_two_finger_gripper.py
  * Dentro del método _get_new_urscript(self) eliminar las dos siguientes líneas:
   - urscript._set_robot_activate()
   - urscript._set_gripper_activate()
## Configuración del robot
 1. Prender el robot, activar el gripper y dejarlo en modo remoto. 
 2. Revisar que el robot esté conectado al router.
 3. Revisar la configuración del robot. Debería cumplir las siguientes condiciones:
  - IP: 192.168.0.16
  - Subred: 255.255.255.0
  - Puerta de enlace: 192.168.0.20
  - DNS1: 8.8.8.8
  - DNS2: 8.8.4.4
 4. Conectar la computadora con la red wifi del Robot.
  * __Nombre de red__: Brazo Robot UR5
  * __Contraseña__: brazorobotur5
 5. Editar la configuración IP de la computadora para esa red. 
  * Para computadoras Windows:
   1. Entrar a Configuracion → Red & Wifi 
   2. Administrar redes conocidas → Seleccionar la red del robot
   3. Propiedades → Asignar IP → Editar
   4. Seleccionar configuración Manual y en IPv4 completar con los datos:
    - IP address: mismo que el robot excepto por último número
    - Subnet prefix length: 24
    - IP gateway: puerta de enlace que le pusimos al robot.
    - DNS servers: iguales al robot.
   5. Guardar cambios.
  * Para computadoras Mac:
   1. Entrar a Network Preferences 
   2. Advanced 
   3. Entrar a la tab de TCP/IP
   4. Cambiar la configuración de IPv4 a manual 
   5. Cambiar la dirección de IPv4 a la misma que el robot salvo por los últimos dos dígitos 
   6. Aplicar los cambios 
 6. Correr `ping 192.168.0.16` en la terminal para verificar que la conexión haya sido exitosa.
## Set up del ambiente
 1.Ubicar QR en la esquina de la visión de la cámara de la siguiente manera.
 2. Asegurar que la superficie donde se esta detectando sea negro. Esto se puede hacer pegando una cartulina o tela si la mesa de trabajo es blanca.
 3. Ubicar la bandeja como indica la imagen abajo. Se pueden cambiar las posiciones de bandeja en el código si se quisiera ubicar las piezas en otro lugar.
 4. Colocar el ‘techo’ sobre el QR, sin tapar la visión de la cámara:
## Ejecución
Una vez que esté todo preparado, se pueden correr los siguientes archivos:
 - __gripper_testing.py__ : testear la conexión del robot y el gripper 
 - __detector.py__ : muestra los contornos de las piezas y dibuja una recta desde el origen hasta el centro de cada uno de estos contornos. Sirve para revisar  que las piezas y el QR están siendo detectados correctamente.
 - __coords_conversion.py__ : Corre el programa de detección y  recolección de piezas. En caso de querer parar al robot en cualquier momento de la ejecución presionar el botón rojo que se encuentra en la  tableta de control del robot.
