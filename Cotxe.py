import math
from Tram import *
import keyboard
from worldview.WPoint import WPoint
from worldview.LinearEquation import LinearEquation

class Cotxe(Poligon):
    def __init__(self, x, y, sentido,w, h, a,c,v=8):
        super().__init__(x, y, h, a, w,c)
        self.v=v
        self.sentido = sentido
        self.theta = math.radians(self.a)
        self.equation = LinearEquation(self.theta, WPoint(self.x, self.y))
        self.tram = None
        if self.sentido == -1:
            self.a = (self.a + 180) % 360
            self.theta = math.radians(self.a)
       
    def asignar_tram(self, tram):
      self.tram = tram
      self.a = tram.a
      self.theta = math.radians(tram.a)
      if self.sentido == -1:
        self.a = (tram.a + 180) % 360
        self.theta = math.radians(self.a)
     
      self.equation = tram.equation
     
    def se_sale(self, margen=5):
        # Vector desde el inicio del tram hasta el coche
        dx = self.x - self.tram.x
        dy = self.y - self.tram.y
        
        # Vector perpendicular unitario a la dirección del tram
        px = -math.sin(math.radians(self.tram.a))
        py = math.cos(math.radians(self.tram.a))
        
       
        producto_escalar = abs(dx * px + dy * py)
        
        umbral_lateral = (self.tram.w / 2.0) + (self.w / 2.0) + margen
           #se para
        if producto_escalar > umbral_lateral:
            self.x = self.x - self.v * math.cos(self.theta)
            self.y = self.y - self.v * math.sin(self.theta)
    
          
    def actualizar_tram(self, trams):
       # si ya tiene un tramoy todavia no ha salido seguir dentro de el
        if self.tram is not None:
            #vector inicio del tram
            dx = self.x - self.tram.x
            dy = self.y - self.tram.y
            productoEscalar =(dx * math.cos(self.theta) + dy * math.sin(self.theta))* self.sentido
            margen = 10
            
            if -margen <= productoEscalar <= self.tram.h + margen:
                return
        # Buscar el tram más cercano
   
        min_distancia = float('inf')
        tram_mas_cercano = None
        
        for tram in trams:
            if self.sentido == -1:
            # Calcular punto final del tramo
                end_x = tram.x + tram.h * math.cos(math.radians(tram.a))
                end_y = tram.y + tram.h * math.sin(math.radians(tram.a))
                distancia = WPoint.distance(WPoint(self.x, self.y), WPoint(end_x, end_y))
            else:
                distancia = WPoint.distance(WPoint(self.x, self.y), WPoint(tram.x, tram.y))

            
            if distancia < min_distancia:
                min_distancia = distancia
                tram_mas_cercano = tram
        
       
        if min_distancia < 80:  
            if self.tram != tram_mas_cercano:
                self.asignar_tram(tram_mas_cercano)
               
   
    def mou(self):

        self.x = self.x + self.v * math.cos(self.theta)
        self.y = self.y + self.v * math.sin(self.theta)
    
    def detectar_choque(self, cotxes):
        
        distancia_colision=self.w
        
        for c in cotxes:
            if c is self:  # no colisionar consigo mismo
                continue
            
            distancia = WPoint.distance(WPoint(self.x, self.y), WPoint(c.x, c.y))
           
            
            # Si la distancia es menor que la distancia de colisión, hay choque
            if distancia < distancia_colision:
               
                if self.sentido != c.sentido:
                    #los dos coches tienen que parar
                    self.x = self.x - self.v * math.cos(self.theta)
                    self.y = self.y - self.v * math.sin(self.theta)
                    c.x = c.x - c.v * math.cos(c.theta)
                    c.y = c.y - c.v * math.sin(c.theta)
                   
                elif self.sentido == c.sentido:
                    #uno va para alante y otro para atras
                    self.x = self.x + 2*self.v * math.cos(self.theta)
                    self.y = self.y + 2*self.v * math.sin(self.theta)
                    c.x = c.x - 2*c.v * math.cos(c.theta)
                    c.y = c.y - 2*c.v * math.sin(c.theta)
    
     
    def pinta(self, w, wv):
        super().paint(w, wv)
        
       #linea dlantera
        x2 = self.x + math.cos(self.theta)*0.75*self.h    
        y2 = self.y + math.sin(self.theta)*0.75*self.h

        # vector normal 
        px = -math.sin(self.theta)
        py = math.cos(self.theta)
        half = self.w / 2.0
        
       
        # Dos puntos para la línea delantera en los extremos del frente del coche
        corners = [
            (x2 + px * half, y2 + py * half), 
            (x2 - px * half, y2 - py * half), 
        ]

        v_coords = []
        for xx, yy in corners:
            vp = wv.worldToViewXY(xx, yy)
            v_coords.extend([vp.x, vp.y])

       
        w.create_line(*v_coords, fill="black", width=2)
        
    def controles_teclat(self):#control intuitivo primera persona
        try:
            desplazamiento  = 10
            if keyboard.is_pressed("up arrow"):
                    # Avanzar en la dirección del coche
                self.x += desplazamiento * math.cos(self.theta)
                self.y += desplazamiento * math.sin(self.theta)

            if keyboard.is_pressed("down arrow"):
                    # Retroceder
                self.x -= desplazamiento* math.cos(self.theta)
                self.y -= desplazamiento* math.sin(self.theta)
            if keyboard.is_pressed("right arrow"):
                  
                self.x += desplazamiento* math.sin(self.theta)
                self.y -= desplazamiento* math.cos(self.theta)
            if keyboard.is_pressed("left arrow"):
                   
                self.x -= desplazamiento * math.sin(self.theta)
                self.y += desplazamiento* math.cos(self.theta)
        except:
            pass #esto pasa por linux
    
    def controles_teclat1(self):# control respetando direcciones y sentidos
        try:
            desplazamiento  = 10
            if self.a % 90 == 0:#0,90,180,270
              
                if keyboard.is_pressed("down arrow"):
                    self.y -= desplazamiento
                if keyboard.is_pressed("up arrow"):
                    self.y += desplazamiento
                if keyboard.is_pressed("right arrow"):
                    self.x += desplazamiento
                if keyboard.is_pressed("left arrow"):
                    self.x -= desplazamiento
                    

            elif self.a >90:  
                if keyboard.is_pressed("up arrow"):
                    # Avanzar en la dirección del coche
                    self.x += desplazamiento * math.cos(self.theta)
                    self.y += desplazamiento * math.sin(self.theta)
                if keyboard.is_pressed("down arrow"):
                    # Retroceder
                    self.x -= desplazamiento* math.cos(self.theta)
                    self.y -= desplazamiento* math.sin(self.theta)
                if keyboard.is_pressed("right arrow"):
                 
                    self.x += desplazamiento* math.sin(self.theta)
                    self.y -= desplazamiento* math.cos(self.theta)
                if keyboard.is_pressed("left arrow"):
                  
                    self.x -= desplazamiento * math.sin(self.theta)
                    self.y += desplazamiento* math.cos(self.theta)
            elif self.a < 270:
               
                if keyboard.is_pressed("up arrow"):
                    # Avanzar en la dirección del coche
                    self.x -= desplazamiento* math.sin(self.theta)
                    self.y -= desplazamiento* math.cos(self.theta)
                  
                if keyboard.is_pressed("down arrow"):
                    # Retroceder
                    self.x += desplazamiento * math.sin(self.theta)
                    self.y += desplazamiento* math.cos(self.theta)
                if keyboard.is_pressed("right arrow"):
                   
                    self.x -= desplazamiento* math.cos(self.theta)
                    self.y += desplazamiento * math.sin(self.theta)
                  
                if keyboard.is_pressed("left arrow"):
                  
                    self.x += desplazamiento * math.cos(self.theta)
                    self.y -= desplazamiento* math.sin(self.theta)
            else:   
                if keyboard.is_pressed("up arrow"):
                    # Avanzar en la dirección del coche
                   self.x += desplazamiento * math.sin(self.theta)
                   self.y += desplazamiento * math.cos(self.theta)
                  
                if keyboard.is_pressed("down arrow"):
                    # Retroceder
                    self.x -= desplazamiento * math.sin(self.theta)
                    self.y -= desplazamiento* math.cos(self.theta)
                    
                if keyboard.is_pressed("right arrow"):
                  
                    self.x += desplazamiento* math.cos(self.theta)
                    self.y -= desplazamiento * math.sin(self.theta)
                  
                if keyboard.is_pressed("left arrow"):
                   
                    self.x -= desplazamiento* math.cos(self.theta)
                    self.y += desplazamiento* math.sin(self.theta)          
        except:
            pass  
    def controles_teclat2(self):# control simple
        try:
            desplazamiento  = 10
            
            if keyboard.is_pressed("down arrow"):
                self.y -= desplazamiento
            if keyboard.is_pressed("up arrow"):
                self.y += desplazamiento
            if keyboard.is_pressed("right arrow"):
                self.x += desplazamiento
            if keyboard.is_pressed("left arrow"):
                self.x -= desplazamiento
        except:
            pass 