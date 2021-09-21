from funciones import varianza
from descarga import*
from preprocesado import*
from tkinter import*
from tkinter import messagebox
import time
import os
import pandas as pd
import tkinter.ttk as Ttk

if (os.path.isfile('DataBase.csv') == False): #Se comprueba si existe el archivo "BaseDatos.csv" y si no se crea
  data = pd.DataFrame(columns=['idPaciente', 'Fecha','Longitud','Duracion','Distancia_Total','Ult_tramo','HR_medio','HR_max','RR_medio','RR_max','V_media','V_max'])
  data.to_csv('DataBase.csv', header=True, index=False)

if (os.path.isfile('DataBase.xlsx') == False): #Se comprueba si existe el archivo "BaseDatos.csv" y si no se crea
  data = pd.DataFrame(columns=['idPaciente', 'Fecha','Longitud','Duracion','Distancia_Total','Ult_tramo','HR_medio','HR_max','RR_medio','RR_max','V_media','V_max'])
  data.to_excel('DataBase.xlsx', header=True, index=False)

def pacientes():
  messagebox.showinfo("Info", "Se ha detectado 1 prueba(s)")
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

def buscaHistorial(idPaciente):
  # messagebox.showinfo('Info','No se ha encontrado en la base de datos ninguna prueba con el ID indicado.')
  identificacion = idPaciente
  datos = pd.read_csv('DataBase.csv')
  resultado = datos[datos.idPaciente == identificacion] #Filas de la base de dato con el mismo paciente
  if len(resultado==0):
    tkinter.messagebox.showinfo("Info", "No hay datos del paciente seleccionado")
  else:
    ventanaHistorial = Tk()                            #Si se encuentran resultados del paciente buscado se abre una
    ventanaHistorial.geometry("450x150+200+200")       #ventana para seleccionar la prueba que se quiere visualizar
    ventanaHistorial.title("Historial del paciente")
    ventanaHistorial.iconbitmap('girl_walking.ico')
    etiqueta = Label(ventanaHistorial, text="Resultados encontrados para el paciente: "+identificacion,
                    font=("Calibri", 13), fg="black").place(x=20, y=10)

    etiqueta = (Label(ventanaHistorial, text='Fecha y hora de la prueba: ',
                          font=("Calibri", 12),
                          fg="black").place(x=20, y=60))
    
    def selecVisual():
      seleccionado = combo.get()
      is_selecionado = resultado.loc[:, 'Fecha'] == seleccionado
      resultado_selecionado = resultado.loc[is_selecionado].values.tolist() #Fila de la base de datos de la prueba seleccionada
      rootVis = Tk()
      rootVis.geometry("300x150")
      rootVis.title("Resultados")
      rootVis.iconbitmap('girl_walking.ico')
      etiqueta = Label(rootVis, text="Seleccione lo que quiere visualizar:",font=("Calibri", 13), fg="black").place(x=30, y=30)
      b1 = Button(rootVis, text="RESULTADOS",command=rootVis.quit).place(x=50, y=100)
      b2 = Button(rootVis, text="REVISIÓN",command=rootVis.quit).place(x=170, y=100)

    combo = Ttk.Combobox(ventanaHistorial,textvariable='Fecha y hora de la prueba:', values=resultado.iloc[:,1].values.tolist() )
    combo.place(x=200, y=62)
    boton = (Button(ventanaHistorial, text="Obtener resultados",command=lambda:selecVisual))
    boton.place(x=80, y=100)

    
