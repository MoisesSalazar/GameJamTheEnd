import pygame
import sys

class Personaje:
    def __init__(self, ruta_imagen):
        self.sprite_personaje = pygame.image.load(ruta_imagen)
        self.cuadros_neutro = self.dividir_sprite(0, 6)
        self.cuadros_ataque = self.dividir_sprite(1, 6)
        self.cuadros_correr = self.dividir_sprite(2, 8)
        self.cuadros_salto = self.dividir_sprite(3, 8) + self.dividir_sprite(4, 8)
        self.cuadros_derrivo = self.dividir_sprite(5, 8)
        self.cuadros_muerte = self.dividir_sprite(6, 4)
        self.cuadros_personaje = self.cuadros_neutro  # Estado inicial
        self.indice_cuadro = 0
        self.posicion = pygame.Vector2(0, 0)  # Nueva posición del personaje
        self.mirando_derecha = True  # Nueva propiedad


    def dividir_sprite(self, fila, num_columnas):
        cuadros = []
        ancho_cuadro = self.sprite_personaje.get_width() // 8
        alto_cuadro = self.sprite_personaje.get_height() // 7

        for columna in range(num_columnas):
            rect = pygame.Rect(columna * ancho_cuadro, fila * alto_cuadro, ancho_cuadro, alto_cuadro)
            cuadro = self.sprite_personaje.subsurface(rect)
            cuadros.append(cuadro)

        return cuadros

    def actualizar(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.cuadros_personaje = self.cuadros_correr  # Cambia a correr
            self.mirando_derecha = False  # Mirando a la izquierda
        elif teclas[pygame.K_RIGHT]:
            self.cuadros_personaje = self.cuadros_correr  # Cambia a correr
            self.mirando_derecha = True  # Mirando a la derecha
        else:
            self.cuadros_personaje = self.cuadros_neutro  # Cambia a neutro

        self.indice_cuadro = (self.indice_cuadro + 1) % len(self.cuadros_personaje)

    def dibujar(self, pantalla, teclas):
        cuadro = self.cuadros_personaje[self.indice_cuadro]
        if not self.mirando_derecha:
            cuadro = pygame.transform.flip(cuadro, True, False)  # Voltea el sprite
        pantalla.blit(cuadro, self.posicion)  # Dibuja en la posición actual


class Juego:
    def __init__(self, titulo_pantalla, dimensiones, fps):
        pygame.init()
        pygame.mixer.init()  # Inicializa el módulo mixer
        self.titulo_pantalla = titulo_pantalla
        self.dimensiones = dimensiones
        self.fps = fps
        self.screen = pygame.display.set_mode(self.dimensiones)
        pygame.display.set_caption(self.titulo_pantalla)
        self.clock = pygame.time.Clock()

        # Carga y reproduce la música de fondo
        pygame.mixer.music.load('fondo.mp3')
        pygame.mixer.music.play(-1)  # Reproduce la música en bucle


        # Crea una instancia de Personaje
        self.personaje = Personaje('personaje.png')

    def bucle_juego(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Rellena la pantalla con color negro
            self.screen.fill((0, 0, 0))

            # Mueve el personaje
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT]:
                self.personaje.posicion.x -= 5  # Mueve a la izquierda
            if teclas[pygame.K_RIGHT]:
                self.personaje.posicion.x += 5  # Mueve a la derecha

            # Actualiza y dibuja el personaje
            self.personaje.actualizar(teclas)
            self.personaje.dibujar(self.screen, teclas)

            # Actualiza la pantalla
            pygame.display.update()

            # Controla los FPS
            self.clock.tick(self.fps)

# Crear una instancia de Juego con 30 FPS
mi_juego = Juego("TheEnd-UCSP", (800, 600), 30)
mi_juego.bucle_juego()