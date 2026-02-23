import json
from  Cotxe import *
from Tram import *


class Fichero_json:
    def __init__(self,nombre_fichero):
        self.nombre_fichero=nombre_fichero
    def lectura_json(self):
        f=open(self.nombre_fichero,"r")
        dades=json.load(f)
        f.close()
        cotxes=[]
        trams=[]
        
        for t in dades['sections']:
            t1=Tram(t['position']['x'],t['position']['y'],t['direction']['x'],t['direction']['y'],t['distance'],t['angle'])
            trams.append(t1)
        
        for c in dades['cars']:
            c1=Cotxe(c['start_position']['x'],c['start_position']['y'],c['direction']['x'],c['width'],c['height'],c['angle'],c['color'])
            cotxes.append(c1)
      
            
        return cotxes, trams