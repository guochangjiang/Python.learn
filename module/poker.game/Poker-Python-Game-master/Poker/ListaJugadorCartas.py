from Baraja import Baraja
from Jugador_Cartas import Jugador_Cartas
from Jugador import Jugador
class ListaJugadorCartas(Baraja,Jugador_Cartas):
    def __init__(self):
        self.listajugadores=[]
        Baraja.__init__(self)
        self.mezclar()
        self.listageneral=[]
    def CrearJugadores(self,NumeroJugadores):
        for x in range(NumeroJugadores):
            self.listajugadores.append(Jugador("Jugador: "+str(x+1)))
            minilista=[]    
            for i in range(5):
                minilista.append(self.RepartirCarta())
                minilista=self.ordenarcartas(minilista)
            self.listajugadores[x].lista=minilista
            self.listageneral.append(minilista)
        return self.listageneral
    def Ganador(self):
        niveles=[]
        listaempat=[]
        for i in self.listajugadores:
            i.jugada,i.nivel,i.diccn=self.tipojugadas(i.lista)
        for i in self.listajugadores:
            print(str(i.nombre)+" "+" "+str(i.nivel)+" "+str(i.jugada))
        print("")
        n=len(self.listajugadores)
        j=0
        i=0
        for i in range(0,n):    
            for j in range(0,n-1):
                if(self.listajugadores[j].nivel < self.listajugadores[j+1].nivel):
                    h=self.listajugadores[j]
                    k=self.listajugadores[j+1]
                    self.listajugadores[j]=k
                    self.listajugadores[j+1]=h
        for i in self.listajugadores:
            print(str(i.nombre)+" "+" "+str(i.nivel)+" "+str(i.jugada))
        va=self.listajugadores[0].nivel
        listaultimos=[]
        for i in self.listajugadores:
            if i.nivel==va:
                listaultimos.append(i)
        print("")
        for i in listaultimos:
            print(str(i.nombre)+" "+" "+str(i.nivel)+" "+str(i.jugada))
        if va==1:
            print("NO hubo ninguna jugada")
            listaultimos=self.cartaalta(self.listajugadores)
        elif len(listaultimos)>1:
            listaultimos=self.empates(va,listaultimos)
            #print(listaultimos[0].nombre)
        return listaultimos