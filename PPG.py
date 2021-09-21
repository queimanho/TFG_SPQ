from math import *
from scipy.optimize import fsolve
from scipy.signal import find_peaks,medfilt
import numpy as np
import sensormotion as sm
from pylab import *
from funciones import media,media_movil, mejora_media
from scipy import arange
from scipy.fftpack import fft, fftfreq

#En el preprocesado, le aplicamos un Filtro Paso Bajo con fc = 10 Hz
def preprocesadoPPG(data):

    '''
    Función que realiza el procesado de la señal PPG cruda

    Devuelve las componentes en frecuencia de la frecuencia cardíaca, respiratoria, y la señal
    PPG con el filtro inicial por si se desea representar.
    '''

    # Voy a probar a quitar la señal de continua restando la media
    data_AC = []
    dc_signal = media(data)

    PPG2 = [] #Señal sin componente de continua (en teoría), con filtro promediado.
    PPG3 = []
    arr = np.array(data)
    filMED = medfilt(arr,251)
    for i in range(len(arr)):
        PPG2.append(arr[i]-filMED[i])
        PPG3.append(PPG2[i]-dc_signal)
    ppg2media = media(PPG2)
    for i in range(len(PPG2)):
        PPG2[i] = PPG2[i] - ppg2media

    for i in range(len(data)):
        data_AC.append(data[i]-dc_signal)
    

    b, a = sm.signal.build_filter(frequency=10,
                            sample_rate=100,
                            filter_type='low',
                            filter_order=8)
    filtrada1 = sm.signal.filter_signal(b,a,signal = data)

    PPG2_2 = [] #Señal sin componente de continua (en teoría), con filtro promediado.
    arr = np.array(filtrada1)
    filMED_2 = medfilt(arr,251)
    for i in range(len(arr)):
        PPG2_2.append((arr[i]-filMED_2[i]))
    mPP = media(PPG2_2)
    # print(mPP)
    for i in range(len(PPG2_2)):
        PPG2_2[i] -= mPP
    # print(media(PPG2_2))

    b, a = sm.signal.build_filter(frequency=0.1,
                            sample_rate=100,
                            filter_type='high',
                            filter_order=5)
    filtrada2 = sm.signal.filter_signal(b,a,signal = filtrada1)

    # Si queremos filtrar de 0.1 a 10 Hz y eliminar la compenente a 0 Hz
    b, a = sm.signal.build_filter(frequency=[0.1, 10],
                            sample_rate=100,
                            filter_type='bandpass',
                            filter_order=3)
    filtrada = sm.signal.filter_signal(b,a,signal = PPG2)

    b, a = sm.signal.build_filter(frequency=[1, 1.5],
                                sample_rate=100,
                                filter_type='bandpass',
                                filter_order=3)
    card = sm.signal.filter_signal(b, a, signal=PPG2)

    #0.1,0.4
    b, a = sm.signal.build_filter(frequency=[0.27, 0.42], #Rango de 16,2 - 25,2 rpm
                                sample_rate=100,
                                filter_type='bandpass',
                                filter_order=3)
    resp = sm.signal.filter_signal(b, a, signal=PPG2_2)

    return card, resp, PPG2_2

def plotSpectrum(y,Fs):

    """
    grafica la amplitud del espectro de y(t)

    """
    n = len(y) # longitud de la señal
    k = arange(n)
    T = n/Fs
    frq = k/T # 2 lados del rango de frecuancia
    frq = frq[range(int(n/2))] # Un lado del rango de frecuencia
    Y = fft(y)/n # fft calcula la normalizacion
    Y = Y[range(int(n/2))]

    b, a = sm.signal.build_filter(frequency=25,
                            sample_rate=100,
                            filter_type='low',
                            filter_order=8)
    Yf = sm.signal.filter_signal(b,a,signal = Y)


    plot(frq, abs(Y),'b')
    xlabel('Frecuencia (Hz)')
    ylabel('|Y(f)|')

