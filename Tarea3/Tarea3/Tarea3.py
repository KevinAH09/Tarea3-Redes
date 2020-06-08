import tkinter as tk
import socket
import os
import random
from tkinter import messagebox
Acodi="Ø" 
Bcodi="Ω"
Ccodi = "Σ"
Dcodi="ø"
Ecodi="º"
Fcodi="◊"
Gcodi="¬"
Hcodi="«"
Icodi="»"

Jcodi="▓"
Kcodi="┤"
Lcodi ="╣"
Mcodi="╝"
Ncodi="¥"
Ñcodi="┴"
Ocodi="ð"
Pcodi="Þ"
Qcodi="≡"
Rcodi="±"
Scodi="¶"
Tcodi="§"
Ucodi="$"
Vcodi="%"
Wcodi="^"
Xcodi="&"
Ycodi="Æ"
Zcodi="₫"
PUNTOcodi = "■"
ESPACIOcodi="_"
COMAcodi = "*"

UNOcodi = "☏"
DOScodi = "☆"
TREScodi = "★"
CUATROcodi = "▽"
CINCOcodi = "△"
SEIScodi = "♡"
SIETEcodi = "∵"
OCHOcodi = "∴"
NUEVEcodi = "∷"
CEROcodi = "♤"

cadena = ""
cadenaDecodi = ""
lista = []

