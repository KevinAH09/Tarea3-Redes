import tkinter as tk
import socket
import os
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

Host = "25.102.7.239"
Puerto = 44440
cadena = ""
cadenaDecodi = ""
lista = []
ventana = tk.Tk()
TextoTexBox2 = tk.StringVar()
texBox2 = None

class CapaEnlaceDatos:
    def init(self):
        self.listaAux=[]
        self.listaRec =[]
        self.lenLis = 0
        self.banWhile = True
        self.clienteIPSesion = ""
    def convertriBinario(self,lista):
        for i in range(len(lista)):
            self.listaAux = lista[i]
            obj1 = format(ord(self.listaAux[0]), 'b')
            obj2 = format(ord(str(self.listaAux[1])), 'b')
            self.listaAux[0] = obj1
            self.listaAux[1] = obj2
            lista[i] = self.listaAux 
        
        print(lista)
        return lista

    def convertirOriginal(self,lista,ipcliente):
        print(lista)
        obj1=''
        obj2 =''
        for j in range(len(lista)):#((h,1
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
        print("Capa Enlace")
        print(lista)
        capa = CapaTransporte()
        capa.verificarllegada(lista,ipcliente)
    def verificarError(self,lista,ipcliente):
        if self.lenLis > len(lista):
           
            for i in range(self.lenLis):
                band = False
                for j in lista:
                    obj2 = ''
                    s = j[1]
                    for n in range(len(s)//len(s)):
                        obj2 = chr(int(s[n*len(s):n*len(s)+len(s)], 2))
                    if i == int(obj2):
                        band = True
                if band == False:
                    print(ipcliente)
                    self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.c.connect((ipcliente, Puerto))
                    msg_rec = self.c.recv(1024)
                    banSYN = "E"+str(i)
                    self.c.send(banSYN.encode('ascii'))
                    self.c.close()
                    self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.c.bind(("", Puerto))
                    self.c.listen(1000)
                    (c, addr) =  self.c.accept()
                    print("Se establecio conexion con %s" % str(addr))
                    msg = 'Conexion establecida con : %s' % socket.gethostname + "\r\n"
                    c.send(msg.encode('utf8'))
                    msg_rec =c.recv(1024)
                    pala = msg_rec.decode('ascii')
                    l =""
                    n =""
                    b = True
                    for i in pala:
                        if i == ",":
                            b = False
                        elif b:
                            l = l+i
                        else:
                            n = n+i
                    print(lista)
                    lista.append([l,n])
                    print(lista)
                    self.c.close()
                    self.convertirOriginal(lista,ipcliente)
                    break
        elif self.lenLis == len(lista):
               self.convertirOriginal(lista,ipcliente)
                

    def iniciarServidor(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 44440))
        s.listen(1000)
        sesion = True
        clienteIPSesion= ""
        Lista = []
        lista = []
        banWhile = True
        while banWhile == True:
            (c, addr) = s.accept()
            print("Se establecio conexion con %s" % str(addr))
            msg = 'Conexion establecida con : %s' % socket.gethostname + "\r\n"
            c.send(msg.encode('utf8'))
            msg_rec =c.recv(1024)
            pala = msg_rec.decode('ascii')
            if (pala == "S" and sesion == True):
                sesion = False
                clienteIPSesion = str(addr[0])
            elif pala[0] == "F":
                b = True
                l = ""
                for i in pala:
                    if i != "F":
                        l = l+i
                self.lenLis = int(l)
                sesion = True
                banWhile = False
            elif clienteIPSesion ==  str(addr[0]):
                l =""
                n =""
                b = True
                for i in pala:
                    if i == ",":
                        b = False
                    elif b:
                        l = l+i
                    else:
                        n = n+i

                lista.append([l,n])
                print(lista)
        s.close()
        self.verificarError(lista,clienteIPSesion)

            

        
class CapaRed:
     def init(self):
        self.c = ""
class CapaTransporte:
    
    def init(self):
        self.n = ""
        self.id = 0
        self.lis = []

    def multiplexar(self,cadena):

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
        l= capaEnlace.convertriBinario(lista)
        capaEnlace.convertirOriginal(l)

    def verificarllegada(self,lista,ipcliente):
        listaAux=[]
        cadena = ""
        for i in range(len(lista)):#((h,1),(o,2))
            for aux in range(len(lista)):
                obj1=lista[aux]
                if i == int(obj1[1]):
                    obj2=lista[aux]
                    listaAux.append(obj2[0])
        
        for j  in listaAux:
            cadena = cadena + j
        print(cadena)
        capa = CapaSesion()
        capa.sesionFinalizada(cadena,ipcliente)
    """def hola():Esta aqui por que despues vemos como lo llamamos
        #messagebox.showinfo(title="Envio", message= "El mensaje "+entry_var.get()+ " sera enviado" )
        transporte = CapaTransporte()
        transporte.multiplexar(entry_var.get())"""

class CapaSesion:
    def __init__(self):
        self.c=None
    def sesionIniciada(self,cadena):
        band = True
        try:
            self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.c.connect((Host, Puerto))
            msg_rec = self.c.recv(1024)
            banSYN = "S"
            self.c.send(banSYN.encode('ascii'))
        except:
            messagebox.showerror(message="No se puede conectar con el servidor", title="ERROR DE CONEXION")
            band = False
        if band:
            messagebox.showinfo(message="Conexion extablecida correctamente", title="CONEXION EXITOSA")
            transporte = CapaTransporte()
            transporte.multiplexar(cadena)
        
    def sesionFinalizada(self,cadena,ipcliente):
        band = True
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.c.connect((ipcliente, Puerto))
        msg_rec = self.c.recv(1024)
        banSYN = "F"
        self.c.send(banSYN.encode('ascii'))
        
        capa = CapaPresentacion()
        capa.decodificor(cadena)

