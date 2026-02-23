import math
from worldview.LinearEquation import LinearEquation
from worldview.WPoint import WPoint
class Poligon:
    def __init__(self, x, y, h, a, w, c):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.a = a
        self.c = c
        theta = math.radians(self.a)
        self.equation = LinearEquation(theta, WPoint(self.x, self.y))

    def paint(self, w, wv):
        # Punt inicial i final 
        theta = math.radians(self.a)
        x1, y1 = self.x, self.y
        x2 = self.x + math.cos(theta)*self.h
        y2 = self.y + math.sin(theta)*self.h

        # Vector normal 
        px = -math.sin(theta)
        py = math.cos(theta)
        half = self.w / 2.0

        # Quatre vertexs del rectangle al món 
     
        corners = [
            (x1 + px * half, y1 + py * half), 
            (x2 + px * half, y2 + py * half), 
            (x2 - px * half, y2 - py * half), 
            (x1 - px * half, y1 - py * half),  
        ]

        # Convertir a coordenadas de vista
        v_coords = []
        for xx, yy in corners:
            vp = wv.worldToViewXY(xx, yy)
            v_coords.extend([vp.x, vp.y])

        w.create_polygon(*v_coords, fill=self.c)

   