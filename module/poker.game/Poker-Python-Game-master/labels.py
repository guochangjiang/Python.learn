import sys
import pygame, sys
from pygame.locals import *
from Poker import ListaJugadorCartas
class JuegoInterfaz:
	def __init__(self, x):
		self.Parametro=x
	# def Imprimir(self):
	# 	print self.Parametro
	def IniciarJuego(self):
		try:
			print (self.Parametro)
			Ciclo2=True
			pygame.init()
			gan=[]
			ventana= pygame.display.set_mode((1400, 700))
			pygame.display.set_caption('Poker en Python & PyGame')
			Color=(76,171,125,0.5)
			Color3=(44,144,138)
			Color2=pygame.Color(255,129,9)
			contornojuego = pygame.Rect(10,10,1380,680)
			Blanco = pygame.Color(192,255,235)
			fuente1 = pygame.font.Font(None, 28)
			fuente2 = pygame.font.Font(None, 22)
			fuente3 = pygame.font.Font(None, 40)
			instruccion="*Presione espacio para repartir cartas*"
			listajugadores=[]
			posisioncartasobra=0
			game=ListaJugadorCartas.ListaJugadorCartas()
			banespacio=True
			banreiniciar=False
			banganador=False
			def marcos(xe,xt,ye,yt,Col):
				marco = pygame.Rect(xe,xt,ye,yt)
				pygame.draw.rect(ventana,Col,marco)
			def drawlabel(texto,x,y):
				label = fuente2.render(texto,0,Blanco)
				ventana.blit(label,(x,y))
			def cargarlista(x,y,lista,vs,t):
				for i in lista:
					if t:
						x=x+vs
					else:
						y=y+vs
					cartassobramtes = pygame.image.load(str(i.ruta))
					ventana.blit(cartassobramtes,(x,y))
				return x
			def generarinterfaz(nj):
				if nj!=5:
					drawlabel("Jugador 1",85,650)
					drawlabel("Jugador 2",1235,650)
					marcos(1170,50,200,600,Blanco)#Der
					marcos(25,50,200,600,Blanco)#Izq
					marcos(1180,60,180,580,Color)#Der
					marcos(35,60,180,580,Color)#Izq
					if nj==3:
						drawlabel("Jugador 3",680,250)
						marcos(420,50,600,200,Blanco)#Top
						marcos(430,60,580,180,Color)#Top
					elif nj==4:
						drawlabel("Jugador 3",680,250)
						drawlabel("Jugador 4",680,450)
						marcos(420,50,600,200,Blanco)#Top
						marcos(420,470,600,200,Blanco)#Down
						marcos(430,60,580,180,Color)#Top
						marcos(430,480,580,180,Color)#Down
				else:
					drawlabel("Jugador 1",85,33)
					drawlabel("Jugador 3",680,33)
					drawlabel("Jugador 2",1230,33)
					drawlabel("Jugador 4",333,452)
					drawlabel("Jugador 5",1000,452)
					marcos(420,50,600,200,Blanco)#Jugador 1 arriba 
					marcos(430,60,580,180,Color)#Jugador 1 arriba 
					marcos(140,470,500,200,Blanco)#Jugador 2
					marcos(150,480,480,180,Color)#Jugador 2
					marcos(25,50,200,400,Blanco)#Jugador 3 
					marcos(35,60,180,380,Color)#Jugador 3
					marcos(1170,50,200,400,Blanco)#Jugador 4
					marcos(1180,60,180,380,Color)#Jugador 4
					marcos(790,470,500,200,Blanco)#Jugador 5
					marcos(800,480,480,180,Color)#Jugador 5
			def cargarlistas(nj):
				if nj!=5:
					cargarlista(80,150,listajugadores[0],50,False)
					cargarlista(1235,150,listajugadores[1],50,False)
					if nj==3:
						cargarlista(530,85,listajugadores[2],50,True)
					if nj==4:
						cargarlista(530,85,listajugadores[2],50,True)
						cargarlista(530,510,listajugadores[3],50,True)
				else:
					cargarlista(80,40,listajugadores[0],50,False)
					cargarlista(1235,40,listajugadores[1],50,False)
					cargarlista(210,510,listajugadores[3],50,True)
					cargarlista(530,85,listajugadores[2],50,True)
					cargarlista(850,510,listajugadores[4],50,True)
			while Ciclo2: # main game loop
				ventana.fill(Color3)
				pygame.draw.rect(ventana,Color,contornojuego) #Contorno verde
				label1 = fuente1.render("Bienvenido a PokerGame",0,Blanco)
				ventana.blit(label1,(600,15))
				generarinterfaz(self.Parametro)
				posisioncartasobra=cargarlista(615,300,game.lista,3,True)
				cartassobramtes = pygame.image.load("cartas02\sobra.gif")
				ventana.blit(cartassobramtes,(posisioncartasobra,300))
				drawlabel(instruccion,580,280)
				if banespacio==False:
					cargarlistas(self.Parametro)
				if banganador:
					drawlabel("Ganador: "+str(gan[0].nombre),400,330)
					drawlabel("Jugada: "+str(gan[0].jugada),400,350)
				#Cartas de jugadores
				for event in pygame.event.get():
					if event.type == QUIT:
						pygame.quit()
						# sys.exit()
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_SPACE :		
							if banespacio:
								listajugadores=game.CrearJugadores(self.Parametro)
								instruccion="*Presione la g para obtener ganador*"
								banespacio=False
								for i in listajugadores:
									for l in i:
										print("Tipo: "+str(l.tipo)+" Nivel: "+str(l.nivel))
									print("")
						if event.key == pygame.K_s and banreiniciar:
							Ciclo2=False
						if event.key==pygame.K_g:
							instruccion="*Presione la tecla s para volver al menu o z para reiniciar*"
							banreiniciar=True
							banganador=True
							gan=game.Ganador()
							print("Nombre: "+str(gan[0].nombre+" Jugada: "+str(gan[0].jugada)))
						if event.key==pygame.K_z:
							banespacio=True
							instruccion="*Presione espacio para repartir cartas*"
							banreiniciar=False
							banganador=False
							game.__init__()
							
				pygame.display.update()
		except Exception as errormsg:
		    print ("Script errored!")
		    print ("Error message: %s" % errormsg)
		    print ("Traceback:")
		    import traceback
		    traceback.print_exc()
		    print ("Press return to exit..")
		    input()