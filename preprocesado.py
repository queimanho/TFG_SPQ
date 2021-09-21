"""
    Módulo que almacena las dos funciones para dividir los datos del fichero principal
    en varios archivos con las señales separadas.

"""

from funciones import*
from tkinter import*
from tkinter import messagebox

def grabarFichero(data, nameFile):
    """
    Función para grabar datos en un fichero

    Parámetros:
        data: 'List[Any]'
            Datos que queremos guardar
        nameFile: 'str'
            Nombre que le queremos dar al Fichero.
    """

    fileN = open(nameFile, 'w') #Se crea el archivo si no existe. Si existe se sobreescribe.
    for i in range(0, len(data),1):
       fileN.write(str(data[i]))
       fileN.write(' ')
       fileN.write('\n')
    fileN.close()


def separarDatos(fichero_pulsera):
    """
    Función para dividir el fichero obtenido del micro para tratar esos datos
    Crea los ficheros y devuelve el número de pacientes detectados.

    Parámetros
    fichero_pulsera: 'str'
        Nombre del archivo descargado
    """
    print(fichero_pulsera)

    #Extracción de los datos del archivo
    try:
        fichero = open(fichero_pulsera)
        contenido = fichero.read()
        fichero.close()
    except:
        print("FA WATCH", "El fichero que has seleccionado no exste o no está en el directorio raíz, inténtalo de nuevo")
    
    datos = contenido.split()
    
    #Separación de cada una de las variables
    ppgData = []
    acelX = []
    acelY = []
    acelZ = []
    giroX = []
    giroY = []
    giroZ = []
    byteExtra = []

    for z in range(0, len(datos), 16):
        ppgData.append((int(datos[z], 16) << 16) + (int(datos[z + 1], 16) << 8) + int(datos[z + 2], 16))
        acelX.append((int(datos[z + 3], 16) << 8) + (int(datos[z + 4], 16))) 
        #int(dato, 16) pasamos de hex a decimal y el primer byte lo shifteamos (<<8) hacia la izquierda
        acelY.append((int(datos[z + 5], 16) << 8) + (int(datos[z + 6], 16)))
        acelZ.append((int(datos[z + 7], 16) << 8) + (int(datos[z + 8], 16)))
        giroX.append((int(datos[z + 9], 16) << 8) + (int(datos[z + 10], 16)))
        giroY.append((int(datos[z + 11], 16) << 8) + (int(datos[z + 12], 16)))
        giroZ.append((int(datos[z + 13], 16) << 8) + (int(datos[z + 14], 16)))
        byteExtra.append(int(datos[z + 15], 16))
    
    #Normalización de los datos del giroscopio en el rango -32768, 32767
    for i in range(len(giroX)):
        if (giroX[i] >= 2**15):
            giroX[i] = (giroX[i] - 2**16)

        if (giroY[i] >= 2**15):
            giroY[i] = (giroY[i] - 2**16)
        
        if (giroZ[i] >= 2**15):
            giroZ[i] = (giroZ[i] - 2**16)
    
    #Convertir los valores de la señal del acelerómetro al rango -32768, 32767
    for i in range(len(acelX)):
        if (acelX[i] >= 2**15):
            acelX[i] = (acelX[i] - 2**16)

        if (acelY[i] >= 2**15):
            acelY[i] = (acelY[i] - 2**16)
        
        if (acelZ[i] >= 2**15):
            acelZ[i] = (acelZ[i] - 2**16)
    

    #Se guarda cada señal en un fichero txt
    
    nombreFichero = 'TESTS/vector_PPG_original_'+fichero_pulsera+'.txt'
    grabarFichero(ppgData, nombreFichero)

    nombreFichero = 'TESTS/vector_giroscopioX_'+fichero_pulsera+'.txt'
    grabarFichero(giroX, nombreFichero)

    nombreFichero = 'TESTS/vector_giroscopioY_'+fichero_pulsera+'.txt'
    grabarFichero(giroY, nombreFichero)

    nombreFichero = 'TESTS/vector_giroscopioZ_'+fichero_pulsera+'.txt'
    grabarFichero(giroZ, nombreFichero)
    
    nombreFichero = 'TESTS/vector_acelX_'+fichero_pulsera+'.txt'
    grabarFichero(acelX, nombreFichero)

    nombreFichero = 'TESTS/vector_acelY_'+fichero_pulsera+'.txt'
    grabarFichero(acelY, nombreFichero)
    
    nombreFichero = 'TESTS/vector_acelZ_'+fichero_pulsera+'.txt'
    grabarFichero(acelZ, nombreFichero)

    t = []
    for i in range(len(giroX)):
        t.append(i)
    gx = grado2uni(giroX)
    start = getPacientes(gx) #guardo en una lista los instantes de tiempo donde empieza cada paciente
    
    messagebox.showinfo("Info", "Se ha detectado "+str(len(start))+" prueba(s)")
    root = Tk()
    root.iconbitmap('girl_walking.ico')
    root.geometry("400x220")
    root.title("Identificación de las pruebas")
    etiqueta=Label(root,text="Introduce los números de identificación de los pacientes",font=("Calibri",13),fg="black").place(x=20,y=10)
    etiquetas=((Label(root, text="Prueba número "+str(0+1)+":", font=("Calibri", 12), fg="black").place(x=20, y=10+(0+1)*30)))
    variable=StringVar()
    entradas=(Entry(root,textvariable=variable))
    entradas.place(x=200,y=10+(0+1)*30)

    etiquetas=((Label(root, text="Prueba número "+str(1+1)+":", font=("Calibri", 12), fg="black").place(x=20, y=10+(1+1)*30)))
    variable=StringVar()
    entradas=(Entry(root,textvariable=variable))
    entradas.place(x=200,y=10+(1+1)*30)

    etiquetas=((Label(root, text="Prueba número "+str(2+1)+":", font=("Calibri", 12), fg="black").place(x=20, y=10+(2+1)*30)))
    variable=StringVar()
    entradas=(Entry(root,textvariable=variable))
    entradas.place(x=200,y=10+(2+1)*30) 
    
    buttonOK = Button(root, text="OK",command=root.quit).place(x=200,y=200)
    
    root.mainloop()

    return(len(start))
