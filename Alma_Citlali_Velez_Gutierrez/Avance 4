import pygame
from pygame.locals import *
import random
import os
import sys
from moviepy.editor import VideoFileClip

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ORIGINAL_SIZE = (272, 512)
WIDTH = 50
HEIGHT = (WIDTH / ORIGINAL_SIZE[0]) * ORIGINAL_SIZE[1]
SPEED = 1

# Define las limitaciones del área permitida en la pista del jugador
allowed_area = pygame.Rect(100, 300, 600, 200)

# Define las limitaciones del área permitida en la pista de los enemigos
enemy_allowed_area = pygame.Rect(100, 20, 600, 400)

# Directorio donde se encuentran las imágenes de los enemigos
ENEMY_DIRECTORY = r'C:\Users\UnKnown\Documents\juego-python-ia\sprites\corredores'

# Inicializar el reloj
clock = pygame.time.Clock()


class Background(pygame.sprite.Sprite):
    def __init__(self):  # Corregir la definición del método __init__
        # Se inicializa la clase Backgorund
        super(Background, self).__init__()

        # Se carga la imagen de la pista
        self.surf = pygame.image.load(r"C:\Users\UnKnown\Documents\Proyecto_juego\pista.png")
        
        # Se asigna el ancho de la pantalla
        background_width = SCREEN_WIDTH  
        
        # Se calcula la altura necesaria para mantener una proporción con la imagen de fondo
        background_height = (background_width / self.surf.get_width()) * self.surf.get_height()
        
        # Tranforma a escala la imagen de fondo
        self.surf = pygame.transform.scale(self.surf, (background_width, background_height))
        
        # Se crea un rectangulo que tenga las dimensiones de la imagen
        self.rect = self.surf.get_rect(
            bottomleft=(0, SCREEN_HEIGHT)
        )
        # Implementamos un bucle de fondo en el juego que se reposicionan cuando una de ellas se mueve fuera de la pantalla
        self.surf2 = self.surf
        self.rect2 = self.surf2.get_rect(
            bottomleft=self.rect.topleft
        )
        self.ypos = 0
        self.ypos2 = background_height - SCREEN_HEIGHT

    # Crea la ilusión de un entorno en movimiento.
    def update(self, delta_time):
        # Incrementa las posiciones verticales de las superficies de fondo
        self.ypos += 0.05 * delta_time
        self.ypos2 += 0.05 * delta_time
        
        # Actualiza las posiciones verticales de los rectángulos de las superficies de fondo
        self.rect.y = int(self.ypos)
        self.rect2.y = int(self.ypos2)
        
        # Verifica si alguna de las superficies de fondo ha salido completamente de la pantalla
        if self.rect.y > SCREEN_HEIGHT:
            # Si la primera superficie ha salido, la reposiciona justo por encima de la segunda superficie
            self.ypos = self.rect2.y - self.surf2.get_height()
            self.rect.y = self.ypos
            
        if self.rect2.y > SCREEN_HEIGHT:
            # Si la segunda superficie ha salido, la reposiciona justo por encima de la primera superficie
            self.ypos2 = self.rect.y - self.surf.get_height()
            self.rect2.y = self.ypos2

    # Al dibujar ambas superficies se crea el efecto de bucle del fondo
    def render(self, dest):
        # Dibuja la primera superficie de fondo 
        dest.blit(self.surf, self.rect)
        # Dibuja la segunda superficie de fondo 
        dest.blit(self.surf2, self.rect2)


# Clase Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Inicializa la clase Player
        super(Player, self).__init__() 

        # Carga la imagen del carro del jugador
        self.surf = pygame.image.load(r"C:\Users\UnKnown\Documents\juego-python-ia\sprites\carrito.png").convert_alpha()
        
        # Se e aplican las escalas
        self.surf = pygame.transform.scale(self.surf, (WIDTH, HEIGHT))
        
        #Detectar coalisiones
        self.update_mask()

        #Se guarda una copia de la imagen del carro
        self.original_surf = self.surf
        
        #Variable para un seguimiento en la rotación del carro
        self.lastRotation = 0
        
        # Define la posicion para que el jugador comience en la parte de en medio de la pista
        self.rect = self.surf.get_rect(
            center=(
                (SCREEN_WIDTH / 2) - (WIDTH / 2),
                (SCREEN_HEIGHT - HEIGHT)
            )
        )

    def update(self, movement, delta_time):
        # Mueve al jugador depediendo de la velocidad y el movimiento
        self.rect.move_ip(SPEED * movement * delta_time, 0)

        # Restringir el movimiento dentro del área de la pista permitida
        if not allowed_area.contains(self.rect):
            self.rect.clamp_ip(allowed_area)

        # Calcula el ángulo de rotación del jugador
        rotation = 45 * movement * -1
        # Rota la imagen del jugador
        self.surf = pygame.transform.rotate(self.original_surf, self.lerp(self.lastRotation, rotation, .5))
        # Actualiza el angulo de rotación 
        self.lastRotation = rotation
        self.update_mask()

    # Transiciones
    def lerp(self, a: float, b: float, t: float) -> float:
        return (1 - t) * a + t * b

    # Actualiza las coalisiones
    def update_mask(self):
        maskSurface = self.surf
        maskSurface = pygame.transform.scale(maskSurface, (WIDTH * .8, HEIGHT * .8))
        self.mask = pygame.mask.from_surface(maskSurface)

