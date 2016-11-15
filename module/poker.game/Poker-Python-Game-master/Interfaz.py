import pygame, sys, time, threading
from pygame.locals import *
# import Parametro

class Interfaz:
	def __init__(self):
		self.Bandera1=1
		self.NumJug=0
	def Ejecutar(self):
		# class Prueba:
		# 	def __init__(self, x):
		# 		self.valor=x
		# 	def imprimir(self):
		# 		print self.valor
		# bb=Prueba(2)
		# bb.imprimir()

		class Cursor(pygame.Rect):
			def __init__(self):
				pygame.Rect.__init__(self, 0, 0, 1, 1)
			def update(self):
				self.left, self.top = pygame.mouse.get_pos()	

		class Boton(pygame.sprite.Sprite):
			def __init__(self, Jugar, Jugar2, x=123, y=79):
				self.imagen_normal = Jugar
				self.imagen_raton = Jugar2
				self.imagen_actual = self.imagen_normal
				self.rect = self.imagen_actual.get_rect()
				self.rect.left,self.rect.top = (x,y)
			def update(self,ventana,cursor1):
				if cursor1.colliderect(self.rect):
					self.imagen_actual = self.imagen_raton
				else: 
					self.imagen_actual = self.imagen_normal
					
				ventana.blit(self.imagen_actual, self.rect)

		# def main():
		pygame.init()
		ButtonsPlayers = False
		ActivarEventoBtns = False
		BotonInicio = True
		Ciclo=True
		ventana= pygame.display.set_mode((1008, 567))
		pygame.display.set_caption('Pokar en Python & PyGame')
		Color=(76,171,125,0.5)
		Color3=(4,140,60)
		Color2=pygame.Color(255,129,9)
		contornojuego = pygame.Rect(10,10,1380,680)
		Blanco = pygame.Color(255,255,255)
		fuente1 = pygame.font.Font(None, 28)
		fuente2 = pygame.font.Font(None, 70)
		logo = pygame.image.load("botones/LogoFondo2.png")
			
		while Ciclo: # main game loop
			ventana.fill(Color3)
			ventana.blit(logo,(0,0))
			Jugar = pygame.image.load("botones/BotonJugar1.png")
			Jugar2 = pygame.image.load("botones/BotonJugar2.png")
			jugador2 = pygame.image.load("botones/BtnJugadores/Sombra/jugador2.png")
			jugador22 = pygame.image.load("botones/BtnJugadores/Brillo/jugador2.png")
			jugador3 = pygame.image.load("botones/BtnJugadores/Sombra/jugador3.png")
			jugador33 = pygame.image.load("botones/BtnJugadores/Brillo/jugador3.png")
			jugador4 = pygame.image.load("botones/BtnJugadores/Sombra/jugador4.png")
			jugador44 = pygame.image.load("botones/BtnJugadores/Brillo/jugador4.png")
			jugador5 = pygame.image.load("botones/BtnJugadores/Sombra/jugador5.png")
			jugador55 = pygame.image.load("botones/BtnJugadores/Brillo/jugador5.png")

			cursor1 = Cursor()
			cursor1.update()

			if ButtonsPlayers:
				btnjugador1 = Boton(jugador2, jugador22, 220, 410)
				btnjugador2 = Boton(jugador3, jugador33, 370, 410)
				btnjugador3 = Boton(jugador4, jugador44, 520, 410)
				btnjugador4 = Boton(jugador5, jugador55, 670, 410)

				btnjugador1.update(ventana,cursor1)
				btnjugador2.update(ventana,cursor1)
				btnjugador3.update(ventana,cursor1)
				btnjugador4.update(ventana,cursor1)
				BotonInicio = False

			if BotonInicio:
				boton1 = Boton(Jugar, Jugar2, 408, 330)
				boton1.update(ventana,cursor1)


			# Nuevojuego = pygame.image.load("botones/points.png")
			# ventana.blit(Nuevojuego,(80,65))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					# pygame.quit()
					sys.exit()

				elif event.type == pygame.MOUSEBUTTONDOWN:
					x, y = event.pos
					print (x, y)

					if (x >= 408 and y >= 330 and x <= 608 and y <= 430):
						print ('Boton Jugar')
						ButtonsPlayers = True
						ActivarEventoBtns = True

					elif (ActivarEventoBtns):
						if (x >= 220 and y >= 410 and x <= 340 and y <= 470):
							print ('Boton 2 Jugadores')
							self.NumJug=2
							Ciclo=False

						elif (x >= 370 and y >= 410 and x <= 490 and y <= 470):
							print ('Boton 3 Jugadores')
							self.NumJug=3
							Ciclo=False

						elif (x >= 520 and y >= 410 and x <= 640 and y <= 470):
							print ('Boton 4 Jugadores')
							self.NumJug=4
							Ciclo=False
							# from labels import *

						elif (x >= 670 and y >= 410 and x <= 790 and y <= 470):
							print ('Boton 5 Jugadores')
							self.NumJug=5
							Ciclo=False

			pygame.display.update()
	def Retornar(self):
		return self.NumJug
# Abrir = Interfaz()
# Abrir.Ejecutar()