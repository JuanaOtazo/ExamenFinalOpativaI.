import pygame # Importa el módulo principal de Pygame, que permite el desarrollo de juegos y aplicaciones multimedia en Python.
from pygame.locals import * # Importa todas las constantes y clases importantes de Pygame
import random #Importa el módulo random, que proporciona funciones para la generación de números aleatorios.
import os # para realizar tareas comunes relacionadas con el sistema operativo, como manejar archivos.

pygame.init()
pygame.mixer.init()

# Ajustar el directorio de trabajo al del script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Crear la ventana
width = 800  # Aumentar el ancho de la ventana
height = 600  # Aumentar la altura de la ventana
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Game')

# Nuevo color de fondo (azul claro)
background_color = (0, 0, 139)

# Colores adicionales
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# Tamaños de la carretera y los marcadores
road_width = 400  # Aumentar el ancho de la carretera
marker_width = 10
marker_height = 50

# Coordenadas de los carriles
left_lane = 100
center_left_lane = 200
center_right_lane = 300
right_lane = 400
lanes = [left_lane, center_left_lane, center_right_lane, right_lane]  # Actualización de la lista de carriles

# Carretera y marcadores de borde
road = (50, 0, road_width, height)
left_edge_marker = (45, 0, marker_width, height)
right_edge_marker = (445, 0, marker_width, height)

# Para animar el movimiento de los marcadores de carril
lane_marker_move_y = 0

# Coordenadas iniciales del jugador
player_x = 250 #indica que inicialmente el jugador está situado a 250 unidades (píxeles, metros)
player_y = 400 #indica que inicialmente el jugador está ubicado a 400 unidades desde el borde superior del área de juego. 

# Configuración de fotogramas
clock = pygame.time.Clock()
fps = 120

# Configuración del juego
game_over = False
restart = False
paused = False
speed = 3  # aumenta la velocidad #
score = 0
high_score = 0
player_name = ""

#Calcula las dimensiones escaladas (new_width y new_height).
#Asigna la imagen escalada al atributo self.image
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        fixed_width = 45
        fixed_height = 90
        self.image = pygame.transform.scale(image, (fixed_width, fixed_height))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

#Pasa la imagen cargada (image), y las coordenadas (x, y) donde se ubicará el vehículo.
class PlayerVehicle(Vehicle):#Inicialización de la clase base (Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('images/car.png')#Carga la imagen del archivo 'car.png' ubicado en la carpeta 'images' usando pygame.image.load().
        super().__init__(image, x, y)#Llama al constructor de la clase base (Vehicle) utilizando super().__init__().

# Grupos de sprites
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