def calcula_RR(resp,window, ploting):
    '''
    Función que calcula la frecuencia respiratoria

    Parámetros:
    resp: 'list[float]'
        componente de la respiración extraida
    window: 'int'
        Entero que determina el valor de la ventana de tiempo [en segundos] para calcular la FR
    ploting: 'Boolean'
        Booleano para representar o no la Frec Resp
    '''
    window = window*100
    listT = []
    t = []
    for k in range(len(resp)):
        t.append(k)
    RR = []
    RRbpm = []
    total_peaks = 0
    minimo = 0.6
    distancia = 200
    tot_peak = []
    tot_values = []
    rrlist = []
    timeList = []
    for i in range(0,len(resp)-(window-1),window):
        peak_times, peak_values = sm.peak.find_peaks(time = t[i:i+window],signal=resp[i:i+window],
                                                 peak_type='peak',
                                                 min_val=minimo, min_dist=distancia, plot=False)
       
        for j in range(len(peak_times)):
            tot_peak.append(peak_times[j])
            tot_values.append(peak_values[j])
        # plot(peak_times,peak_values,'ro')
        ###
        # for j in range(1000):
        total_peaks += len(peak_times)
        listT = []
        RRbpm.append(len(peak_times)*6)
        for j in range(len(peak_times)-1):
            listT.append(peak_times[j+1]-peak_times[j])
            rrlist.append(60*100/(peak_times[j+1]-peak_times[j]))
            timeList.append(peak_times[j])
        if len(listT) != 0:
            periodo = media(listT)
            RR.append(60*100/periodo)
    # if (len(resp) % 1000 != 0):
    #     print("HOLI")
    RT = []
    for i in range(len(tot_peak)-1):
        periodo = tot_peak[i+1]-tot_peak[i]
        RT.append(60*100/periodo)

    resto = len(tot_peak) % 3
    entero = len(tot_peak)//3

    mv5,tmv5 = media_movil(rrlist,timeList,5)
    mv10,tmv10 = media_movil(rrlist,timeList,10)
    mv15,tmv15 = media_movil(rrlist,timeList,15)

    if ploting:
        plot(resp)
        plot(tot_peak,tot_values,'ro')
        title('Señal PPG frecuencia respiratoria',fontsize=25)
        legend(('Señal frecuencia respiratoria','Picos de la señal'),fontsize=20)
        xlabel('Tiempo [muestras]',fontsize=25)
        show()
        plot(timeList,rrlist)
        plot(tmv5, mv5)
        plot(tmv10, mv10)
        
        plot(tmv15, mv15,'red')
        title('Frecuencia respiratoria') # Ventanas de 20s (6,67 picos/ventana)
        legend(('Señal ','MA(5)','MA(10)','MA(15)'))
        xlabel('Tiempo [muestras]')
        ylabel('Frecuencia respiratoria [rpm]')
        show()

    return tmv15, mv15

def calcula_HR(card,window, ploting):
    '''
    Función que calcula la frecuencia cardíaca

    Parámetros:
    card: 'list[float]'
        componente de las pulsaciones extraida
    window: 'int'
        Entero que determina el valor de la ventana de tiempo [en segundos] para calcular la Freq Card
    ploting: 'Boolean'
        Booleano para representar o no la Frec Card
    '''
    window = window*100
    listT = []
    t = []
    for k in range(len(card)):
        t.append(k)
    HR = []
    RRbpm = []
    total_peaks = 0
    minimo = 0.4
    distancia = 50
    tot_peak = []
    tot_values = []
    rhlist = []
    timeList = []
    rhlist2 = []
    for i in range(0,len(card)-(window-1),window):
        peak_times, peak_values = sm.peak.find_peaks(time = t[i:i+window],signal=card[i:i+window],
                                                 peak_type='peak',
                                                 min_val=minimo, min_dist=distancia, plot=False)
       
        for j in range(len(peak_times)):
            tot_peak.append(peak_times[j])
            tot_values.append(peak_values[j])
        # plot(peak_times,peak_values,'ro')
        ###
        # for j in range(1000):
        total_peaks += len(peak_times)
        listT = []
        RRbpm.append(len(peak_times)*60*100/window)
        for j in range(len(peak_times)-1):
            listT.append(peak_times[j+1]-peak_times[j])
            rhlist.append(60*100/(peak_times[j+1]-peak_times[j]))
            timeList.append(peak_times[j])
        if len(listT) != 0:
            periodo = media(listT)
            HR.append(60*100/periodo)
            new_listT = mejora_media(listT,10)
            for i in new_listT:
                rhlist2.append(i)

    # if (len(resp) % 1000 != 0):
    #     print("HOLI")
    RT = []
    for i in range(len(tot_peak)-1):
        periodo = tot_peak[i+1]-tot_peak[i]
        RT.append(60*100/periodo)
    RR = []
    for i in range(0,len(tot_peak)-2, 3):
        periodo = (tot_peak[i+2]-tot_peak[i])/3
        RR.append(60*100/periodo)
    resto = len(tot_peak) % 3
    entero = len(tot_peak)//3
    # if resto == 2:
    #     periodo = (tot_peak[entero+resto]-tot_peak[entero])/(resto+1)
    #     RR.append(60*100/periodo)
    # print(tot_peak)
    # print('El número total de pulsaciones fueron: '+str(total_peaks))
    mv10,tmv10 = media_movil(rhlist,timeList,10)
    mv15,tmv15 = media_movil(rhlist,timeList,15)
    mv20,tmv20 = media_movil(rhlist,timeList,20)
    if ploting:
        plot(card)
        plot(tot_peak,tot_values,'ro')
        title('Señal PPG ritmo cardíaco',fontsize=25)
        legend(('Señal ritmo cardíaco','Picos de la señal'),fontsize=20)
        xlabel('Tiempo [muestras]',fontsize=25)
        show()
        plot(timeList,rhlist)
        plot(tmv10, mv10)
        plot(tmv15, mv15)
        plot(tmv20, mv20)
        title('Frecuencia cardíaca')
        legend(('Señal ','MA(10)','MA(15)','MA(20)'))
        xlabel('Tiempo [muestras]')
        ylabel('Frecuencia cardíaca [ppm]')
        show()
    
    return tmv20, mv20