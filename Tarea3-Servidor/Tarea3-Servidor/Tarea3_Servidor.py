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

cadena = ""
cadenaDecodi = ""
lista = []
ventana = tk.Tk()
TextoTexBox2 = tk.StringVar()
texBox2 = None

class CapaEnlaceDatos:
    def __init__(self):
        self.listaAux=[]
        self.listaRec =[]
        self.lenLis = 0
        self.banWhile = True
        self.PDUCapaRed = CapaRed()
        self.PDUCapaTransporte = CapaTransporte()
   

    def convertirOriginal(self,lista):
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
            obj2 = int(s, 2)
            self.listaAux[0] = obj1
            self.listaAux[1] = int(obj2)
            lista[j] = self.listaAux
        print("Capa Enlace")
        print(lista)
        self.PDUCapaTransporte.verificarllegada(lista,self.PDUCapaRed.hostCliente)

    def verificarError(self,lista):
        if self.lenLis > len(lista):
            messagebox.showinfo(message="Hubo un error con el mensaje recibido, pronto lo solucionaremos", title="Advertencia")
            for i in range(self.lenLis):
                band = False
                for j in lista:
                    obj2 = ''
                    s = j[1]
                    obj2 = int(s, 2)
                    if i == int(obj2):
                        band = True
                if band == False:
                    self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.c.connect((self.PDUCapaRed.hostCliente, self.PDUCapaTransporte.Puerto))
                    msg_rec = self.c.recv(1024)
                    banSYN = "E"+str(i)
                    self.c.send(banSYN.encode('ascii'))
                    self.c.close()
                    self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.c.bind(("", self.PDUCapaTransporte.Puerto))
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
                    self.convertirOriginal(lista)
                    break
        elif self.lenLis == len(lista):
               self.convertirOriginal(lista)
                

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
                self.PDUCapaRed.colocarIPs(str(addr[0]))
            elif pala[0] == "F":
                b = True
                l = ""
                for i in pala:
                    if i != "F":
                        l = l+i
                self.lenLis = int(l)
                sesion = True
                banWhile = False
            elif self.PDUCapaRed.hostCliente ==  str(addr[0]):
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
        self.verificarError(lista)

            

        
class CapaRed:
    def init(self):
        self.hostCliente = ""
        self.hostServidor = "25.101.246.19"

    def colocarIPs(self,ipcliente):
        self.hostCliente = ipcliente
class CapaTransporte:
    
    def __init__(self):
        self.n = ""
        self.id = 0
        self.lis = []
        self.Puerto = 44440

    

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
        capa.sesionFinalizada(cadena,ipcliente,self.Puerto)
    """def hola():Esta aqui por que despues vemos como lo llamamos
        #messagebox.showinfo(title="Envio", message= "El mensaje "+entry_var.get()+ " sera enviado" )
        transporte = CapaTransporte()
        transporte.multiplexar(entry_var.get())"""

class CapaSesion:
    def __init__(self):
        self.c=None
      
    def sesionFinalizada(self,cadena,ipcliente,puerto):
        band = True
        try:
            self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.c.connect((ipcliente, puerto))
            msg_rec = self.c.recv(1024)
            banSYN = "F"
            self.c.send(banSYN.encode('ascii'))
            capa = CapaPresentacion()
            capa.decodificor(cadena)
        except:
            messagebox.showerror(message="Error al cerrar sesion con el cliente", title="ERROR")

class CapaPresentacion:
    def __init__(self):
        cadena = ""
        cadenaDecodi = ""
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
        messagebox.showinfo(message="Mensaje recibido correctamente", title="Mensaje")
        readOnlyText = tk.Text(ventana)
        readOnlyText.insert(1.0,cadenaDecodi)
        readOnlyText.configure(state='disabled')
        readOnlyText.place(x=150, y=200,width=500,height=100)
        texBox1 = tk.Label(ventana,text="Click en INICIAR, para activar el servidor",bg = "RoyalBlue3", fg = "black")
        texBox1.place(x=295, y=100,width=210,height=30)
        ventana.update()

class CapaAplicacion():
    def __init__(self):
        self.men = ""
        
    
    def ServidorIniciado(self):
        if messagebox.askyesno(message="El servidor entrara en modo SERVIDOR ACTIVO ¿Desea continuar?", title="Advertencia"):
            cadena = ""
            cadenaDecodi = ""
            readOnlyText = tk.Text(ventana)
            readOnlyText.insert(1.0,"")
            readOnlyText.configure(state='disabled')
            readOnlyText.place(x=150, y=200,width=500,height=100)
            texBox1 = tk.Label(ventana,text="Modo SERVIDOR ACTIVO",bg = "RoyalBlue3", fg = "black")
            texBox1.place(x=295, y=100,width=210,height=30) 
            ventana.update()
            CapaEnlac = CapaEnlaceDatos()
            CapaEnlac.iniciarServidor();
   
    def GUI(self):
        ventana.title("Servidor")
        ventana.minsize(800,600)
        ventana.maxsize(800,600)

        ruta = os.getcwd()
        ruta1 = ruta.replace("\\", "\\\\")

        filename = tk.PhotoImage(file = ruta1+"\\\\fondo3.png")
        background_label = tk.Label(ventana,bg="blue",image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        texBox1 = tk.Label(ventana,text="Click en INICIAR, para activar el servidor",bg = "RoyalBlue3", fg = "black")
        texBox1.place(x=295, y=100,width=210,height=30) 
        
        readOnlyText = tk.Text(ventana)
        readOnlyText.insert(1.0,"")
        readOnlyText.configure(state='disabled')
        readOnlyText.place(x=150, y=200,width=500,height=100)

        Button = tk.Button(ventana, text="INICIAR", command=self.ServidorIniciado)
        Button.place(x=350, y=350,width=100,height=20)

        
        ventana.mainloop()
        

capaApli = CapaAplicacion()
capaApli.GUI()
