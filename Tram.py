import math
from worldview.LinearEquation import LinearEquation
from worldview.WPoint import WPoint
from Poligon import Poligon


class Tram(Poligon):
    def __init__(self, x, y, dirx, diry, h, a, w=60):
        super().__init__(x, y, h, a, w, "gray")
        self.dirx = dirx
        self.diry = diry
        self.theta = math.radians(self.a)
        self.equation = LinearEquation(self.theta, WPoint(self.x, self.y))

    def pinta(self, w, wv):
        super().paint(w, wv)
        x1, y1 = self.x, self.y
        x2 = self.x + math.cos(self.theta)*self.h
        y2 = self.y + math.sin(self.theta)*self.h
        # Dibujar la linea central
        
        x1v = wv.worldToViewXY(x1, y1)
        x2v = wv.worldToViewXY(x2, y2)
        w.create_line(x1v.x, x1v.y, x2v.x, x2v.y, fill="white", width=2, dash=(10, 10))