#separarDatos("FilesPaciente1/2020.07.06-10.11.38.txt",'paciente1')
# separarDatos("C:/Users/Usuario/Desktop/TFG/TFG_Maria/Codigo/TESTING/pruebaCASTRO3.txt",'PRUEBA_CASTRO3')

def separarDatosV2(fichero_pulsera, idPaciente):
    """
    Función para dividir el fichero obtenido del micro para tratar esos datos

    Parametros:
    fichero_pulsera: 'str'
        Nombre del archivo descargado
    idPaciente: 'str'
        Nombre del paciente
    """
    print(fichero_pulsera)

    #Extracción de los datos del archivo
    try:
        fichero = open(fichero_pulsera)
        contenido = fichero.read()
        fichero.close()
    except:
        print("FA WATCH", "El fichero que has seleccionado no exste o no está en el directorio raíz, inténtalo de nuevo")
    
    datos = contenido.split()
    
    #Separación de cada una de las variables
    ppgData = []
    acelX = []
    acelY = []
    acelZ = []
    giroX = []
    giroY = []
    giroZ = []
    byteExtra = []

    for z in range(0, len(datos), 16):
        ppgData.append((int(datos[z], 16) << 16) + (int(datos[z + 1], 16) << 8) + int(datos[z + 2], 16))
        acelX.append((int(datos[z + 3], 16) << 8) + (int(datos[z + 4], 16))) 
        #int(dato, 16) pasamos de hex a decimal y el primer byte lo shifteamos (<<8) hacia la izquierda
        acelY.append((int(datos[z + 5], 16) << 8) + (int(datos[z + 6], 16)))
        acelZ.append((int(datos[z + 7], 16) << 8) + (int(datos[z + 8], 16)))
        giroX.append((int(datos[z + 9], 16) << 8) + (int(datos[z + 10], 16)))
        giroY.append((int(datos[z + 11], 16) << 8) + (int(datos[z + 12], 16)))
        giroZ.append((int(datos[z + 13], 16) << 8) + (int(datos[z + 14], 16)))
        byteExtra.append(int(datos[z + 15], 16))
    
    #Normalización de los datos del giroscopio en el rango -32768, 32767
    for i in range(len(giroX)):
        if (giroX[i] >= 2**15):
            giroX[i] = (giroX[i] - 2**16)

        if (giroY[i] >= 2**15):
            giroY[i] = (giroY[i] - 2**16)
        
        if (giroZ[i] >= 2**15):
            giroZ[i] = (giroZ[i] - 2**16)
    
    #Convertir los valores de la señal del acelerómetro al rango -32768, 32767
    for i in range(len(acelX)):
        if (acelX[i] >= 2**15):
            acelX[i] = (acelX[i] - 2**16)

        if (acelY[i] >= 2**15):
            acelY[i] = (acelY[i] - 2**16)
        
        if (acelZ[i] >= 2**15):
            acelZ[i] = (acelZ[i] - 2**16)
    

    #Se guarda cada señal en un fichero txt
    
    nombreFichero = 'TESTS/vector_PPG_original_'+idPaciente+'.txt'
    grabarFichero(ppgData, nombreFichero)

    nombreFichero = 'TESTS/vector_giroscopioX_'+idPaciente+'.txt'
    grabarFichero(giroX, nombreFichero)

    nombreFichero = 'TESTS/vector_giroscopioY_'+idPaciente+'.txt'
    grabarFichero(giroY, nombreFichero)

    nombreFichero = 'TESTS/vector_giroscopioZ_'+idPaciente+'.txt'
    grabarFichero(giroZ, nombreFichero)
    
    nombreFichero = 'TESTS/vector_acelX_'+idPaciente+'.txt'
    grabarFichero(acelX, nombreFichero)

    nombreFichero = 'TESTS/vector_acelY_'+idPaciente+'.txt'
    grabarFichero(acelY, nombreFichero)
    
    nombreFichero = 'TESTS/vector_acelZ_'+idPaciente+'.txt'
    grabarFichero(acelZ, nombreFichero)
