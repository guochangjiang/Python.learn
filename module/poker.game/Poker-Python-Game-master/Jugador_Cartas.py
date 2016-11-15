from Pokar import Pokar
class Jugador_Cartas(Pokar):
    def __init__(self):
        self.jugador=Jugador
    
    def ordenarcartas(self,lista):
        lista.sort(key = lambda x: x.nivel)
        return lista
    def tipojugadas(self,lista):
        Pokar.__init__(self,lista)
        nivel=1
        nom="Carta Alta"
        if self.escalera(3):
            nom="Escalera real"
            nivel=10
        elif self.escalera(2):
            nom="Escalera de color"
            nivel=9
        elif self.parejasotrioypokar(4):
            nom="Pokar"
            nivel=8
        elif self.full():
            nom="Full"
            nivel=7
        elif self.color():
            nom="Color"
            nivel=6
        elif self.escalera(1):
            nom="Escalera"
            nivel=5
        elif self.parejasotrioypokar(3):
            nom="Tercia"
            nivel=4
        elif self.doblesparejas():
            nom="Dobles Parejas"
            nivel=3
        elif self.parejasotrioypokar(2):
            nom="Parejas"
            nivel=2
        return nom,nivel,self.lidic[0]