# Crear el coche del jugador
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# Cargar las imágenes de los vehículos
image_filenames = ['pickup_truck.png', 'semi_trailer.png','car4.png','car1.png','car2.png','taxi.png', 'van.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load('images/' + image_filename)
    vehicle_images.append(image)

# Cargar la imagen del choque
crash = pygame.image.load('images/crash.png')
crash_rect = crash.get_rect()

# Cargar sonidos
collision_sound = None #Esta variable se utilizará para almacenar el objeto de sonido cargado desde el archivo.
try:
    collision_sound = pygame.mixer.Sound('sounds/colision.wav') # es la ruta relativa al archivo de sonido que se intenta cargar. 
except pygame.error as e:
    print(f"No reproduce: {e}")

# Función para dibujar texto
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Pantalla de inicio de sesión
def login_screen():
    global width, height
    
    login = True
    input_box = pygame.Rect(150, 200, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 32)

    # Cargar la imagen de fondo
    background_image = pygame.image.load('images/fondo.png')
    background_image = pygame.transform.scale(background_image, (width, height))

    # Bucle Principal (while login):
    while login:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        login = False
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                        

        screen.blit(background_image, (0, 0))  # Dibujar la imagen de fondo

        # Cambia el color de la letra 
        black = (0, 0, 0)
        draw_text('Ingrese su nombre para iniciar el juego:', font, black, screen, 150, 150)

        
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

    return text

def reset_game():
    global game_over, restart, paused, speed, score, lane_marker_move_y, player_group, vehicle_group, player

    # Reiniciar variables de juego
    game_over = False
    restart = False
    paused = False
    speed = 3
    score = 0
    lane_marker_move_y = 0

    # Vaciar los grupos de sprites
    player_group.empty()    # Vacía el grupo de sprites de jugadores
    vehicle_group.empty()   # Vacía el grupo de sprites de vehículos

    # Crear de nuevo el jugador
    player = PlayerVehicle(player_x, player_y)
    player_group.add(player)

def main():
    global game_over, restart, paused, speed, score, high_score, lane_marker_move_y, player_name

    player_name = login_screen()



    



    # Iniciar la música de fondo después de ingresar el nombre del jugador
    try:
        background_music = 'sounds/carrera.mp3'
        pygame.mixer.music.load(background_music)
        pygame.mixer.music.set_volume(0.5)  # Ajusta el volumen si es necesario
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"Warning: Unable to load background music: {e}")

    # controla el ciclo de vida del juego en Pygame. Mientras game_over sea False, el bucle principal del juego
    #  se ejecuta y maneja los eventos del usuario. Si el usuario decide salir del juego
    #  (presionando la X de la ventana o Escape), o si el juego ya ha terminado y presiona 'r' para reiniciar,
    while True:
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    if event.key == pygame.K_p:
                        paused = not paused

            if not paused:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and player.rect.left > 100:
                    player.rect.x -= 5
                if keys[pygame.K_RIGHT] and player.rect.right < 450:
                    player.rect.x += 5

                lane_marker_move_y += speed
                if lane_marker_move_y >= marker_height * 2:
                    lane_marker_move_y = 0

                screen.fill(background_color)
                pygame.draw.rect(screen, gray, road)
                pygame.draw.rect(screen, yellow, left_edge_marker)
                pygame.draw.rect(screen, yellow, right_edge_marker)

                for lane in lanes:
                    for y in range(marker_height * -2, height, marker_height * 2):
                        pygame.draw.rect(screen, white, (lane - (marker_width // 2), y + lane_marker_move_y, marker_width, marker_height))

                player_group.draw(screen)
                player_group.update()

                if len(vehicle_group) < 2:
                    lane = random.choice(lanes)
                    image = random.choice(vehicle_images)
                    vehicle = Vehicle(image, lane, -100)
                    vehicle_group.add(vehicle)

                for vehicle in vehicle_group:
                    vehicle.rect.y += speed
                    if vehicle.rect.top > height:
                        vehicle.kill()
                        score += 1

                if pygame.sprite.spritecollide(player, vehicle_group, True):
                    if collision_sound:
                        collision_sound.play()
                    game_over = True

                vehicle_group.draw(screen)
                vehicle_group.update()

                if score > high_score:
                    high_score = score

                draw_text(f'Puntuación: {score}', pygame.font.Font(None, 36), white, screen, 10, 10)
                draw_text(f'Mejor puntuación: {high_score}', pygame.font.Font(None, 36), white, screen, 10, 40)
                draw_text(f'Jugador: {player_name}', pygame.font.Font(None, 36), white, screen, 10, 70)

                pygame.display.flip()
                clock.tick(fps)

        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reset_game()
                        game_over = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

            screen.fill(background_color)
            draw_text('¡Game Over!', pygame.font.Font(None, 70), red, screen, 250, 200)
            draw_text('Presiona R para reiniciar o ESC para salir', pygame.font.Font(None, 36), white, screen, 120, 300)
            draw_text(f'Puntuación final: {score}', pygame.font.Font(None, 36), white, screen, 280, 360)

            pygame.display.flip()
            clock.tick(15)

if __name__ == '__main__':
    main()

pygame.quit()
