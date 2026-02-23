from tkinter import *
import time
import json
import keyboard
import math
from Cotxe import *
from Fichero_json import *
from Tram import *
from worldview.VPoint import *
from worldview.WPoint import *
from worldview.WorldView import *
from Poligon import *

# Estados: 0=menu, 1=jugando, -1=terminar
estado = 0

def iniciar_juego():
    global estado
    estado = 1
    btn_jugar.config(state=DISABLED)

def terminar_juego():
    global estado
    estado = -1

tk=Tk()
tk.title("Matecar")

w=Canvas(tk, width=800, height=600, background="lightgreen")
w.pack()
btn_terminar = Button(tk, text="TERMINAR", command=terminar_juego, bg="red",fg="white", width=15, height=2  )
btn_terminar.pack(side=BOTTOM)
btn_jugar = Button(tk, text="JUGAR", command=iniciar_juego, bg="green", fg="white", width=15, height=2)
btn_jugar.pack(side=BOTTOM, padx=5, pady=5)



wv=WorldView(WPoint(0,0),WPoint(1000,1000*6/8),VPoint(0,0),VPoint(800,600))
fichero=Fichero_json("carretera.json")
cotxes, trams = fichero.lectura_json()

# Asignar trams iniciales a cada coche
for c in cotxes:
    c.actualizar_tram(trams)



while estado != -1:
    w.delete("all")

    if estado == 1:
        # Centro 
        centro_x = (wv.wMin.x + wv.wMax.x) / 2
        centro_y = (wv.wMin.y + wv.wMax.y) / 2
        
        dx = cotxes[0].x - centro_x
        dy = cotxes[0].y - centro_y

        # Centrar
        wv.translateWindow(dx, dy)
        
        cotxes[0].se_sale()
        Cotxe.controles_teclat(cotxes[0])

        
        for t in trams:
            t.pinta(w, wv)
        
       
        for c in cotxes:
           
            c.actualizar_tram(trams)
           
            c.detectar_choque(cotxes)
           
            c.mou()
            
            c.pinta(w, wv)
     
    else:
        w.create_text(400, 300, text="Bienvenidos a Matecar", font=("Arial", 20, "bold"), fill="black")
    
    w.update()
    time.sleep(50/1000)  # 50ms de pausa

tk.quit()

