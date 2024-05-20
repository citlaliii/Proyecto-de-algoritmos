import pygame
import sys
from moviepy.editor import VideoFileClip
from pygame.locals import *
from threading import Thread
import cv2
import platform
import random
import os
import cv2
import mediapipe as mp
import math
import os
from threading import Thread
from datetime import datetime

# Define las limitaciones del área permitida en la pista del jugador
allowed_area = pygame.Rect(100, 300, 600, 200)

# Define las limitaciones del área permitida en la pista de los enemigos
enemy_allowed_area = pygame.Rect(400, 10, 500, 300)


# Definir un nuevo evento personalizado para agregar enemigos al juego
ADD_ENEMY = pygame.USEREVENT + 1

# Configurar la velocidad inicial del juego
game_speed = 1

# Tamallo de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Tamano original de las imagenes 
ORIGINAL_SIZE = (272,512)
WIDTH = 50
HEIGHT = (WIDTH/ORIGINAL_SIZE[0])*ORIGINAL_SIZE[1]
SPEED = 1

# Directorio donde se encuentran las imágenes de los enemigos
ENEMY_DIRECTORY = r'C:\Users\UnKnown\Downloads\proyecto_algoritmos\sprites\corredores'

# Función main
def main():
    # Reproducir el video con sonido antes de iniciar el juego
    play_video()

    # Mostrar el menú y esperar a que el usuario inicie el juego
    show_menu()

    # Iniciar el juego
    Game().loop()

# Función para reproducir el video de la intro
def play_video():
    pygame.display.set_caption("ChecoGame")
    # Ruta del archivo de video
    video_path = r"C:\Users\UnKnown\Downloads\proyecto_algoritmos\sprites\f1_intro.mp4"

    # Reproducir el video con sonido
    video_clip = VideoFileClip(video_path)

    # Redimensionar el video al tamaño deseado y centrarlo en una ventana de 800x600
    video_clip_resized = video_clip.resize((800, 600))
    video_clip_resized = video_clip_resized.set_position(('center', 'center'))

    # Reproducir el video con sonido
    video_clip_resized.preview()

# Función del menú
def show_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Menú")
    
    # Cargar imagen de fondo del menú
    background_image = pygame.image.load(r"C:\Users\UnKnown\Downloads\proyecto_algoritmos\sprites\back_menu.jpg").convert()
    background_image = pygame.transform.scale(background_image, (800, 600))  # Redimensionar la imagen al tamaño de la pantalla

    # Cargar imagen del botón de inicio
    start_button_image = pygame.image.load(r"C:\Users\UnKnown\Downloads\proyecto_algoritmos\sprites\boton.png").convert_alpha()
    start_button_image = pygame.transform.scale(start_button_image, (200, 100))  # Redimensionar el botón

    # Inicializar el módulo de sonido de pygame
    pygame.mixer.init()
    # Cargar el archivo de audio
    background_music = pygame.mixer.Sound(r"C:\Users\UnKnown\Downloads\proyecto_algoritmos\sprites\intro.wav")
    # Reproducir el audio en bucle
    background_music.play(-1)
    
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                # Verificar si el botón de inicio fue presionado
                if start_button_rect.collidepoint(event.pos):
                    background_music.stop()  # Detener la música antes de salir del menú
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

