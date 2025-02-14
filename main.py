import pygame
import pygame as pg
from Tools.demo.spreadsheet import center

width = 700
height = 450
FPS = 60
background_color = (255, 255, 255)

images_dict = {
    'bg': pg.image.load('img/Background.png'),
    'player': {
        'rear': pg.image.load('img/cab_rear.png'),
        'left': pg.image.load('img/cab_left.png'),
        'right': pg.image.load('img/cab_right.png'),
        'front': pg.image.load('img/cab_front.png'),
    },
    'hole': pg.image.load('img/hole.png'),
    'hotel': pg.image.load('img/hotel.png'),
    'pas': pg.image.load('img/passenger.png'),
    'screen': pg.image.load('img/screenshot.jpg'),
    't_bg': pg.image.load('img/taxi_background.png'),

}

# taxi
player_view = 'rear'
player_rect = images_dict['player'][player_view].get_rect()
player_rect.x = 300
player_rect.y = 300



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
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                x_direction = 1
                player_view = 'right'
            elif event.key == pg.K_LEFT:
                x_direction = -1
                player_view = 'left'
            elif event.key == pg.K_UP:
                y_direction = -1
                player_view = 'rear'
            elif event.key == pg.K_DOWN:
                y_direction = 1
                player_view = 'front'




    # Поновлення

    # Відображення
    screen.fill(background_color)
    screen.blit(images_dict['bg'], (0, 0))


    screen.blit(images_dict['player'][player_view], player_rect)

    hotel_rect = images_dict['hotel'].get_rect()
    hotel_rect.x = 350
    hotel_rect.y = 300
    screen.blit(images_dict['hotel'], hotel_rect)


    pygame.display.flip()


pygame.quit()