class CapaPresentacion:
    def __init__(self):
        cadena = ""
        cadenaDecodi = ""
    def codificar(self,mensaje):
        global cadena
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
        print(cadena)
        capaS = CapaSesion()
        capaS.sesionIniciada(cadena)
        

    def decodificor(self,mensaje):
        global cadenaDecodi
        cadenaDecodi = ""
        for i in mensaje:
            if i == Acodi:
                cadenaDecodi = cadenaDecodi + "A"
            elif i == Bcodi:
                cadenaDecodi = cadenaDecodi + "B"
            elif i == Ccodi:
                cadenaDecodi = cadenaDecodi + "C"
            elif i == Dcodi:
                cadenaDecodi = cadenaDecodi + "D"
            elif i == Ecodi:
                cadenaDecodi = cadenaDecodi + "E"
            elif i == Fcodi:
                cadenaDecodi = cadenaDecodi + "F"
            elif i == Gcodi:
                cadenaDecodi = cadenaDecodi + "G"
            elif i == Hcodi:
                cadenaDecodi = cadenaDecodi + "H"
            elif i == Icodi:
                cadenaDecodi = cadenaDecodi + "I"
            elif i == Jcodi:
                cadenaDecodi = cadenaDecodi + "J"
            elif i == Kcodi:
                cadenaDecodi = cadenaDecodi + "K"
            elif i == Lcodi:
                cadenaDecodi = cadenaDecodi + "L"
            elif i == Mcodi:
                cadenaDecodi = cadenaDecodi + "M"
            elif i == Ncodi:
                cadenaDecodi = cadenaDecodi + "N"
            elif i == Ocodi:
                cadenaDecodi = cadenaDecodi + "O"
            elif i == Pcodi:
                cadenaDecodi = cadenaDecodi + "P"
            elif i == Qcodi:
                cadenaDecodi = cadenaDecodi + "Q"
            elif i == Rcodi:
                cadenaDecodi = cadenaDecodi + "R"
            elif i == Scodi:
                cadenaDecodi = cadenaDecodi + "S"
            elif i == Tcodi:
                cadenaDecodi = cadenaDecodi + "T"
            elif i == Ucodi:
                cadenaDecodi = cadenaDecodi + "U"
            elif i == Vcodi:
                cadenaDecodi = cadenaDecodi + "V"
            elif i == Wcodi:
                cadenaDecodi = cadenaDecodi + "W"
            elif i == Xcodi:
                cadenaDecodi = cadenaDecodi + "X"
            elif i == Ycodi:
                cadenaDecodi = cadenaDecodi + "Y"
            elif i == Zcodi:
                cadenaDecodi = cadenaDecodi + "Z"
            elif i == UNOcodi:
                cadenaDecodi = cadenaDecodi + "1"
            elif i == DOScodi:
                cadenaDecodi = cadenaDecodi + "2"
            elif i == TREScodi:
                cadenaDecodi = cadenaDecodi + "3"
            elif i == CUATROcodi:
                cadenaDecodi = cadenaDecodi + "4"
            elif i == CINCOcodi:
                cadenaDecodi = cadenaDecodi + "5"
            elif i == SEIScodi:
                cadenaDecodi = cadenaDecodi + "6"
            elif i == SIETEcodi:
                cadenaDecodi = cadenaDecodi + "7"
            elif i == OCHOcodi:
                cadenaDecodi = cadenaDecodi + "8"
            elif i == NUEVEcodi:
                cadenaDecodi = cadenaDecodi + "9"
            elif i == CEROcodi:
                cadenaDecodi = cadenaDecodi + "0"
            elif i == PUNTOcodi:
                cadenaDecodi = cadenaDecodi + "."
            elif i == COMAcodi:
                cadenaDecodi = cadenaDecodi + ","
            elif i == ESPACIOcodi:
                cadenaDecodi = cadenaDecodi + " "
            else:
                cadenaDecodi = cadenaDecodi + i;
        print(cadenaDecodi)
        texBox2 = tk.Label(ventana,text=cadenaDecodi,bg = "RoyalBlue3", fg = "black")
        texBox2.place(x=350, y=250,width=100,height=30)
        ventana.update()

class CapaAplicacion():
    def __init__(self):
        self.men = ""
        

    def ServidorIniciado(self):
        cadena = ""
        cadenaDecodi = ""
        texBox2 = tk.Label(ventana,text=" ",bg = "RoyalBlue3", fg = "black")
        texBox2.place(x=350, y=250,width=100,height=30)
        ventana.update()
        CapaEnlac = CapaEnlaceDatos()
        CapaEnlac.iniciarServidor();
   
    def GUI(self):
        ventana.title("Cliente")
        ventana.minsize(800,600)
        ventana.maxsize(800,600)

        ruta = os.getcwd()
        ruta1 = ruta.replace("\\", "\\\\")

        filename = tk.PhotoImage(file = ruta1+"\\\\fondo3.png")
        background_label = tk.Label(ventana,bg="blue",image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        texBox1 = tk.Label(ventana,text="Menseje a Recibir",bg = "RoyalBlue3", fg = "black")
        texBox1.place(x=350, y=150,width=100,height=30)

        texBox2 = tk.Label(ventana,text="sdfsd",bg = "RoyalBlue3", fg = "black")
        texBox2.place(x=350, y=250,width=100,height=30)
        

        Button = tk.Button(ventana, text="INICIAR", command=self.ServidorIniciado)
        Button.place(x=350, y=350,width=100,height=20)
        ventana.mainloop()


capaApli = CapaAplicacion()
capaApli.GUI()
