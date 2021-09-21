from __future__ import print_function, division
import sys
import tkinter
from tkinter import *
import tkinter.ttk as Ttk
import tkinter.messagebox
import time
import serial
import scipy
import pylab as pl
import scipy.io
import scipy.signal
import numpy as np
import peakutils
from peakutils.plot import plot as pplot
from scipy.io import loadmat
import sensormotion as sm
from math import sqrt
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import codecs
import pandas as pd
import openpyxl
import os.path

##################################################################
#
#       FUNCIONES PARA LA DESCARGA Y LA GENERACIÓN DE FICHEROS
#
##################################################################

def scan(num_ports=20):
 """
 Función que busca puertos serie disponibles

 Parámetros :
  num_ports: 'int', optional
   Numero de puertos a escanear
 Return :
  dispositivos_serie: '[List[Tuple[int, str]]'
   Lista con todos los puertos encontrados. Cada elemento de la lista es una tupla con el numero y el nombre del puerto
  hay_puerto: 'bool'
   Indica si hay algún puerto disponible
 """

 hay_puerto = False
 dispositivos_serie = []

 for i in range(num_ports):

  try:
   s = serial.Serial("COM%s" % i)

   dispositivos_serie.append((i, s.portstr))
   hay_puerto = True

   s.close()

  except:
   pass

 return (dispositivos_serie, hay_puerto)


def Aceptar_descarga(puerto, nombreFichero):
 """
 Función de aviso finalizacion descarga o error durante la descarga

 Parámetros :
  puerto: 'str'
   Nombre del puerto que se utiliza para la descarga
  nombreFichero: 'str'
   Nombre del fichero que se va a crear
 """

 if (data_download(puerto, nombreFichero)):
   tkinter.messagebox.showinfo("Info", "Fichero descargado correctamente!")
 else:
   tkinter.messagebox.showinfo("Info", "Ha ocurrido un error.\n Desconecte la pulsera e inténtelo de nuevo.\nAsegúrese antes de que el puerto COM es el correcto")


def data_download(puerto, nombreFichero):
 """
 Función para descargar los datos de la pulsera y guardarlos en un fichero

 Parámetros :
  puerto: 'str'
   Nombre del puerto que se utiliza para la descarga
  nombreFichero: 'str'
   Nombre del fichero que se va a crear
 Return : 'bool'
  1 si la descarga se realiza correctamente
  0 si se produce un error en la descarga
 """

 time.sleep(15)
 try:
  s = serial.Serial('%s' %puerto, 4000000)#windows
  #s = serial.Serial('/dev/ttyACM0', 9600)#ubuntu
 except:
  return 0
 s.timeout=1
 s.write('start'.encode())
 s.flush()
 list=[]
 a_escribir=[]
 i=0
 contador=0
 while(s.in_waiting==0):
  contador+=1
 while(1):
  try:
   contador=0
   while(s.in_waiting==0):
    contador+=1
    if (contador>1000000):
     break
   if(s.in_waiting>0):
    for i in range (0,16,1):
      data = s.read()
      list.append(codecs.encode(data,'hex_codec'))
    a_escribir.append(list)
    list=[]
   else:
    break
  except:
   return 0
   #break;
 grabartxt(a_escribir,nombreFichero)
 s.close()
 return 1


def grabartxt(filas, name):
 """
 Función para guardar datos en un fichero

 Parámetros :
  filas: 'List[List[bytes]]'
   Datos a guardar
  name: 'str'
   Nombre del fichero
 """
 archi=open(name,'ab') #Se crea el archivo si no existe. Si existe se abre en modo escritura, manteniendo el contenido actual y añadiendo los datos al final del archivo
 for j in range(0,len(filas),1):
  for h in range (0, len(filas[j]),1):
   archi.write(filas[j][h])
   archi.write(' '.encode())
  archi.write('\n'.encode())
 archi.close()

def grabartxt_senhales(datos, nombreFichero):
 """
 Función para guardar datos en un fichero sobreescribiéndolo

 Parámetros :
  datos: 'List[Any]'
   Datos a guardar
  nombreFichero: 'str'
   Nombre del fichero
 """
 archi=open(nombreFichero,'w') #Se crea el archivo si no existe. Si existe se sobreescribe
 for j in range(0,len(datos),1):
  archi.write(str(datos[j]))
  archi.write(' ')
  archi.write('\n')
 archi.close()

#print(scan())
#Aceptar_descarga('COM3','pruebaSERIAL.txt')
data_download('COM3','TESTING/pruebaCASTRO3.txt')
#C:/Users/Usuario/Desktop/TFG/TFG_Maria/Codigo/TESTING
