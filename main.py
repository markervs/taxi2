import pygame
import pygame as pg

width = 700
height = 450
FPS = 60
background_color = (255, 255, 255)

pg.init()
screen = pg.display.set_mode([width, height])

timer = pg.time.Clock()

run = True
while run:
    # Обробка подій
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Поновлення
    pygame.display.flip()
    # Відображення
    screen.fill(background_color)


pygame.quit()
