from math import *
from scipy.optimize import fsolve
from scipy.signal import find_peaks
import numpy as np
import sensormotion as sm
from pylab import *
from tkinter import*
# import matplotlib
from matplotlib import*
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

def media(lista):
    """
    Función que calcula la media de una lista

    Parámetros :
    lista: 'list[float]'
    conjunto de datos para caluclar la media
    Returns : 'float'
    media de los datos
    """
    s = 0
    for elemento in lista:
        s += elemento
    if len(lista)>0:
        return s / float(len(lista))
    else:
        return 0

def varianza(lista):
    """
    Función que calcula la variaza de una lista

    Parámetros :
    lista: 'list[float]'
    conjunto de datos para caluclar la varianza
    Returns : 'float'
    varianza de los datos
    """
    s = 0
    m = media(lista)
    var = []
    for elemento in lista:
        s = (elemento - m) ** 2
        var.append(s)
    return var

def desviacion_tipica(lista):
    """
    Función que calcula la desvación típica de una lista

    Parámetros :
    lista: 'list[float]'
    conjunto de datos para caluclar la desvación típica
    Returns : 'list[float]'
    desviación típica de los datos
    """
    desv = []
    vari = varianza(lista)
    for i in range(len(lista)):
        desv.append(sqrt(vari[i]))

    return desv

def getPacientes(DATAGX):
    '''
    Función que determina el instante de inicio de las pruebas, así como el número de estas.
    
    Parámetro:
    DATAGX: 'list[float]'
        Valores del giroscopio eje X
    
    Return:
    comienzo_paciente: 'list[int]'
        Instantes de tiempo donde se ha detectado el inicio de un paciente
    '''
    absGX = []
    tGx = []
    #Adaptamos los valores de la señal Gx de 0 al FSR(1000º) y creamos un vector tiempo
    for i in range(len(DATAGX)):
        absGX.append(abs(DATAGX[i]))
        tGx.append(i*0.01)
    
    #Detectamos los picos mayores de 2
    minimo = 0.3
    distancia = 20
    peak_times, peak_values = sm.peak.find_peaks(time=tGx, signal=absGX,
                                            peak_type='peak',
                                            min_val=minimo, min_dist=distancia,
                                            plot=False)
    pacientes = 0
    comienzo_paciente = []
    picos = 0
    nPicos = len(peak_times)
    for i in range(len(peak_times)):
        if ((peak_times[i] - peak_times[i-1]) < 1) or i == 0:
            picos += 1
        elif picos > 4:
            pacientes += 1
            comienzo_paciente.append(int(round(peak_times[i-1]) + 1.5))
            picos = 0
        elif ((peak_times[i] - peak_times[i-1]) > 1) and picos != 0:
            picos = 0

        if picos > 4 and i == nPicos-1:
            picos = 0
            pacientes += 1
            comienzo_paciente.append(int(round(peak_times[i]) + 1.5))

    return comienzo_paciente

