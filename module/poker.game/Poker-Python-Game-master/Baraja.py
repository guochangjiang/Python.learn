from Carta import Carta
class Baraja(Carta):
    def __init__(self):
        self.lista=[]
        self.inicializacion()
        self.mezclar()
    def inicializacion(self):
        for tipo in["trebol","pica","corazon","diamante"]:
            for nivel in range(2,15):
                self.lista.append(Carta(nivel,tipo,"cartas02/"+str(nivel)+str(tipo[:1])+".gif"))
        return self.lista
    def mezclar(self):
        from random import shuffle
        shuffle(self.lista)
        shuffle(self.lista)
        return self.lista
    def RepartirCarta(self):
        return self.lista.pop()

    




