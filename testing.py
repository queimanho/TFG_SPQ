'''
Módulo de prueba para validar los algoritmos y comprobar su funcionamiento
'''

from funciones import *
from preprocesado import*
from math import *
# from scipy.optimize import fsolve
# from scipy.signal import find_peaks, medfilt
import numpy as np
import sensormotion as sm
from pylab import *
from PPG import *
from scipy.fftpack import fft, fftfreq
from scipy import arange
# from matplotlib import*
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

#Sacamos los datos del acelerómetro de los ficheros
# Quitar el comentario de la línea 21 (justo debajo)
# separarDatosV2("file",'idPaciente') #file es el fichero y idPaciente el nombre del paciente
filePrueba = 'PRUEBA_CUVI3.txt' # == idPaciente.txt
minuto = 6
distPasillo = 8
fileName=['TESTS/vector_acelX_'+filePrueba,'TESTS/vector_acelY_'+filePrueba,'TESTS/vector_acelZ_'+filePrueba]
datos = []
for name in fileName:
    try:
        fichero = open(name)
        contenido = fichero.read()
        fichero.close()
    except:
        print("FA WATCH", "El fichero que has seleccionado no exste o no está en el directorio raíz, inténtalo de nuevo")

    datos.append(contenido.split())

#Sacamos los datos del giroscopio de los ficheros
fileName2=['TESTS/vector_giroscopioX_'+filePrueba,'TESTS/vector_giroscopioY_'+filePrueba,'TESTS/vector_giroscopioZ_'+filePrueba]
datosG = []
for name in fileName2:
    try:
        fichero = open(name)
        contenido = fichero.read()
        fichero.close()
    except:
        print("FA WATCH", "El fichero que has seleccionado no exste o no está en el directorio raíz, inténtalo de nuevo")
    datosG.append(contenido.split())

#Sacamos los datos de la señal PPG del fichero
datosPPG = []
name = 'TESTS/vector_PPG_original_'+filePrueba
try:
    fichero = open(name)
    contenido = fichero.read()
    fichero.close
except:
    print("FA WATCH", "Holi, El fichero que has seleccionado no exste o no está en el directorio raíz, inténtalo de nuevo")

datosPPG = contenido.split()
PPG = []
for i in range(len(datosPPG)):
    PPG.append(float(datosPPG[i]))
PPG_n=[]
maximo = max(PPG)
minimo = min(PPG)
for i in range(len(PPG)):
    PPG_n.append((PPG[i]-minimo)/(maximo-minimo))

listaG = []
AxDATA = []
AyDATA = []
AzDATA = []
GxDATA = []
GyDATA = []
GzDATA = []
giroX = []
giroY = []
giroZ = []
FSCg = 1000
for i in range(len(datos[0])):
    g = sqrt(int(datos[0][i])**2+int(datos[1][i])**2+int(datos[2][i])**2)
    GxDATA.append(int(datosG[0][i])*FSCg*0.01/2**15) # Guardamos los datos como variación del ángulo
    GyDATA.append(int(datosG[1][i])*FSCg*0.01/2**15) # en grados
    GzDATA.append(int(datosG[2][i])*FSCg*0.01/2**15)
    AxDATA.append(int(datos[0][i]))
    AyDATA.append(int(datos[1][i]))
    AzDATA.append(int(datos[2][i]))
    giroX.append(int(datosG[0][i]))
    giroY.append(int(datosG[1][i]))
    giroZ.append(int(datosG[2][i]))
    if (giroX[i] >= 0):

        giroX[i] = giroX[i] / float(32768)
    else:
        giroX[i] = giroX[i] / float(-32768)

    if (giroY[i] >= 0):

        giroY[i] = giroY[i] / float(32768)
    else:
        giroY[i] = giroY[i] / float(-32768)

    if (giroZ[i] >= 0):

        giroZ[i] = giroZ[i] / float(32768)
    else:
        giroZ[i] = giroZ[i] / float(-32768)

threshold = 170
ploting = False #Poner a True si se desea visualizar los resultados
start, v_t, v_v, distancia, last_distancia, vect_v,PLOT_LIST = analisis_movimiento(minuto,AxDATA,AyDATA,AzDATA,GxDATA,GyDATA,GzDATA,distPasillo,ploting,threshold)

ploting = True
for paciente in start:
    fin = paciente*100 + minuto*60*100
    card,resp, originalPPG = preprocesadoPPG(PPG_n[paciente*100:fin])
    t_HR, v_HR = calcula_HR(card,5,ploting)
    t_RR, v_RR = calcula_RR(resp,10,ploting)

if False: #Poner a True si se desea representar los resultados
    representResults(v_t,v_v,vect_v,t_HR, v_HR, t_RR, v_RR, distancia, last_distancia," Paciente 00012 2021.05.28-10.26.42",PLOT_LIST)