def getCambios(lista,start,trig,min):
    '''
    Función que detecta los cambios de sentido dada una lista que indica el ángulo YAW

    Parámetros:
    lista: 'list[float]'
        lista que indica el valor instantáneo del ángulo YAW del paciente
    start: 'int'
        valor que indica el inicio de la prueba en segundos
    trig: 'int'
        valor en grados, a partir del cual marcamos un cambio de sentido (del orden de 165º)
    min: 'int'
        Minutos que dura la prueba
    
    Return:
    cambio: 'list[int]'
        lista que guarda el instante de tiempo en muestras donde se produce el fin de un cambio de sentido
    cambioValue 'list[float]'
        Lista donde se guardan los valores de la señal 'lista' para plotear los cambios de sentido
    sTcambio: 'list[int]'
        lista que guarda el instante de tiempo en muestras donde se produce el inicio de un cambio de sentido
    sTcambioValue 'list[float]'
        Lista donde se guardan los valores de la señal 'lista' para plotear los cambios de sentido
    '''

    # ref = lista[start*100]
    UP1 = lista[start*100]
    idUP1 = start*100
    idDOWN1 = start*100
    DOWN1 = lista[start*100]
    # ref2 = lista[start*100+min*60*100]
    cambio = []
    cambioValue = []
    stCambio = []
    stCambioValue = []
    cambio2 = []
    listaCambios = []
    fin = start*100+min*60*100
    UP2 = lista[fin]
    DOWN2 = lista[fin]
    idDOWN2 = fin
    idUP2 = fin

    #Guardamos el final de cada cambio de sentido (NUEVO ALGORITMO)
    for i in range(start*100,fin-100):
        if len(cambio) != 0:
            if i >= cambio[-1]:
                if lista[i] >= UP1:
                    UP1 = lista[i]
                    idUP1 = i
                if lista[i] <= DOWN1:
                    DOWN1 = lista[i]
                    idDOWN1 = i
                if lista[i] > (trig+DOWN1) or lista[i]<(UP1-trig):
                    cambio.append(i+100)
                    cambioValue.append(lista[i+100])
                    UP1 = lista[i+100]
                    DOWN1 = lista[i+100]
                    idDOWN1 = i+100
                    idUP1 = i+100
        elif len(cambio) == 0:
            if lista[i] >= UP1:
                UP1 = lista[i]
                idUP1 = i
            if lista[i] <= DOWN1:
                DOWN1 = lista[i]
                idDOWN1 = i
            if lista[i] > (trig+DOWN1) or lista[i]<(UP1-trig):
                cambio.append(i+100)
                cambioValue.append(lista[i+100])
                UP1 = lista[i+100]
                DOWN1 = lista[i+100]
                idDOWN1 = i+100
                idUP1 = i+100

    #Guardamos el inicio de cada cambio de sentido
    for i in range(fin-100,start*100,-1):
        if len(stCambio) != 0:
            if i <= stCambio[-1]:
                if lista[i] >= UP2:
                    UP2 = lista[i]
                    idUP2 = i
                if lista[i] <= DOWN2:
                    DOWN2 = lista[i]
                    idDOWN2 = i
                if lista[i] > (trig+DOWN2) or lista[i]<(UP2-trig):
                    stCambio.append(i-100)
                    stCambioValue.append(lista[i-100])
                    UP2 = lista[i-100]
                    DOWN2 = lista[i-100]
                    idDOWN2 = i-100
                    idUP2 = i-100 
        elif len(stCambio) == 0:
            if lista[i] >= UP2:
                UP2 = lista[i]
                idUP2 = i
            if lista[i] <= DOWN2:
                DOWN2 = lista[i]
                idDOWN2 = i
            if lista[i] > (trig+DOWN2) or lista[i]<(UP2-trig):
                stCambio.append(i-100)
                stCambioValue.append(lista[i-100])
                UP2 = lista[i-100]
                DOWN2 = lista[i-100]
                idDOWN2 = i-100
                idUP2 = i-100

    #Guardamos en una lista ordendada, el inicio de cada cambio de giro
    for i in reversed(stCambio):
        cambio2.append(i)
    
    if len(cambio)>=len(cambio2):
        rango = len(cambio2)
    else:
        rango = len(cambio)
    #Guardamos en una lista [fin, inicio] de cada giro.
    CAMBIOS = []
    for i in range(rango):
        listaCambios.append([cambio[i]-start*100,cambio2[i]-start*100])
        CAMBIOS.append([cambio[i],cambio2[i]])
    
    
    return cambio, cambioValue, stCambio, stCambioValue, CAMBIOS, listaCambios

def calcula_pasos(acel,timeList):
    '''
    Función que calcula los pasos durante los tramos fijos
    '''
    minimo = 0.60
    distancia = 40
    peak_times, peak_values = sm.peak.find_peaks(time=timeList,signal=acel,
                                                     peak_type='peak',
                                                     min_val=minimo,min_dist=distancia, plot=False)
    pasos = len(peak_times)
    
    return pasos,peak_times,peak_values

