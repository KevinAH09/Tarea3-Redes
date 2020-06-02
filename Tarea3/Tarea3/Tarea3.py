import tkinter as tk
import os





ventana = tk.Tk()
entry_var = tk.StringVar()



def hola():
    print(entry_var.get())




ventana.title("Cliente")
ventana.minsize(800,600)
ventana.maxsize(800,600)

ruta = os.getcwd()
ruta1 = ruta.replace("\\", "\\\\")

filename = tk.PhotoImage(file = ruta1+"\\\\fondo4.png")
filename.zoom(1,1)
background_label = tk.Label(ventana,image=filename,bg="dodger blue")
background_label.place(x=0, y=0, relwidth=1, relheight=1)

texBox1 = tk.Label(ventana,text="Ingrese el Mensaje",bg = "blue", fg = "white")
texBox1.place(x=50, y=10)
entry = tk.Entry(ventana,textvariable = entry_var)
entry.place(x=50, y=50)


Button = tk.Button(ventana, text="Clícame", command=hola)
Button.place(x=50, y=100)



ventana.mainloop()