# Clase enemigo
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemies_group):
        super(Enemy, self).__init__()

        self.enemies_group = enemies_group
        
        # Lista de nombres de archivos de imágenes de enemigos
        enemy_images = os.listdir(ENEMY_DIRECTORY)

        # Selecciona aleatoriamente una imagen de la lista
        image_name = random.choice(enemy_images)
        image_path = os.path.join(ENEMY_DIRECTORY, image_name)

        # Carga la imagen y la escala
        self.surf = pygame.image.load(image_path).convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (70, 90))  # Escala fija
        self.mask = pygame.mask.from_surface(self.surf)

        # Configura el rectángulo y la posición inicial
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
                random.randint(-100, -20)
            )
        )
        # Limites de pista
        if not enemy_allowed_area.contains(self.rect):
            # Si el enemigo sale de esa área, lo reposiciona dentro de ella
            self.rect.clamp_ip(enemy_allowed_area)
            
        # Velocidad semi-aleatoria, aumenta con la velocidad global del juego
        self.speed = (random.randint(1, 2) / 10) * (1 + (game_speed / 2))

        self.rect.bottomleft = (random.randint(0, SCREEN_WIDTH - self.rect.width), -self.rect.height)

    # Representa los movimientos de los enemigos en la pantalla
    def update(self, delta_time):
        # Movimiento hacia abajo
        self.rect.move_ip(0, self.speed * delta_time)
        self.mask = pygame.mask.from_surface(self.surf)

        # Verificación de colisiones con otros enemigos
        for enemy in self.enemies_group:
            if enemy != self and self.rect.colliderect(enemy.rect):
                # Si hay colisión con otro enemigo, ajusta la posición vertical
                if self.speed > 0:
                    self.rect.bottom = min(enemy.rect.top, self.rect.bottom) - 1
                else:
                    self.rect.top = max(enemy.rect.bottom, self.rect.top) + 1

        # Eliminación cuando sale de la pantalla
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
                


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super(Background, self).__init__()

        self.surf = pygame.image.load(r"C:\Users\UnKnown\Downloads\proyecto_algoritmos\sprites\pista.png")
        background_width = SCREEN_WIDTH #doble ancho
        background_height = (background_width/self.surf.get_width())*self.surf.get_height()
        self.surf = pygame.transform.scale(self.surf, (background_width, background_height))
        self.rect = self.surf.get_rect(
            bottomleft=(0,SCREEN_HEIGHT)
        )
        # Implementamos un bucle de fondo en el juego que se reposicionan cuando una de ellas se mueve fuera de la pantalla
        #Usamos 2 surface para hacer un buen loop del fondo
        #Se mueven juntos y cuando uno desaparece de pantalla se mueve
        #hasta abajo, y asi se van repitiendo
        self.surf2 = self.surf
        self.rect2 = self.surf2.get_rect(
            bottomleft=self.rect.topleft
        )
        self.ypos = 0
        self.ypos2 = background_height-SCREEN_HEIGHT

    # Gestiona el fondo de la pista
    def update(self, delta_time):
        self.ypos += .05 * delta_time
        self.ypos2 += .05 * delta_time
        self.rect.y = int(self.ypos)
        self.rect2.y = int(self.ypos2)
        if self.rect.y > SCREEN_HEIGHT:
            self.ypos = self.rect2.y - self.surf2.get_height()
            self.rect.y = self.ypos
        if self.rect2.y > SCREEN_HEIGHT:
            self.ypos2 = self.rect.y - self.surf.get_height()
            self.rect2.y = self.ypos2

    # Dibuja los fondos de la pista en la pantalla
    def render(self, dest):
        dest.blit(self.surf, self.rect)
        dest.blit(self.surf2, self.rect2)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        self.surf = pygame.image.load(r"C:\Users\UnKnown\Downloads\proyecto_algoritmos\sprites\carrito.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (WIDTH,HEIGHT))
        self.update_mask()

        #Guardar para manejar bien las rotaciones
        self.original_surf = self.surf 
        self.lastRotation = 0
        
        # Posicionamos al jugador en el centro
        self.rect = self.surf.get_rect(
            center=(
                (SCREEN_WIDTH/2) - (WIDTH/2),
                (SCREEN_HEIGHT - HEIGHT)
            )
        )

    def update(self, movement, delta_time):
        self.rect.move_ip(SPEED * movement * delta_time, 0)

        # Restringir el movimiento dentro del área de la pista permitida
        if not allowed_area.contains(self.rect):
            self.rect.clamp_ip(allowed_area)
            
        # Rotación
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
        #Mascara tiene un 80% del tamano para 'perdonar' al jugador en ciertas colisiones
        maskSurface = self.surf
        maskSurface = pygame.transform.scale(maskSurface, (WIDTH*.8,HEIGHT*.8))
        self.mask = pygame.mask.from_surface(maskSurface)
        

class Game:
    def __init__(self):
        pygame.mixer.init()
        self.background_music = pygame.mixer.Sound(r"C:\Users\UnKnown\Downloads\proyecto_algoritmos\sprites\carros.wav")
        
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.clock = pygame.time.Clock()
        self.running = True
        self.started = False

        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        pygame.init()
        pygame.display.set_caption("ChecoGame")

        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.smaller_font = pygame.font.Font('freesansbold.ttf', 22)
        
        self.background = Background()
        self.initialize()

    def initialize(self):
        self.start_time = pygame.time.get_ticks()
        self.last_frame_time = self.start_time
        self.player = Player()
        self.movement = 0
        self.enemy_timer = 1000
        pygame.time.set_timer(ADD_ENEMY, self.enemy_timer)
        self.enemies = pygame.sprite.Group()
        self.lost = False
        self.score = 0
        self.webcam = Webcam().start()
        self.max_face_surf_height = 0
        self.face_left_x = 0
        self.face_right_x = 0
        self.face_top_y = 0
        self.face_bottom_y = 0
        self.background_music.play(-1)
        self.leaderboard = self.load_leaderboard()

    def update(self, delta_time):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False

        if self.lost or not self.started:
            for event in events:
                if event.type == KEYDOWN and event.key == K_RETURN:
                    self.initialize()
                    self.started = True
        else:
            game_speed = 1 + ((pygame.time.get_ticks() - self.start_time) / 1000) * .1
            self.score = self.score + (delta_time * game_speed)

            for event in events:
                if event.type == ADD_ENEMY:
                    num = random.randint(1, 2)
                    for e in range(num):
                        enemy = Enemy(self.enemies)
                        self.enemies.add(enemy)
                    self.enemy_timer = 1000 - ((game_speed - 1) * 100)
                    if self.enemy_timer < 50:
                        self.enemy_timer = 50
                    pygame.time.set_timer(ADD_ENEMY, int(self.enemy_timer))

            self.player.update(self.movement, delta_time)
            self.enemies.update(delta_time)
            self.process_collisions()
            self.background.update(delta_time)
            self.render_leaderboard()

    def process_collisions(self):
        collide = pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_mask)
        if collide:
            self.lost = True
            self.update_leaderboard(self.score)  # Actualizar el leaderboard
            

    def load_leaderboard(self):
        leaderboard = []
        if os.path.exists('leaderboard.txt'):
            with open('leaderboard.txt', 'r') as file:
                for line in file:
                    name, score = line.strip().split(',')
                    leaderboard.append((name, int(score)))
        return leaderboard

    def update_leaderboard(self, new_score):
        name = "Jugador"  # Aquí puedes pedir el nombre del jugador si deseas
        self.leaderboard.append((name, int(new_score)))
        self.leaderboard = sorted(self.leaderboard, key=lambda x: x[1], reverse=True)[:5]
        with open('leaderboard.txt', 'w') as file:
            for entry in self.leaderboard:
                file.write(f"{entry[0]},{entry[1]}\n")

    def render_leaderboard(self):
        leaderboard_title = self.font.render('Leaderboard', True, (255, 255, 255), (0, 0, 0))  # Letras blancas con subrayado negro
        leaderboard_title_rect = leaderboard_title.get_rect()
        leaderboard_title_rect.center = (SCREEN_WIDTH // 2, 50)
        self.screen.blit(leaderboard_title, leaderboard_title_rect)

        vertical_offset = 100  # Ajuste el desplazamiento vertical inicial
        player_score_displayed = False  # Variable para rastrear si el puntaje del jugador actual se ha mostrado
        for i, entry in enumerate(self.leaderboard):
            name, score = entry
            entry_text = self.smaller_font.render(f"{i + 1}. {name}: {score}", True, (255, 255, 255), (0, 0, 0))
            self.screen.blit(entry_text, (SCREEN_WIDTH // 2 - entry_text.get_width() // 2, vertical_offset))
            vertical_offset += entry_text.get_height() + 10  # Aumentar el desplazamiento vertical
            if score == self.score and not player_score_displayed:  # Verificar si el puntaje del jugador actual coincide
                player_score_displayed = True

        
    def render(self):
        self.screen.fill((0, 0, 0))
        self.background.render(self.screen)

        if self.webcam.lastFrame is not None:
            self.render_camera()

        self.screen.blit(self.player.surf, self.player.rect)
        for e in self.enemies:
            self.screen.blit(e.surf, e.rect)

        display_score = round(self.score / 1000)
        text_score = self.font.render('Puntaje: ' + str(display_score), True, (255, 255, 255), (0, 0, 0))  # Letras blancas
        scoreTextRect = text_score.get_rect()
        scoreTextRect.bottom = SCREEN_HEIGHT - 5
        scoreTextRect.left = 5
        self.screen.blit(text_score, scoreTextRect)

        if self.lost:
            game_over_text = self.font.render('BANDERA ROJA', True, (255, 0, 0), (0, 0, 0))  # Letras rojas
            game_over_text_rect = game_over_text.get_rect()
            game_over_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4 - 40)  # Ajuste vertical
            self.screen.blit(game_over_text, game_over_text_rect)

            retry_text = self.smaller_font.render('Presiona enter para reintentar', True, (255, 255, 0), (0, 0, 0))  # Letras amarillas
            retry_text_rect = retry_text.get_rect()
            retry_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4 + 20)  # Ajuste vertical
            self.screen.blit(retry_text, retry_text_rect)

            # Mostrar puntaje del jugador que perdió debajo del texto de volver a intentarlo
            player_lost_text = self.smaller_font.render(f"Tu puntaje: {round(self.score)}", True, (255, 255, 255), (0, 0, 0))  # Letras blancas
            player_lost_text_rect = player_lost_text.get_rect()
            player_lost_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4 + 60)  # Ajuste vertical
            self.screen.blit(player_lost_text, player_lost_text_rect)

            self.render_leaderboard()  # Renderiza el leaderboard cuando el juego termina

            # Reiniciar puntaje solo si el juego se ha reiniciado
            if not self.started:
                self.score = 0

        if not self.started:
            game_over_text = self.font.render('Presiona enter para iniciar', True, (255, 255, 255), (0, 0, 0))
            game_over_text_rect = game_over_text.get_rect()
            game_over_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.screen.blit(game_over_text, game_over_text_rect)

        if self.webcam.lastFrame is not None:
            self.render_camera()
            
        pygame.display.flip()


    def loop(self):
        with self.mp_face_mesh.FaceMesh(
                static_image_mode=False,
                max_num_faces=1,
                min_detection_confidence=0.5,
                refine_landmarks=True
        ) as self.face_mesh:
            while self.running:
                if not self.lost:
                    if not self.webcam.ready():
                        continue
                    self.process_camera()
                else:
                    self.background_music.stop()

                time = pygame.time.get_ticks()
                delta_time = time - self.last_frame_time
                self.last_frame_time = time
                self.update(delta_time)
                self.render()
                self.clock.tick(60)
            pygame.quit()

    def process_camera(self):
        image = self.webcam.read()
        if image is not None:
            image.flags.writeable = False
            image = cv2.flip(image, 1)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            results = self.face_mesh.process(image)
            self.webcam_image = image
            if results.multi_face_landmarks is not None:
                for face_landmarks in results.multi_face_landmarks:
                    top = (face_landmarks.landmark[10].x, face_landmarks.landmark[10].y)
                    bottom = (face_landmarks.landmark[152].x, face_landmarks.landmark[152].y)
                    self.face_left_x = face_landmarks.landmark[234].x
                    self.face_right_x = face_landmarks.landmark[454].x
                    self.face_top_y = face_landmarks.landmark[10].y
                    self.face_bottom_y = face_landmarks.landmark[152].y
                    self.face_left_x = self.face_left_x - .1
                    self.face_right_x = self.face_right_x + .1
                    self.face_top_y = self.face_top_y - .1
                    self.face_bottom_y = self.face_bottom_y + .1
                    self.detect_head_movement(top, bottom)
            k = cv2.waitKey(1) & 0xFF

    def detect_head_movement(self, top, bottom):
        radians = math.atan2(bottom[1] - top[1], bottom[0] - top[0])
        degrees = math.degrees(radians)
        min_degrees = 70
        max_degrees = 110
        degree_range = max_degrees - min_degrees
        if degrees < min_degrees: degrees = min_degrees
        if degrees > max_degrees: degrees = max_degrees
        self.movement = (((degrees - min_degrees) / degree_range) * 2) - 1

    def render_camera(self):
        if self.face_left_x < 0: self.face_left_x = 0
        if self.face_right_x > 1: self.face_right_x = 1
        if self.face_top_y < 0: self.face_top_y = 0
        if self.face_bottom_y > 1: self.face_bottom_y = 1
        face_surf = pygame.image.frombuffer(self.webcam_image, (int(self.webcam.width()), int(self.webcam.height())), "BGR")
        face_rect = pygame.Rect(
            int(self.face_left_x * self.webcam.width()),
            int(self.face_top_y * self.webcam.height()),
            int(self.face_right_x * self.webcam.width()) - int(self.face_left_x * self.webcam.width()),
            int(self.face_bottom_y * self.webcam.height()) - int(self.face_top_y * self.webcam.height())
        )
        only_face_surf = pygame.Surface((
            int(self.face_right_x * self.webcam.width()) - int(self.face_left_x * self.webcam.width()),
            int(self.face_bottom_y * self.webcam.height()) - int(self.face_top_y * self.webcam.height())
        ))
        only_face_surf.blit(face_surf, (0, 0), face_rect)
        height = only_face_surf.get_rect().height
        width = only_face_surf.get_rect().width
        if width == 0:
            width = 1
        face_ratio = height / width
        face_area_width = 130
        face_area_height = face_area_width * face_ratio
        if face_area_height > self.max_face_surf_height:
            self.max_face_surf_height = face_area_height
        only_face_surf = pygame.transform.scale(only_face_surf, (int(face_area_width), int(self.max_face_surf_height)))
        self.screen.blit(only_face_surf, only_face_surf.get_rect())