def calcula_pasos2(acel,timeList,trig):
    '''
    Función que calcula los pasos durante los giros
    '''
    minimo = 0.80
    distancia = 40
    peak_times2 = []
    peak_values2 = []
    
    peak_times, peak_values = sm.peak.find_peaks(time=timeList,signal=acel,
                                                     peak_type='peak',
                                                     min_val=minimo,min_dist=distancia, plot=False)
    pasos = len(peak_times)
    for i in range(len(peak_times)):
        if peak_values[i] >= trig*0.97:
            peak_times2.append(peak_times[i])
            peak_values2.append(peak_values[i])
    pasos = len(peak_times2)
    
    return pasos,peak_times2,peak_values2

def actualizaPasos(listaPasos, desv):
    '''
    Función que filtra los tramos cuya medida de los pasos se desvía de la media en un valor mayor a 'desv'
    '''
    aux = listaPasos
    aux.pop(-1) #Eliminamos el último elemento de la lista (último tramo incompleto)
    desv = desviacion_tipica(aux)
    # print(desv)
    tramos = len(aux)
    popList = []
    for i in range(len(aux)):
        if desv[i]>desv:
            popList.append(i)
            tramos -= 1
    for i in reversed(popList):
        aux.pop(i)
    mediaSt = media(aux)

    return aux, mediaSt

def actualizaTramos(pt,pg,cambios,start):
    '''
    Función para unir los pasos dados en cada giro con los pasos del tramo anterior
    
    '''
    start = start*100
    pasitos = []
    largo = []
    for i,tramo in enumerate(pt):
        #Primero añadimos los pasos dados en el giro anterior que se correspondan al tramo i
        if i>0 and i<len(pt)-1:
            media_giro2 = (cambios[i-1][0]-start+cambios[i-1][1]-start)/2
            for pasoG in pg[i-1]:
                if pasoG>media_giro2:
                    largo.append(pasoG)
        #Segundo se añaden los pasos del tramo recto
        for paso in tramo:
            largo.append(paso)
        #Tercero y último, se añaden los pasos en el giro al final del tramo i que le correspondan
        if i<len(pt)-1:
            media_giro = (cambios[i][0]-start+cambios[i][1]-start)/2
            for pasoG in pg[i]:
                if pasoG<=media_giro:
                    largo.append(pasoG)
        pasitos.append(largo)
        largo = []
    # print(pasitos)    
    return pasitos

