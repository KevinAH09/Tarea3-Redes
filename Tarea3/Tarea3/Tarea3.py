import tkinter as tk
import os
from tkinter import messagebox




ventana = tk.Tk()
entry_var = tk.StringVar()



def hola():
    messagebox.showinfo(title="Envio", message= "El mensaje"+entry_var+ "sera enviado" )

ventana.title("Cliente")
ventana.minsize(800,600)
ventana.maxsize(800,600)

ruta = os.getcwd()
ruta1 = ruta.replace("\\", "\\\\")


filename = tk.PhotoImage(file = ruta1+"\\\\fondo3.png")
background_label = tk.Label(ventana,bg="blue",image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


texBox1 = tk.Label(ventana,text="Ingrese el mensaje",bg = "RoyalBlue3", fg = "black")
texBox1.place(x=350, y=150,width=100,height=30)

entry = tk.Entry(ventana,textvariable = entry_var)
entry.place(x=150, y=300,width=500,height=20)

Button = tk.Button(ventana, text="ENVIAR", command=hola)
Button.place(x=350, y=350,width=100,height=20)


ventana.mainloop()
