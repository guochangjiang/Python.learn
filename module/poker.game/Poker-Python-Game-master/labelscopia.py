import sys
import pygame, sys
from pygame.locals import *
from extra import *
class JuegoInterfaz:
	def __init__(self, x):
		self.Parametro=x
	# def Imprimir(self):
	# 	print self.Parametro
	def IniciarJuego(self):
		try:
			print self.Parametro
			Ciclo2=True
			pygame.init()
			ventana= pygame.display.set_mode((1400, 700))
			pygame.display.set_caption('Poker en Python & PyGame')
			Color=(76,171,125,0.5)
			Color3=(4,140,60)
			Color2=pygame.Color(255,129,9)
			contornojuego = pygame.Rect(10,10,1380,680)
			Blanco = pygame.Color(255,255,255)
			fuente1 = pygame.font.Font(None, 28)
			fuente2 = pygame.font.Font(None, 22)
			fuente3 = pygame.font.Font(None, 40)
			banderainicio=False
			bancargcartas=False
			banderapresionaespacio=True
			instruccion="Presiona la telca 'Espacio' para iniciar el juego"
			haywinner=False
			contspace=0
			li1=[]
			li2=[]
			li3=[]
			li4=[]
			Juego=Juegos()
			Jugador1=Jugador(li1,"Jugador 1","Ninguna")
			Jugador2=Jugador(li2,"Jugador 2","Ninguna")
			Jugador3=Jugador(li3,"Jugador 3","Ninguna")
			Jugador4=Jugador(li4,"Nosotros","Ninguna")
			ganador="Juancho"
			listageneral=Juego.arrancarlista()

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
	
			while Ciclo2: # main game loop
				ventana.fill(Color3)
				pygame.draw.rect(ventana,Color,contornojuego) #Contorno verde
				label1 = fuente1.render("Bienvenido a PokerGame",0,Blanco)
				ventana.blit(label1,(600,15))
				marcos(420,50,600,200,Blanco)#Top
				marcos(420,470,600,200,Blanco)#Down
				marcos(1170,50,200,600,Blanco)#Der
				marcos(25,50,200,600,Blanco)#Izq
				marcos(430,60,580,180,Color)#Top
				marcos(430,480,580,180,Color)#Down
				marcos(1180,60,180,580,Color)#Der
				marcos(35,60,180,580,Color)#Izq
				drawlabel(instruccion,550,450)
				drawlabel("Jugador 1",85,650)
				drawlabel("Jugador 2",1235,650)
				drawlabel("Jugador 3",680,250)
				drawlabel("Nosotros",680,250)
				if haywinner:
					drawlabel("The winner is: "+ganador,800,350)
					drawlabel("The winner is: "+ganador,230,350)
				cargarlista(615,300,listageneral,3,True)
				#Cartas de jugadores
				if bancargcartas:
					cargarlista(80,150,Jugador1.lista,50,False)
					cargarlista(1235,150,Jugador2.lista,50,False)
					cargarlista(530,85,Jugador3.lista,50,True)
					cargarlista(530,510,Jugador4.lista,50,True)
				#Cargar jugadas
				if Jugador1.ban:
					drawlabel("Jugada Jugador:"+str(Jugador1.jug),80,670)
				if Jugador2.ban:
					drawlabel("Jugada Jugador:"+str(Jugador2.jug),1200,670)
				if Jugador3.ban:
					drawlabel("Jugada Jugador:"+str(Jugador3.jug),670,225)
				if Jugador4.ban:
					drawlabel("Jugada Jugador:"+str(Jugador4.jug),680,640)
				for event in pygame.event.get():
					if event.type == QUIT:
						pygame.quit()
						# sys.exit()
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_SPACE :		
							if contspace==0:
								banderainicio=True
								listageneral=Juego.reborujar(listageneral)
								instruccion="Presione las telcas 'direccion' para obtener jugadas"
								Jugador1.lista,listageneral=Juego.darcartas(listageneral)
								Jugador2.lista,listageneral=Juego.darcartas(listageneral)
								Jugador3.lista,listageneral=Juego.darcartas(listageneral)
								Jugador4.lista,listageneral=Juego.darcartas(listageneral)
								bancargcartas=True
								# espacio
								ganador,Jugador1.jug,Jugador2.jug,Jugador3.jug,Jugador4.jug=Juego.comenzar(Jugador1,Jugador2,Jugador3,Jugador4)					
								print("The winner is: "+str(ganador))
							contspace=contspace+1
						if event.key == pygame.K_RIGHT and contspace!=0 :		
							Jugador2.ban=True
						elif event.key == pygame.K_LEFT  and contspace!=0:		
							Jugador1.ban=True
						if event.key == pygame.K_UP  and contspace!=0:		
							Jugador3.ban=True
						if event.key == pygame.K_DOWN  and contspace!=0:		
							Jugador4.ban=True
						if event.key == pygame.K_TAB and Jugador1.ban==True and Jugador2.ban==True and Jugador3.ban==True and Jugador4.ban==True:		
							haywinner=True
						if event.key == pygame.K_s:
							Ciclo2=False
						if event.key == pygame.K_r:
							listageneral=Juego.arrancarlista()
							contspace=0
							Jugador1.ban=False
							Jugador2.ban=False
							Jugador3.ban=False
							Jugador4.ban=False
							Jugador1.lista=[]
							Jugador2.lista=[]
							Jugador3.lista=[]
							Jugador4.lista=[]
				pygame.display.update()
		except Exception, errormsg:
		    print "Script errored!"
		    print "Error message: %s" % errormsg
		    print "Traceback:"
		    import traceback
		    traceback.print_exc()
		    print "Press return to exit.."
		    raw_input()