def getPasos(acc, start, minutos, dist, cambios):
    '''
    Función que determina los pasos y la distancia total recorrida
    
    Parámetros:
    acc: 'list[float]'
        lista que contiene los datos del acelerómetro del eje Y
    start: 'int'
        instante de tiempo donde inicia la prueba
    dist: 'int'
        distancia fija del pasillo
    cambios: 'list[int][float]'
        lista que contiene los instantes de tiempo donde se han procucido cambios de sentido
        Son dos listias [0][i] y [1][i], la 0 muestra el fin de cada giro y la 1, el inicio
    '''
    # print(cambios)
    radio = 0.5 #Radio de giro, aprox medio metro.
    fin = minutos*60
    t_total = []
    values_total = []
    steps = []
    totalSteps = 0
    timeList = []
    mediaPaso = []
    for i in range(len(acc)):
        timeList.append(i)
    b, a = sm.signal.build_filter(frequency=3,
                            sample_rate=100,
                            filter_type='low',
                            filter_order=4)
    acc_filtered = sm.signal.filter_signal(b,a,signal = acc)

    #Primer tramo
    acel = acc_filtered[0:cambios[0][1]-start*100]
    nPasos,t_step,values_step = calcula_pasos(acel,timeList[0:cambios[0][1]-start*100])
    mediaPaso.append(media(values_step))
    t_total.append(t_step)
    values_total.append(values_step)
    steps.append(nPasos)
    totalSteps += nPasos
    
    #Tramos sin contar primero y último.
    for i in range(len(cambios)-1):
        a = cambios[i][0]-start*100
        b = cambios[i+1][1]-start*100
        # print(a,b)
        acel = acc_filtered[a:b]
        if a<=b:
            nPasos,t_step,values_step = calcula_pasos(acel,timeList[a:b])
            mediaPaso.append(media(values_step))
            t_total.append(t_step)
            values_total.append(values_step)
            steps.append(nPasos)
            totalSteps += nPasos
        else:
            print("Hay un error en los giros")

    #Último tramo
    a = cambios[-1][0]-start*100
    b = len(acc)-1
    # print("FINALE",a,b)
    acel = acc_filtered[a:b]
    # print('Marca A')
    lastSteps, t_step, values_step = calcula_pasos(acel,timeList[a:b])
    mediaPaso.append(media(values_step))
    # print('Marca B')
    t_total.append(t_step)
    values_total.append(values_step)
    steps.append(lastSteps)

    acel = acc_filtered[start*100:start*100+minutos*60*100]
    
    listPasos = []
    listValuesPasos = []
    for i in range(len(t_total)):
        for j in range(len(t_total[i])):
            listPasos.append(t_total[i][j])
            listValuesPasos.append(values_total[i][j])
            
    
    listPasos2 = []
    listValuesPasos2 = []

    #Contar los pasos durante el giro
    pasosGiros = 0
    listPasoGiro = []
    t_total_giros = []
    listValuesGiro = []
    for i in range(len(cambios)):
        a = cambios[i][1]-start*100
        b = cambios[i][0]-start*100
        if a<b:
            acel = acc_filtered[a:b]
            nPasos,t_step,values_step = calcula_pasos2(acel,timeList[a:b],mediaPaso[i])
            pasosGiros += nPasos
            # plot(t_step,values_step,'go')
            listPasos2 += t_step
            t_total_giros.append(t_step)
            listValuesPasos2 += values_step 
            for j in range(len(t_step)):
                listPasoGiro.append(t_step[j])
                listValuesGiro.append(values_step[j])
                #Añadimos a la lista 'steps' que recoge el valor de los pasos dados en cada tramo, los datos del giro
                medio = (a+b)/2
                if t_step[j] < medio:
                    steps[i] = steps[i]+1
                elif t_step[j] > medio:
                    steps[i+1] = steps[i+1]+1

        else:
            print("Error en los pasos durante los giros")
    mediaGiro = pasosGiros/len(cambios)
    
    giro = pi*radio #Distancia recorrida en cada giro
    giroTOT = giro*len(cambios)
    mediaSteps = totalSteps/len(cambios) #Media de pasos por largo
    zancada = dist/mediaSteps #Media de la zancada
    
    #Algoritmos 3 y 4
    steps2 = steps.copy()
    stepsUpdated, mediaSteps = actualizaPasos(steps2,7)
    print('Steps Actualizados:\n'+str(stepsUpdated))

    lastSteps = steps[-1]

    if mediaSteps>0:
        zancada = dist/mediaSteps
    else:
        zancada = 0
        print("Revisar prueba, algo va mal con la cuenta de los pasos")
    distanciaTOT = len(cambios)*dist + zancada*lastSteps+giroTOT #Distancia total
    
    pasosFin = totalSteps + lastSteps

    listaDATA = [acc_filtered,t_total,values_total,listPasos2,listValuesPasos2]
    #pasos_lista = actualizaTramos(t_total,t_total_giros,cambios,start)

    return distanciaTOT,pasosFin,steps, listaDATA, t_total, lastSteps*zancada

def grado2uni(Gx):
    '''
    Función que convierte los datos del giroscopio de delta de grados a 0-1

    Parámetros:
    Gx: 'list[float]'
        datos del giroscopio como variación del ángulo en grados.
    
    returns:
    gx: 'list[float]'
        datos del giroscopio normalizados de 0 a 1.

    '''
    gx = []
    add = 0
    FSCg = 1000
    for i in range(len(Gx)):
        add = Gx[i]*2**15/(FSCg*0.01)
        if add >= 0:
            add = add/float(32768)
        else:
            add = add/float(-32768)
        gx.append(add)
    return gx

