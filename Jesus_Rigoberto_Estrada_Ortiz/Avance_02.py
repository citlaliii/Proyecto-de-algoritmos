import pygame
from pygame.locals import *
import random
import os

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ORIGINAL_SIZE = (272, 512)
WIDTH = 50
HEIGHT = (WIDTH / ORIGINAL_SIZE[0]) * ORIGINAL_SIZE[1]
SPEED = 1

# Directorio donde se encuentran las imágenes de los enemigos
ENEMY_DIRECTORY = r'C:\Users\servidor\Desktop\juego-python-ia-misiles-main\juego-python-ia-misiles-main\sprites\corredores'

# Inicializar Pygame
pygame.init()

# Configurar la ventana del juego
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mi Juego")

# Inicializar el reloj
clock = pygame.time.Clock()

# Clase Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        self.surf = pygame.image.load(r"C:\Users\servidor\Desktop\juego-python-ia-misiles-main\juego-python-ia-misiles-main\sprites\carrito.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (WIDTH, HEIGHT))
        self.update_mask()

        self.original_surf = self.surf
        self.lastRotation = 0
        
        self.rect = self.surf.get_rect(
            center=(
                (SCREEN_WIDTH / 2) - (WIDTH / 2),
                (SCREEN_HEIGHT - HEIGHT)
            )
        )

    def update(self, movement, delta_time):
        self.rect.move_ip(SPEED * movement * delta_time, 0)

        rotation = 45 * movement * -1
        self.surf = pygame.transform.rotate(self.original_surf, self.lerp(self.lastRotation, rotation, .5))
        self.lastRotation = rotation
        self.update_mask()

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0: self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT: self.rect.bottom = SCREEN_HEIGHT

    def lerp(self, a: float, b: float, t: float) -> float:
        return (1 - t) * a + t * b

    def update_mask(self):
        maskSurface = self.surf
        maskSurface = pygame.transform.scale(maskSurface, (WIDTH * .8, HEIGHT * .8))
        self.mask = pygame.mask.from_surface(maskSurface)

# Clase Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()

        enemy_images = os.listdir(ENEMY_DIRECTORY)
        image_name = random.choice(enemy_images)
        image_path = os.path.join(ENEMY_DIRECTORY, image_name)

        self.surf = pygame.image.load(image_path).convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (70, 90))
        self.mask = pygame.mask.from_surface(self.surf)

        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
                random.randint(-100, -20)
            )
        )

        self.speed = (random.randint(1, 2) / 10)

    def update(self, delta_time):
        self.rect.move_ip(0, self.speed * delta_time)
        self.mask = pygame.mask.from_surface(self.surf)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Función para generar enemigos
def generate_enemy():
    new_enemy = Enemy()
    enemies.add(new_enemy)

# Crear instancias de las clases Player y Enemy
player = Player()
enemies = pygame.sprite.Group()

# Bucle principal del juego
running = True
while running:
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Controlar al jugador con las teclas de flecha
    keys = pygame.key.get_pressed()
    movement = keys[K_RIGHT] - keys[K_LEFT]  # Movimiento lateral
    player.update(movement, clock.get_time())

    # Generar un nuevo enemigo aleatorio de vez en cuando
    if random.random() < 0.01:
        generate_enemy()

    # Actualizar enemigos
    enemies.update(clock.get_time())

    # Dibujar en pantalla
    screen.fill((0, 0, 0))  # Limpiar la pantalla
    screen.blit(player.surf, player.rect)  # Dibujar al jugador

    for enemy in enemies:
        screen.blit(enemy.surf, enemy.rect)  # Dibujar enemigos

    pygame.display.flip()

    # Limitar la velocidad de fotogramas
    clock.tick(60)  # Limitar a 60 FPS

# Salir del juego
pygame.quit()