ventana=Tk()
ventana.geometry("450x420+200+200")
ventana.title("PD6MM")
ventana.iconbitmap('girl_walking.ico')
Canvas1=Canvas(ventana)
Canvas1.pack(fill="x")
Canvas1.config(bd=3)
Canvas1.config(relief="sunken")
Canvas1.config(width=400,height=130)
Canvas2=Canvas(ventana)
Canvas2.pack(fill="x")
Canvas2.config(bd=3)
Canvas2.config(relief="sunken")
Canvas2.config(width=400,height=160)
Canvas3=Canvas(ventana)
Canvas3.pack(fill="x")
Canvas3.config(bd=3)
Canvas3.config(relief="sunken")
Canvas3.config(width=400,height=100)
#------------------------------------------------------------------------------------------
###### Zona de descarga de datos ######
(puertos_disponibles, hay_puerto)=scan()
etiqueta= Label(Canvas1,text="DESCARGA DE DATOS:",font=("Calibri",12),fg="black").place(x=10,y=10)
etiqueta= Label(Canvas1,text="Introduce el nombre del nuevo fichero:",font=("Calibri",12),fg="black").place(x=10,y=40)
file_name=StringVar()
file_name.set("%s.%s.%s-%s.%s.%s.txt"%(time.strftime("%Y"),time.strftime("%m"),time.strftime("%d"),time.strftime("%H"),time.strftime("%M"),time.strftime("%S")))
campo=Entry(Canvas1,textvariable=file_name).place(x=270,y=45)
etiqueta= Label(Canvas1,text="Introduce el puerto COM (ej: COM3):",font=("Calibri",12),fg="black").place(x=10,y=65)
numero_puerto=StringVar()
if hay_puerto:
  print (puertos_disponibles[0][1])
  numero_puerto.set("%s" %puertos_disponibles[0][1])
  campo=Entry(Canvas1,textvariable=numero_puerto).place(x=270,y=70)
  boton=Button(ventana,command=lambda: Aceptar_descarga(numero_puerto.get(), file_name.get() ),text="Descargar").place(x=150,y=100)
else:
  numero_puerto.set("")
  campo=Entry(Canvas1, textvariable=numero_puerto).place(x=270,y=70)
  boton=Button(Canvas1,command=lambda: Aceptar_descarga(numero_puerto.get(), file_name.get() ),text="Descargar").place(x=150,y=100)
#--------------------------------------------------------------------------------------------
###### Zona de obtencion de resultados ######
etiqueta= Label(Canvas2,text="OBTENCIÓN DE RESULTADOS:",font=("Calibri",12),fg="black").place(x=10,y=10)
etiqueta= Label(Canvas2,text="Introduce el nombre del fichero existente:",font=("Calibri",12),fg="black").place(x=10,y=40)
file_name_read_2=StringVar()
file_name_read_2.set("%s.%s.%s-%s.%s.%s.txt"%(time.strftime("%Y"),time.strftime("%m"),time.strftime("%d"),time.strftime("%H"),time.strftime("%M"),time.strftime("%S")))
campo=Entry(Canvas2,textvariable=file_name_read_2).place(x=290,y=45)
# boton2=Button(Canvas2,text="Obtener datos", command=pacientes).place(x=150,y=125)
# boton2=Button(Canvas2,command=lambda:separarDatos(file_name_read_2.get(),campo2.get(),campo3.get()),text="Obtener datos").place(x=150,y=125)
boton2=Button(Canvas2,command=lambda:separarDatos(file_name_read_2.get()),text="Obtener datos").place(x=150,y=125)
etiqueta= Label(Canvas2,text="Introduce la longitud del tramo en metros:",font=("Calibri",12),fg="black").place(x=10,y=65)
distancia_predefinida=DoubleVar()
distancia_predefinida.set(30)
campo2 = Entry(Canvas2,textvariable=distancia_predefinida)
campo2.place(x=290,y=70)
etiqueta= Label(Canvas2,text="Introduce el tiempo en minutos:",font=("Calibri",12),fg="black").place(x=10,y=90)
tiempo_predefinido=DoubleVar()
tiempo_predefinido.set(6)
campo3=Entry(Canvas2,textvariable=tiempo_predefinido)
campo3.place(x=290,y=95)
#--------------------------------------------------------------------------------------------
###### Zona de consulta de historial ######
etiqueta= Label(Canvas3,text="CONSULTA DE HISTORIAL:",font=("Calibri",12),fg="black").place(x=10,y=10)
etiqueta= Label(Canvas3,text="Introduce la identificación del paciente:",font=("Calibri",12),fg="black").place(x=10,y=40)
campo4 = Entry(Canvas3,textvariable="")
campo4.place(x=290,y=45)
boton3=Button(Canvas3,text="Buscar",command=lambda:buscaHistorial(campo4.get())).place(x=150,y=75)
# boton3=Button(Canvas3,command=lambda:buscar(campo4.get()),text="Buscar").place(x=150,y=75)

ventana.mainloop()