def deltaList(lista):
    '''
    Función que calcula la derivada de una lista dada como parámetro
    '''
    delta = [0]
    for i in range(len(lista)):
        if i == 0:
            delta[0] = lista[i]
        elif i > 0:
            inc = (delta[i-1]+(lista[i]))
            delta.append(inc)
    return delta

def media_movil(lista,time,x):
    '''
    Función que determina la media móvil de una señal

    Parámetros:
    lista: 'list[float]'
        señal input
    time: 'list[int]'
        lista de tiempos
    x: 'int'
        valor de muestras para la media
    Return:
    y: 'list[float]'
        lista con la media móvil
    t: 'list[int]'
        lista con los tiempos
    '''
    if x>(len(lista)-1):
        return print('Parámetro para la media demasiado grande')
    else:
        y = []
        t = []
        for i in range(len(lista)-x+1):
            a = i
            b = i+x-1
            c = i+int(x/2)
            y.append(media(lista[a:b]))
            t.append(time[c])
        return y,t

def getSpeed(lista, dist, vv, last, ploting):
    '''
    Función encargada de calcular la velocidad instantánea y de representar la evolución de la
    distancia recorrida.
    '''
    v_dist = []
    vector_v = []
    vector_t = []
    vector_td = []
    for i,tramo in enumerate(lista):
        if i != len(lista)-1:
            zancada = dist/len(tramo)
            for j,paso in enumerate(tramo):
                if j > 0:
                    periodo = (paso-tramo[j-1])/100 #Partido 100 para pasarlo a segundos
                    speed = zancada/periodo
                    tiempo = (paso + tramo[j-1])/2
                    vector_t.append(tiempo)
                    vector_v.append(speed)
                    v_dist.append(zancada)
                    vector_td.append(tiempo)
            v_dist.append(0.5*pi)
            tiempo = (tiempo+lista[i+1][0])/2
            vector_td.append(tiempo)
    #El último tramo tiene una longitud distinta
    zancada = last/len(lista[-1])
    for i,paso in enumerate(lista[-1]):
        if i > 0:
            periodo = (paso-tramo[i-1])/100 #Partido 100 para pasarlo a segundos. Creo que está mal
            speed = zancada/periodo
            tiempo = (paso + tramo[i-1])/2
            vector_t.append(tiempo)
            vector_v.append(speed)
            v_dist.append(zancada)
            vector_td.append(tiempo)
    dist_acum = [v_dist[0]]
    acumulado = 0
    for i,paso in enumerate(v_dist):
        if i > 0:
            for j in range(0,i):
                acumulado =acumulado + v_dist[j]
            dist_acum.append(acumulado)
            acumulado = 0

    mv5, t5 = media_movil(vector_v,vector_t,5)
    mv10, t10 = media_movil(vector_v,vector_t,10)
    mv15, t15 = media_movil(vector_v,vector_t,15)
        
    return t15,mv15