# Clase Enemigos 
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()  # Llama al constructor de la clase base 

        # Selecciona una imagen aleatoria del directorio de enemigos
        enemy_images = os.listdir(ENEMY_DIRECTORY)
        image_name = random.choice(enemy_images)
        image_path = os.path.join(ENEMY_DIRECTORY, image_name)

        # Carga la imagen del enemigo y la escala a un tamaño específico
        self.surf = pygame.image.load(image_path).convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (70, 90))

        # Crea una de colisión a partir de la superficie del enemigo
        self.mask = pygame.mask.from_surface(self.surf)

        # Establece la posición inicial del enemigo de forma aleatoria
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),  # Posición horizontal aleatoria 
                random.randint(-100, -20)  # Posición vertical aleatoria 
            )
        )

        # Establece la velocidad de movimiento del enemigo
        self.speed = (random.randint(1, 2) / 10)  

    def update(self, delta_time):
        # Mueve el rectángulo del enemigo hacia abajo en función de su velocidad y el tiempo transcurrido
        self.rect.move_ip(0, self.speed * delta_time)

        if not enemy_allowed_area.contains(self.rect):
            # Si el enemigo sale de esa área, lo reposiciona dentro de ella
            self.rect.clamp_ip(enemy_allowed_area)
            
        # Actualiza la máscara de colisión del enemigo 
        self.mask = pygame.mask.from_surface(self.surf)

        # Si el enemigo sale completamente de la pantalla por la parte inferior, se elimina
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()  # Elimina el enemigo del grupo de sprites al que pertenece


# Función para generar enemigos
def generate_enemy(enemies):
    new_enemy = Enemy()
    enemies.add(new_enemy)


# Reproducción del vvideo
def play_video():
    pygame.display.set_caption("ChecoGame")
    
    video_path = r"C:\Users\UnKnown\Documents\Proyecto_juego\f1_intro.mp4" # Ruta del archivo de video

    # Reproducir el video con sonido
    video_clip = VideoFileClip(video_path)

    # Redimensionar el video al tamaño deseado y centrarlo en una ventana de 800x600
    video_clip_resized = video_clip.resize((SCREEN_WIDTH, SCREEN_HEIGHT))
    video_clip_resized = video_clip_resized.set_position(('center', 'center'))

    # Reproducir el video con sonido
    video_clip_resized.preview()


def show_menu():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Menú")
    
    # Cargar imagen de fondo del menú
    background_image = pygame.image.load(r"C:\Users\UnKnown\Documents\Proyecto_juego\back_menu.jpg").convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Redimensionar la imagen al tamaño de la pantalla

    # Cargar imagen del botón de inicio
    start_button_image = pygame.image.load(r"C:\Users\UnKnown\Documents\Proyecto_juego\boton.png").convert_alpha()
    start_button_image = pygame.transform.scale(start_button_image, (200, 100))  # Redimensionar el botón

    # Inicializar el módulo de sonido de pygame
    pygame.mixer.init()
    # Cargar el archivo de audio
    background_music = pygame.mixer.Sound(r"C:\Users\UnKnown\Documents\juego-python-ia\sprites\intro.wav")
    # Reproducir el audio en bucle
    background_music.play(-1)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                # Detener la reproducción del audio cuando se hace clic en el botón de inicio
                background_music.stop()
                # Verificar si el botón de inicio fue presionado
                if start_button_rect.collidepoint(event.pos):
                    return  # Salir de la función para iniciar el juego

        # Dibujar la imagen de fondo del menú
        screen.blit(background_image, (0, 0))

        # Obtener el rectángulo del botón de inicio
        start_button_rect = start_button_image.get_rect()
        # Centrar el botón de inicio en la parte inferior de la pantalla
        start_button_rect.center = (400, 550)
        # Dibujar el botón de inicio
        screen.blit(start_button_image, start_button_rect)

        pygame.display.flip()
        clock.tick(30)
        

def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ChecoGame")
    
    # Crear una instancia de Background
    background = Background()
    
    # Inicializar el módulo de sonido de pygame
    pygame.mixer.init()
    # Cargar el archivo de audio
    background_music = pygame.mixer.Sound(r"C:\Users\UnKnown\Documents\juego-python-ia\sprites\carros.wav")
    # Reproducir el audio en bucle
    background_music.play(-1)
    
    clock = pygame.time.Clock()
    
    # Crear instancias de las clases Player y Enemy
    player = Player()
    enemies = pygame.sprite.Group()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Actualizar el fondo
        background.update(clock.get_time())

        # Dibujar el fondo en la pantalla
        background.render(screen)

        # Controlar al jugador con las teclas de flecha
        keys = pygame.key.get_pressed()
        movement = keys[K_RIGHT] - keys[K_LEFT]  # Movimiento lateral
        player.update(movement, clock.get_time())

        # Generar un nuevo enemigo aleatorio de vez en cuando
        if random.random() < 0.01:
            generate_enemy(enemies)

        # Actualizar enemigos
        enemies.update(clock.get_time())

        # Dibujar al jugador
        screen.blit(player.surf, player.rect)

        # Dibujar enemigos
        for enemy in enemies:
            screen.blit(enemy.surf, enemy.rect)

        pygame.display.flip()

        # Limitar la velocidad de fotogramas
        clock.tick(60)  # Limitar a 60 FPS

    pygame.quit()
    sys.exit()

def main():
    # Reproducir el video con sonido antes de iniciar el juego
    play_video()

    # Mostrar el menú y esperar a que el usuario inicie el juego
    show_menu()

    # Iniciar el juego
    game_loop()
    

main()
