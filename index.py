import pygame
import random

WIDTH, HEIGHT = 640, 480
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

BRICK_IMAGE = pygame.image.load("Assets/img/brick.png")
BRICK = pygame.transform.scale(BRICK_IMAGE, (32, 32))
CRATE_IMAGE = pygame.image.load("Assets/img/crate.png")
CRATE = pygame.transform.scale(CRATE_IMAGE, (32, 32))
FLOOR_IMAGE = pygame.image.load("Assets/img/floor.png")
FLOOR = pygame.transform.scale(FLOOR_IMAGE, (32, 32))
PLAYER_IMAGE = pygame.image.load("Assets/img/player.png")

MUTE_IMAGE = pygame.image.load("Assets/img/mute.png")
MUTE = pygame.transform.scale(MUTE_IMAGE, (32, 32))
PLAY_IMAGE = pygame.image.load("Assets/img/play.png")
PLAY = pygame.transform.scale(PLAY_IMAGE, (32, 32))

PLAYER_FRONT_STILL = PLAYER_IMAGE.subsurface(pygame.Rect(0, 3, 30, 30))
PLAYER_LEFT_STILL = PLAYER_IMAGE.subsurface(pygame.Rect(0, 35, 30, 30))
PLAYER_BACK_STILL = PLAYER_IMAGE.subsurface(pygame.Rect(0, 70, 30, 30))
PLAYER_RIGHT_STILL = PLAYER_IMAGE.subsurface(pygame.Rect(0, 100, 30, 30))

PLAYER_FRONT_WALK = [PLAYER_IMAGE.subsurface(pygame.Rect(30*i, 135, 30, 30)) for i in range(10)]
PLAYER_LEFT_WALK = [PLAYER_IMAGE.subsurface(pygame.Rect(30*i, 165, 30, 30)) for i in range(10)]
PLAYER_BACK_WALK = [PLAYER_IMAGE.subsurface(pygame.Rect(30*i, 195, 30, 30)) for i in range(10)]
PLAYER_RIGHT_WALK = [PLAYER_IMAGE.subsurface(pygame.Rect(30*i, 230, 30, 30)) for i in range(10)]

player_x = 200
player_y = 200
player_speed = 3
player_hitbox = pygame.Rect(player_x, player_y, 26, 30)
walking_index = 0
walking_timer = 0
last_direction = "down"
moving = False
footstep = 14
play_music = True

map_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]




pygame.display.set_caption("Sokoban")
pygame.mixer.init()

FOOTSTEPS_SOUNDS = [
    pygame.mixer.Sound("Assets/sounds/foot_1.wav"),
    pygame.mixer.Sound("Assets/sounds/foot_2.wav"),
    pygame.mixer.Sound("Assets/sounds/foot_3.wav"),
    pygame.mixer.Sound("Assets/sounds/foot_4.wav"),
    pygame.mixer.Sound("Assets/sounds/foot_5.wav"),
]

def play_random_footstep_sound():
    global FOOTSTEPS_SOUNDS
    random_sound = random.choice(FOOTSTEPS_SOUNDS)
    random_sound.play()

def create_collision(tile_x, tile_y):
    global player_hitbox, last_direction, player_x, player_y
    block_hitbox = pygame.Rect(tile_x, tile_y, 32, 32)

    if player_hitbox.colliderect(block_hitbox):
        if last_direction in ["up", "down"]:
            if last_direction == "up":
                player_y = block_hitbox.bottom
            elif last_direction == "down":
                player_y = block_hitbox.top - player_hitbox.height
        elif last_direction in ["left", "right"]:
            if last_direction == "left":
                player_x = block_hitbox.right
            elif last_direction == "right":
                player_x = block_hitbox.left - player_hitbox.width


def draw_window():
    global last_direction, player_x, player_y, key
    for row in range(int(HEIGHT / 32)):
        for col in range(int(WIDTH / 32)):
            tile_x = col * 32
            tile_y = row * 32
            tile = map_data[row][col]
            if tile == 0:
                WIN.blit(FLOOR, (tile_x, tile_y))
            elif tile == 1:
                WIN.blit(BRICK, (tile_x, tile_y))
                create_collision(tile_x, tile_y)
            elif tile == 2:
                WIN.blit(CRATE, (tile_x, tile_y))
                create_collision(tile_x, tile_y) 
                if key[pygame.K_e]:
                    update_crate(tile_x, tile_y)
            elif tile == 3:
                WIN.blit(OBJECTIVE, (tile_x, tile_y))
            
    draw_player()
            
    pygame.display.update()

def update_crate(tile_x, tile_y):
    global last_direction, player_x, player_y, map_data
    
    if last_direction == "up": 
        map_data[tile_y - 1][tile_x] = 2
        map_data[tile_y][tile_x] = 0
    elif last_direction == "down":
        map_data[tile_y + 1][tile_x] = 2
        map_data[tile_y][tile_x] = 0
    elif last_direction == "left":
        map_data[tile_y][tile_x - 1] = 2
        map_data[tile_y][tile_x] = 0
    elif last_direction == "right":
        map_data[tile_y][tile_x + 1] = 2
        map_data[tile_y][tile_x] = 0

    

def draw_player():
    global walking_index, walking_timer, player_x, player_y, key, last_direction, moving, player_speed, footstep, player_hitbox
    
    if key[pygame.K_UP] or key[pygame.K_z]:
        player_y -= player_speed
        WIN.blit(PLAYER_BACK_WALK[walking_index], (player_x, player_y))
        last_direction = "up"
        moving = True
    elif key[pygame.K_DOWN] or key[pygame.K_s]:
        player_y += player_speed
        WIN.blit(PLAYER_FRONT_WALK[walking_index], (player_x, player_y))
        last_direction = "down"
        moving = True
    elif key[pygame.K_LEFT] or key[pygame.K_q]:
        player_x -= player_speed
        WIN.blit(PLAYER_LEFT_WALK[walking_index], (player_x, player_y))
        last_direction = "left"
        moving = True
    elif key[pygame.K_RIGHT] or key[pygame.K_d]:
        player_x += player_speed
        WIN.blit(PLAYER_RIGHT_WALK[walking_index], (player_x, player_y))
        last_direction = "right"
        moving = True
    else: 
        moving = False
    
    if moving == False:
        footstep = 14
        if last_direction == "up":
            WIN.blit(PLAYER_BACK_STILL, (player_x, player_y))
        elif last_direction == "down":
            WIN.blit(PLAYER_FRONT_STILL, (player_x, player_y))
        elif last_direction == "left":
            WIN.blit(PLAYER_LEFT_STILL, (player_x, player_y))
        elif last_direction == "right":
            WIN.blit(PLAYER_RIGHT_STILL, (player_x, player_y))

    player_hitbox = pygame.Rect(player_x, player_y, 24, 28)

    if moving:
        footstep += 1
        if(footstep == 15):
            footstep = 0
            play_random_footstep_sound()

    walking_timer += 1
    if walking_timer >= 2.5:
        walking_timer = 0
        walking_index = (walking_index + 1) % len(PLAYER_FRONT_WALK)

def main():
    global player_x, player_y, key, idle_index, idle_timer
    player = pygame.Rect(0, 0, 0, 0)
    run = True
    clock = pygame.time.Clock()


    pygame.mixer.music.load("Assets/music/background.wav")
    pygame.mixer.music.play(-1)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        key = pygame.key.get_pressed()

        draw_window()

    pygame.quit()

if __name__ == "__main__":
    main()