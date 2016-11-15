import Interfaz
import labels
while True:
	Abrir = Interfaz.Interfaz()
	Abrir.Ejecutar()
	Jugadores = Abrir.Retornar()
	AbrirJuego = labels.JuegoInterfaz(Jugadores)
	# AbrirJuego.Imprimir()
	AbrirJuego.IniciarJuego()