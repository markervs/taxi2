import pygame
import pygame as pg
import random
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
    't_bg': pg.transform.scale(pg.image.load('img/taxi_background.png'), (80, 45))

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
hotel_rect.x, hotel_rect.y = random.choice(hotel_positions)

#parking
parking_img = images_dict['t_bg']
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

    keys_klava = pg.key.get_pressed()
    if keys_klava[pg.K_RIGHT]:
        x_direction = 1
        player_view = 'right'
    elif keys_klava[pg.K_LEFT]:
        x_direction = -1
        player_view = 'left'
    elif keys_klava[pg.K_UP]:
        y_direction = -1
        player_view = 'rear'
    elif keys_klava[pg.K_DOWN]:
        y_direction = 1
        player_view = 'front'




    # Поновлення
    player_rect.x += player_speed * x_direction
    player_rect.y += player_speed * y_direction
    x_direction = 0
    y_direction = 0


    # Відображення
    screen.fill(background_color)
    screen.blit(images_dict['bg'], (0, 0))


    screen.blit(images_dict['player'][player_view], player_rect)
    screen.blit(images_dict['hotel'], hotel_rect)
    screen.blit(parking_img, parking_rect)


    pygame.display.flip()


pygame.quit()