class Webcam:
    def __init__(self):
        # Inicialización de variables
        self.stopped = False
        self.stream = None
        self.lastFrame = None
        self.os_name = platform.system()

    def start(self):
        # Actualizar continuamente la captura de la webcam
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # Inicia la captura de video de la webcam
        if self.stream is None:
            if self.os_name == "Windows":
                self.stream = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            elif self.os_name == "Darwin": #macOS
                self.stream = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
            else: # Linux
                self.stream = cv2.VideoCapture(0, cv2.CAP_V4L)
        # Bucle para actualizar continuamente el último fotograma
        while True:
            if self.stopped:
                return
            (result, image) = self.stream.read()
            if not result:
                self.stop()
                return
            self.lastFrame = image
                
    def read(self):
        # Devuelve el último fotograma capturado por la webcam
        return self.lastFrame

    def stop(self):
        # Detiene la captura de la webcam
        self.stopped = True

    def width(self):
        # Obtiene el ancho del fotograma capturado por la webcam
        return self.stream.get(cv2.CAP_PROP_FRAME_WIDTH )

    def height(self):
        # Obtiene la altura del fotograma capturado por la webcam
        return self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT )
    
    def ready(self):
        # Verifica si la webcam está lista y ha capturado al menos un fotograma
        return self.lastFrame is not None
    
if __name__ == "__main__":
    main()