def analisis_movimiento(minutos, AceleracionX, AceleracionY, AceleracionZ, GiroX, GiroY, GiroZ, longitud_largos, ploting, threshold):
    """
    Función para realizar el análisis del movimiento del paciente. Detecta los cambios de sentido, para cada tramo llama a
    la funcion calculo_pasos y calcula la distancia recorrida y la velocidad.

    Parámetros :
    minutos: 'float'
        Duracion de la prueba [min]
    AceleracionX: 'list[float]'
        Datos de aceleración del eje X de la prueba del paciente rango -32768, 32767
    AceleracionY: 'list[float]'
        Datos de aceleración del eje Y de la prueba del paciente rango -32768, 32767
    AceleracionZ: 'list[float]'
        Datos de aceleración del eje Z de la prueba del paciente rango -32768, 32767
    GiroX: 'list[float]'
        Datos de giro del eje X de la prueba del paciente rango -32768, 32767
    GiroY: 'list[float]'
        Datos de giro del eje Y de la prueba del paciente rango -32768, 32767
    GiroZ: 'list[float]'
        Datos de giro del eje Z de la prueba del paciente rango -32768, 32767
    t: 'list[float]'
        Valores de tiempo correspondientes a las medidas de los sensores de la prueba del paciente
    longitud_largos: 'float'
        Longitud del tramo del pasillo en el que se realiza la prueba [m]
    start: 'int'
        Instante de tiempo de inicio de la prueba del paciente

    Returns :
    tiempo_pasos: 'list[float]'
        Instantes de tiempo correspondientes a los datos de distancia recorrida (instantes en los que se produce cada paso)
    contador_distancia: 'list[float]'
        Datos de distancia recorrida
    tiempo_velocidad: 'list[float]'
        Instantes de tiempo correspondientes a los datos de velocidad
    velocidad: 'list[float]'
        Datos de velocidad
    """
    #Parámetros constantes
    FSCg = 1000
    #Definimos un vector tiempo para simplificar
    t = []
    for i in range(len(GiroX)):
        t.append(i)
    gx = grado2uni(GiroX)
    start = getPacientes(gx) #guardo en una lista los instantes de tiempo donde empieza cada paciente
    nPacientes = len(start)

    #Eliminamos el error constante de las medidas del giroscopio
    GxBias = -268*FSCg*0.01/2**15
    GyBias = -12*FSCg*0.01/2**15
    GzBias = -63*FSCg*0.01/2**15
    updatedGx = []
    updatedGy = []
    updatedGz = []
    aMod = []
    for i in range(len(GiroY)):
        updatedGx.append(GiroX[i]-GxBias)
        updatedGy.append(GiroY[i]-GyBias)
        updatedGz.append(GiroZ[i]-GzBias)
        acc = sqrt(AceleracionX[i]**2+AceleracionY[i]**2+AceleracionZ[i]**2)
        aMod.append(acc)
    #Calculo de los ángulos instantáneos
    Dgx = deltaList(updatedGx)
    Dgy = deltaList(updatedGy)
    
    
    cambiosPaciente = []
    valuePaciente = []

    b, a = sm.signal.build_filter(frequency=0.25,
                            sample_rate=100,
                            filter_type='low',
                            filter_order=4)
    Dgy_fil = sm.signal.filter_signal(b,a,signal = Dgy)
    b, a = sm.signal.build_filter(frequency=0.25,
                            sample_rate=100,
                            filter_type='low',
                            filter_order=4)
    Dgx_fil = sm.signal.filter_signal(b,a,signal = Dgx)

    for paciente in range(nPacientes):
        cambios_sentido, cambiosValue, start_cambio, startValue,CAMBIOS2, CAMBIOS = getCambios(Dgy_fil,start[paciente],threshold,minutos)
        cambiosPaciente.append(cambios_sentido)
        valuePaciente.append(cambiosValue)
        
        a = start[paciente]*100
        b = a + 6*60*100
        
        distancia = 0
        pasosTOT = 0
        listaPasos = []
        
        distancia, pasosTOT, listaPasos, PLOT, pasos_lista, ult_dist = getPasos(AceleracionY[a:b],start[paciente],minutos,longitud_largos,CAMBIOS2)
        
        mensaje = 'Distancia total recorrida del paciente '+str(paciente+1)+' es: '+ str(distancia)+'m'
        mensaje2 = 'Distancia[m]: '+str(distancia)+'\nTotal Pasos: '+str(pasosTOT)
        print(mensaje)
        print(listaPasos)
        
        inicia = start[paciente]*100
        finaliza = 60*100*minutos+start[paciente]*100
        
        startGiro = []
        finGiro = [CAMBIOS[0][0]]
        for i in range(1,len(CAMBIOS)):
            startGiro.append(CAMBIOS[-i][1])
            finGiro.append(CAMBIOS[i][0])
        startGiro.append(CAMBIOS[0][1])

        CHANGE = [Dgy_fil[inicia:finaliza],startGiro,startValue,finGiro,cambiosValue]
        
        ########################### CÁLCULO VELOCIDAD ################################
        #Necesitamos pasar por parámetro pasos_lista + longitud_largos       
        vect_T = []
        vmedia_vect = []
        anterior = 0
        vect_v = []
        for i in range(0,minutos*100*60):
            vect_T.append(i)
        for giro in CAMBIOS:
            vmedia = (longitud_largos*100/(giro[1]-anterior), giro[1])
            vmedia_vect.append(vmedia)
            anterior = giro[0]
        vmedia = ult_dist*100/(minutos*100*60-anterior)
        vmedia_vect.append((vmedia, vect_T[-1]))
        for t in vect_T:
            inicio = 0
            for a, b in vmedia_vect:
                if t == b:
                        inicio = b
                if b>inicio and t<=b:
                    vect_v.append(a) 
                    break

        v_t,v_v = getSpeed(pasos_lista,longitud_largos, vect_v, ult_dist,ploting)
        
    return start, v_t, v_v, distancia, ult_dist, vect_v, CHANGE

