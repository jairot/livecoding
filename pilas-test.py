from PyQt4.QtCore import *
from PyQt4.QtGui import *
import types

def debug_trace():
  '''Set a tracepoint in the Python debugger that works with Qt'''
  from PyQt4.QtCore import pyqtRemoveInputHook
  from ipdb import set_trace
  pyqtRemoveInputHook()
  set_trace()

import pilas


class Actor(pilas.actores.Actor):

    def __init__(self, x=0, y=0):
        pilas.actores.Actor.__init__(self, 'caja.png', x, y)

    def actualizar(self):
        self.escala = 1
        self.rotacion += 1


def actualizar_archivo(*k):
    #print "Actualizar !!!!!"
    try:
        m = __import__('antes')
        reload(m)
    except Exception, e:
        print e
    Actor.actualizar.im_func.func_code = m.Actor.actualizar.im_func.func_code

    # Verificando si hay metodos nuevos y los inyecta.
    atributos_actuales = set(dir(Actor))
    atributos_nuevos = set(dir(m.Actor))

    atributos_creados = atributos_nuevos - atributos_actuales

    if atributos_creados:
        #debug_trace()
        print "Hay cosas nuevas en la clase:", atributos_creados

        for attr in atributos_creados:
            setattr(Actor, attr, types.MethodType(getattr(m.Actor, attr).im_func, Actor))

    for attr in atributos_nuevos:
        attr_viejo = getattr(Actor, attr)

        if isinstance(attr_viejo, types.MethodType):
            attr_viejo.im_func.func_code = getattr(m.Actor, attr).im_func.func_code


    QTimer.singleShot(100, actualizar_archivo)

if __name__ == '__main__':
    pilas.iniciar()
    QTimer.singleShot(100, actualizar_archivo)
    actores = Actor() * 10

    pilas.ejecutar()