class CapaEnlaceDatos:
    def init(self):
        self.listaAux=[]

    def escucharServidor(self,lista,host,puerto):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", puerto))
        s.listen(5)
        ban=True
        while ban:
            (c, addr) = s.accept()
            print("Se establecio conexion con %s" % str(addr))
            msg = 'Conexion establecida con : %s' % socket.gethostname + "\r\n"
            c.send(msg.encode('utf8'))
            msg_rec =c.recv(1024)
            pala = msg_rec.decode('ascii')
            if pala == "F":
                print(pala)
                c.close()
                ban=False
            else:
                band = True
                cadena = ""
                for i in pala:
                    if i == "E" and band:
                        print("Error")
                        band=False
                    elif band == False:
                        cadena = cadena + i
                self.listaAux=lista[int(cadena)]
                c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                c.connect((host, puerto))
                msg_rec = c.recv(1024)
                trama = self.listaAux[0]+","+self.listaAux[1]
                c.send(trama.encode('ascii'))
                messagebox.showinfo(message="Mensaje con error pero solucionado correctamente", title="MENSAJE EXITOSO")
                c.close()

                
                    
           
      
    def EnviarDatos(self,lista,c,host,puerto):
        band = True
        a = random.randint(1,2)
        print(a)
        if a == 1: 
            for i in lista:
                c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                c.connect((host, puerto))
                msg_rec = c.recv(1024)
                trama = i[0]+","+i[1]
                c.send(trama.encode('ascii'))
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c.connect((host, puerto))
            msg_rec = c.recv(1024)
            m="F"+str(len(lista))
            c.send(m.encode('ascii'))
            messagebox.showinfo(message="Mensaje enviado correctamente", title="MENSAJE EXITOSO")
        else:
            obj1 = ''
            a = random.randint(0,len(lista)-1)
            for i in lista:
                n = i[1]
                obj1=int(n,2)
                if int(obj1) != a:
                    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    c.connect((host, puerto))
                    msg_rec = c.recv(1024)
                    trama = i[0]+","+i[1]
                    c.send(trama.encode('ascii'))
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c.connect((host, puerto))
            msg_rec = c.recv(1024)
            m="F"+str(len(lista))
            c.send(m.encode('ascii'))
        self.escucharServidor(lista,host,puerto)

    def convertriBinario(self,lista,c,host,puerto):
        
        for i in range(len(lista)):
            
            self.listaAux = lista[i]
            obj1 = format(ord(self.listaAux[0]), 'b')
            obj2 = format((self.listaAux[1]), 'b')
            self.listaAux[0] = obj1
            self.listaAux[1] = obj2
            lista[i] = self.listaAux
        self.EnviarDatos(lista,c,host,puerto)



    def convertirOriginal(self,lista):
        obj1=''
        obj2 =''
        for j in range(len(lista)):
            self.listaAux = lista[j]
            s = self.listaAux[0]
            w = len(self.listaAux[0])
            for i in range(len(s)//w):
                obj1 = chr(int(s[i*w:i*w+w], 2))
            s = self.listaAux[1]
            w = len(self.listaAux[1])
            for i in range(len(s)//w):
                obj2 = chr(int(s[i*w:i*w+w], 2))

            self.listaAux[0] = obj1
            self.listaAux[1] = int(obj2)
            lista[j] = self.listaAux 

    
class CapaRed:
     def __init__(self):
        self.HostDestino = "25.101.246.19"
        self.HostOrigen = "25.102.7.239"
        
class CapaTransporte:
    
    def __init__(self):
        self.n = ""
        self.id = 0
        self.lis = []
        self.Puerto = 44440

    def multiplexar(self,cadena,c,hotsDestino,puerto):
        lista=[]
        self.lis=[]
        self.id=0
        self.n=""
        cont = 0
        for u in cadena:
            self.lis = []
            self.n=u
            self.id=cont
            self.lis.append(u)
            self.lis.append(cont)
            lista.append(self.lis)
            cont=cont+1
        capaEnlace = CapaEnlaceDatos()
        capaEnlace.convertriBinario(lista,c,hotsDestino,puerto)


class CapaSesion:
    def __init__(self):
        self.c=None
    def sesionIniciada(self,cadena):
        PDURed = CapaRed()
        PDUTransprote = CapaTransporte()
        band = True
        try:
            self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.c.connect((PDURed.HostDestino,PDUTransprote.Puerto))
            msg_rec = self.c.recv(1024)
            banSYN = "S"
            self.c.send(banSYN.encode('ascii'))
        except:
            messagebox.showerror(message="No se puede conectar con el servidor", title="ERROR DE CONEXION")
            band = False
        if band:
            messagebox.showinfo(message="Conexion extablecida correctamente", title="CONEXION EXITOSA")
            PDUTransprote.multiplexar(cadena,self.c,PDURed.HostDestino, PDUTransprote.Puerto)
        

class CapaPresentacion:
    def __init__(self):
        cadena = ""
        cadenaDecodi = ""
    def codificar(self,mensaje):
        global cadena
        cadena = ""
        for i in mensaje:
            if i == "A":
                cadena = cadena + Acodi
            elif i == "B":
                cadena = cadena + Bcodi
            elif i == "C":
                cadena = cadena + Ccodi
            elif i == "D":
                cadena = cadena + Dcodi
            elif i == "E":
                cadena = cadena + Ecodi
            elif i == "F":
                cadena = cadena + Fcodi
            elif i == "G":
                cadena = cadena + Gcodi
            elif i == "H":
                cadena = cadena + Hcodi
            elif i == "I":
                cadena = cadena + Icodi
            elif i == "J":
                cadena = cadena + Jcodi
            elif i == "K":
                cadena = cadena + Kcodi
            elif i == "L":
                cadena = cadena + Lcodi
            elif i == "M":
                cadena = cadena + Mcodi
            elif i == "N":
                cadena = cadena + Ncodi
            elif i == "O":
                cadena = cadena + Ocodi
            elif i == "P":
                cadena = cadena + Pcodi
            elif i == "Q":
                cadena = cadena + Qcodi
            elif i == "R":
                cadena = cadena + Rcodi
            elif i == "S":
                cadena = cadena + Scodi
            elif i == "T":
                cadena = cadena + Tcodi
            elif i == "U":
                cadena = cadena + Ucodi
            elif i == "V":
                cadena = cadena + Vcodi
            elif i == "W":
                cadena = cadena + Wcodi
            elif i == "X":
                cadena = cadena + Xcodi
            elif i == "Y":
                cadena = cadena + Ycodi
            elif i == "Z":
                cadena = cadena + Zcodi
            elif i == "1":
                cadena = cadena + UNOcodi
            elif i == "2":
                cadena = cadena + DOScodi
            elif i == "3":
                cadena = cadena + TREScodi
            elif i == "4":
                cadena = cadena + CUATROcodi
            elif i == "5":
                cadena = cadena + CINCOcodi
            elif i == "6":
                cadena = cadena + SEIScodi
            elif i == "7":
                cadena = cadena + SIETEcodi
            elif i == "8":
                cadena = cadena + OCHOcodi
            elif i == "9":
                cadena = cadena + NUEVEcodi
            elif i == "0":
                cadena = cadena + CEROcodi
            elif i == ".":
                cadena = cadena + PUNTOcodi
            elif i == ",":
                cadena = cadena + COMAcodi
            elif i == " ":
                cadena = cadena + ESPACIOcodi
            else:
                cadena = cadena + i;
        capaS = CapaSesion()
        capaS.sesionIniciada(cadena)
        

class CapaAplicacion():
    def __init__(self):
        self.men = ""
        self.ventana = tk.Tk()
        self.entry_var = tk.StringVar()

    def EnvioMensaje(self):
        self.men = self.entry_var.get()
        codi = CapaPresentacion()
        c=codi.codificar(self.men.upper())
   
    def GUI(self):
        self.ventana.title("Cliente")
        self.ventana.minsize(800,600)
        self.ventana.maxsize(800,600)

        ruta = os.getcwd()
        ruta1 = ruta.replace("\\", "\\\\")

        filename = tk.PhotoImage(file = ruta1+"\\\\fondo3.png")
        background_label = tk.Label(self.ventana,bg="blue",image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        texBox1 = tk.Label(self.ventana,text="Ingrese el mensaje",bg = "RoyalBlue3", fg = "black")
        texBox1.place(x=350, y=150,width=100,height=30)

        entry = tk.Entry(self.ventana,textvariable = self.entry_var)
        entry.place(x=150, y=300,width=500,height=20)

        Button = tk.Button(self.ventana, text="ENVIAR", command=self.EnvioMensaje)
        Button.place(x=350, y=350,width=100,height=20)
        self.ventana.mainloop()

capaApli = CapaAplicacion()
capaApli.GUI()