def representResults(vel_t,vel_v,v_media,HR_t,HR_v,RR_t,RR_v,dist,last_dist,namePaciente,CAMBIO):
    '''
    Función para representar los resultados

    Parámetros:
    vel_t: 'list[int]'
        vector con los instantes de tiempo de la velocidad instantánea
    vel_v:  'list[float]'
        vector con los valores de la velocidad instantánea
    v_media: 'list[float]'
        vector para representar la velocidad media
    HR_t: 'list[int]'
        vector con los instantes de tiempo de la frecuencia cardíaca
    HR_v: 'list[float]'
        vector con los valores de la frecuencia cardíaca
    RR_t: 'list[int]'
        vector con los instantes de tiempo de la frecuencia respiratoria
    RR_v: 'list[float]'
        vector con los valores de la frecuencia respiratoria
    dist: 'int'
        valor de la distancia total recorrida
    last_dist: 'int'
        valor de la distancia recorrida en el último tramo
    namePaciente: 'str'
        nombre del paciente
    CAMBIO: 'list[list]'
        lista de listas con los datos necesarios para la representación de los cambios de sentido
    '''
    
    #Se calculan los valores máximos y medios de las señales a representar
    vmedia = media(vel_v)
    HRmedia = media(HR_v)
    RRmedia = media(RR_v)
    vmax = max(vel_v)
    HRmax = max(HR_v)
    RRmax = max(RR_v)

    #Se abre una ventana (root) para visualizar los resultados de la prueba
    root = Tk()
    root.iconbitmap('girl_walking.ico')
    root.geometry("1200x600")
    root.title("Datos prueba: "+ namePaciente)
    frame = Frame(root)
    fig = figure.Figure(figsize=(3, 2), dpi=80)
    #Se colocan 4 sistemas de ejes en la figura
    ax0 = fig.add_axes((0.3, .55, .25, .35), frameon=True)
    # ax1 = fig.add_axes((0.05, .1, .4, .35), frameon=True)
    ax2 = fig.add_axes((0.4, .1, .4, .35), frameon=True) #VELOCIDAD
    ax3 = fig.add_axes((0.65, .55, .25, .35), frameon=True)
    #En los ejes 0 se representa la frecuencia cardíaca
    ax0.set_xlabel("Tiempo [muestras]")
    ax0.set_ylabel("frec. cardíaca [ppm]",color = "red")
    ax0.set_title("Frecuencia cardiaca y velocidad")
    #En los ejes 1 se representa los cambios de sentido
    # ax1.set_xlabel("Tiempo [muestras]")
    # ax1.set_ylabel("Variación de ángulo [°]")
    # ax1.set_title("Cambios de sentido")
    #En los ejes 2 se representa la velocidad instantánea
    ax2.set_xlabel("Tiempo [muestras]")
    ax2.set_ylabel("velocidad [m/s]")
    ax2.set_title("Velocidad")
    #En los ejes 3 se representa la frecuencia respiratoria
    ax3.set_xlabel("Tiempo [muestras]")
    ax3.set_ylabel("frec. respiratoria [rpm]",color = "red")
    ax3.set_title("Frecuencia respiratoria y velocidad")

    #Se plotean las 4 señales corerrespondientes
    ax0.plot(HR_t, HR_v, "red")
    # ax1.plot(CAMBIO[0])
    # ax1.plot(CAMBIO[1],CAMBIO[2],'ro')
    # ax1.plot(CAMBIO[3],CAMBIO[4],'go')
    # ax1.legend(('Ángulo','Inicio cambio de sentido','Fin cambio de sentido'))
    ax2.plot(vel_t, vel_v, 'dodgerblue')
    ax2.plot(v_media,'green')
    ax2.legend(('Velocidad instantánea','Velocidad media'))
    ax3.plot(RR_t, RR_v, "red")

    #Sobre la gráfica de frecuencia cardíaca se muestra la de velocidad
    ax4=ax0.twinx() #Parámetro que permite representar dos señales con diferentes ejes X en la misma gráfica
    ax4.plot(vel_t, vel_v,'dodgerblue')
    ax4.set_ylabel("velocidad [m/s]",color = 'dodgerblue')

    #Sobre la gráfica de frecuencia respiratoria se muestra la de velocidad
    ax5 = ax3.twinx() #Parámetro que permite representar dos señales con diferentes ejes X en la misma gráfica
    ax5.plot(vel_t, vel_v,'dodgerblue')
    ax5.set_ylabel("velocidad [m/s]",color = 'dodgerblue')

    #Se muestran las figuras en la ventana
    frame.pack(side=LEFT, fill=BOTH, expand=1)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    canvas.draw()
    toolbar=NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    #Se muestran en labels los datos de mayor interés de la prueba en la esquina superiror izquierda de la ventana
    etiqueta = Label(frame, text="Resumen de datos:", font=("Calibri", 14), fg="black", bg="white").place(x=30, y=210)
    etiqueta = Label(frame, text="Distancia recorrida: " + str(round(dist,2)) + " m", font=("Calibri", 12),
                    fg="black", bg="white").place(x=30, y=240)
    etiqueta = Label(frame, text="Distancia último tramo: " + str(round(last_dist,2)) + " m", font=("Calibri", 12),
                    fg="black", bg="white").place(x=30, y=260)
    etiqueta = Label(frame, text="Frecuencia cardíaca media: " + str(round(HRmedia,2)) + " ppm", font=("Calibri", 12),
                    fg="black", bg="white").place(x=30, y=280)
    etiqueta = Label(frame, text="Frecuencia cardíaca máxima: " + str(round(HRmax,2)) + " ppm", font=("Calibri", 12),
                    fg="black", bg="white").place(x=30, y=300)
    etiqueta = Label(frame, text="Frecuencia respiratoria media: " + str(round(RRmedia,2)) + " resp/min", font=("Calibri", 12),
                    fg="black", bg="white").place(x=30, y=320)
    etiqueta = Label(frame, text="Frecuencia respiratoria máxima: " + str(round(RRmax,2)) + " resp/min", font=("Calibri", 12),
                    fg="black", bg="white").place(x=30, y=340)
    etiqueta = Label(frame, text="Velocidad media: " + str(round(vmedia,2)) + " m/s", font=("Calibri", 12), fg="black",
                    bg="white").place(x=30, y=360)
    etiqueta = Label(frame, text="Velocidad máxima: " + str(round(vmax,2)) + " m/s", font=("Calibri", 12), fg="black",
                    bg="white").place(x=30, y=380)
    
    root.mainloop() #Loop infinito para representar la ventana

    return 0