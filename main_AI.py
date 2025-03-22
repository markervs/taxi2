from collections import defaultdict
from email.policy import default

import pygame
import pygame as pg
import random
import numpy as np
from Tools.demo.spreadsheet import center

width = 700
height = 450
FPS = 60
background_color = (255, 255, 255)

x_direction = 0
y_direction = 0
player_speed = 2

images_dict = {
    'bg': pg.image.load('img/Background.png'),
    'player': {
        'rear': pg.image.load('img/cab_rear.png'),
        'left': pg.image.load('img/cab_left.png'),
        'right': pg.image.load('img/cab_right.png'),
        'front': pg.image.load('img/cab_front.png'),
    },
    'hole': pg.image.load('img/hole.png'),
    'hotel':pg.transform.scale(pg.image.load('img/hotel.png'),(80, 80)),
    'pas': pg.image.load('img/passenger.png'),
    'screen': pg.image.load('img/screenshot.jpg'),
    't_bg': pg.transform.scale(pg.image.load('img/taxi_background.png'), (80, 45)),
    'parking': pg.transform.scale(pg.image.load('img/Image20250301115336.png'), (80, 45))

}

# taxi
player_view = 'rear'
player_rect = images_dict['player'][player_view].get_rect()
player_rect.x = 300
player_rect.y = 300

hotel_rect = images_dict['hotel'].get_rect()
hotel_positions = [
    (60, 30),
    (555, 30),
    (60, 250),
    (555, 250)
]
pas_img = images_dict['pas']
pas_rect = pas_img.get_rect()
# pas_positions = [
#     (60, 30),
#     (555, 30),
#     (60, 365),
#     (555, 250)
# ]


hotel_rect.x, hotel_rect.y = random.choice(hotel_positions)

pas_rect.x, pas_rect.y = random.choice(hotel_positions)
pas_rect.y += hotel_rect.height
# while (pas_rect.x, pas_rect.y) == (hotel_rect.x, hotel_rect.y):
#     pass

actions = [0, 1, 2, 3] # 0 - right, 1 - left, 2 - up, 3 - bottom
Q_table = defaultdict(lambda: [0, 0, 0, 0]) # (300, 300) : [-2, -3, 5, 3]

learning_rate = 0.9
discount_factor = 0.9
epsilon = 0.1

def choose_action(state):
    if random.random() < epsilon:
        return random.choice(actions)
    else:
        return np.argmax(Q_table[state])

def update_q(state, action, reward, next_step):
    best_next = max(Q_table[next_step])
    Q_table[state][action] += learning_rate * (reward + discount_factor * best_next - Q_table[state][action])

def make_step():
    current_state = (player_rect.x, player_rect.y)
    action = choose_action(current_state)
    apply_action(action)
    draw()
    reward = -1
    episode_end = False
    success = False

    if is_crash():
        reward = -100
        episode_end = True

    if parking_rect.contains(player_rect):
        # draw_message("You win!!", pg.Color('green'))
        print("Win!")
        reward = 100
        episode_end = True
        success = True
    next_state = (player_rect, player_rect.y)

    update_q(current_state, action, reward, next_state)

    return (episode_end, success)







def apply_action(action):
    global x_direction, y_direction, player_view
    x_direction = 0
    y_direction = 0
    if action == 0:
        x_direction = 1
        player_view = 'right'
    elif action == 1:
        x_direction = -1
        player_view = 'left'
    elif action == 2:
        y_direction = -1
        player_view = 'rear'
    elif action == 3:
        y_direction = 1
        player_view = 'front'

def draw_message(text, color):
    font = pg.font.SysFont(None, 36)
    message = font.render(text, True, color)
    screen.blit(message, (300, 150))
    pg.display.flip()
    pg.time.delay(1500)



def is_crash():
    for x in range(player_rect.x, player_rect.topright[0], 1):
        for y in range(player_rect.y, player_rect.bottomleft[1], 1):
            try:
                if screen.get_at((x,y)) == (220, 215, 177):
                    return True
            except IndexError:
                print("pixel index out of range")
    return False


#parking
parking_img = images_dict['parking']
parking_rect = parking_img.get_rect()
parking_rect.x, parking_rect.y = hotel_rect.x, hotel_rect.y + hotel_rect.height



pg.init()
screen = pg.display.set_mode([width, height])

timer = pg.time.Clock()

run = True
while run:
    timer.tick(FPS)
    # Обробка подій
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            # pygame.quit()
            # exit()
        # if event.type == pg.KEYDOWN:
        #     if event.key == pg.K_RIGHT:
        #         x_direction = 1
        #         player_view = 'right'
        #     elif event.key == pg.K_LEFT:
        #         x_direction = -1
        #         player_view = 'left'
        #     elif event.key == pg.K_UP:
        #         y_direction = -1
        #         player_view = 'rear'
        #     elif event.key == pg.K_DOWN:
        #         y_direction = 1
        #         player_view = 'front'

    # keys_klava = pg.key.get_pressed()
    # if keys_klava[pg.K_RIGHT]:
    #     x_direction = 1
    #     player_view = 'right'
    # elif keys_klava[pg.K_LEFT]:
    #     x_direction = -1
    #     player_view = 'left'
    # elif keys_klava[pg.K_UP]:
    #     y_direction = -1
    #     player_view = 'rear'
    # elif keys_klava[pg.K_DOWN]:
    #     y_direction = 1
    #     player_view = 'front'




    # Поновлення
    player_rect.x += player_speed * x_direction
    player_rect.y += player_speed * y_direction
    x_direction = 0
    y_direction = 0

    if is_crash():
        print("IS CRASH")
        draw_message("You crash!!", pg.Color('red'))
        player_view = 'rear'
        player_rect.x = 300
        player_rect.y = 300

        hotel_rect.x, hotel_rect.y = random.choice(hotel_positions)
        parking_rect.x, parking_rect.y = hotel_rect.x, hotel_rect.y + hotel_rect.height
        pas_rect.x, pas_rect.y = random.choice(hotel_positions)
        pas_rect.y += hotel_rect.height
        continue


    if player_rect.colliderect(pas_rect):
        pas_rect.x, pas_rect.y = player_rect.x, player_rect.y

    if parking_rect.contains(player_rect):
        draw_message("You win!!", pg.Color('green'))
        player_view = 'rear'
        player_rect.x = 300
        player_rect.y = 300

        hotel_rect.x, hotel_rect.y = random.choice(hotel_positions)
        parking_rect.x, parking_rect.y = hotel_rect.x, hotel_rect.y + hotel_rect.height
        pas_rect.x, pas_rect.y = random.choice(hotel_positions)
        pas_rect.y += hotel_rect.height
        continue

    # Відображення
    screen.fill(background_color)


def draw():
    screen.blit(images_dict['bg'], (0, 0))

    screen.blit(images_dict['player'][player_view], player_rect)
    screen.blit(images_dict['hotel'], hotel_rect)
    screen.blit(parking_img, parking_rect)
    screen.blit(images_dict['pas'], pas_rect)

    pygame.display.flip()


pygame.quit()
