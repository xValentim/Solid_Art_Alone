from tracemalloc import start
from cv2 import cvtColor
from vehicles import *
import cv2 as cv
import random
import numpy as np
import pygame
import sys


altura = 720
largura = 720
gray = (50, 50, 50)
black = (0, 0, 0)
white = (255, 255, 255)
background = white
ball_color = gray
fps = 60

<<<<<<< HEAD
img = cv.imread("cic.png")
img = cv.resize(img, [600, 600])
cv.imshow('img', img)
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
=======
if len(sys.argv) != 2:
    print("Error Usage. You must type this form: python main.py path_image")
else:
    filename = sys.argv[1]
    # img = cv.imread("assets/alexia.png")
    img = cv.imread(filename)
    img = cv.resize(img, [720, 720])
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
>>>>>>> faster_processing

    print(img.shape)
    t = 0
    bs = []
    particules = []
    on_move = set()
    for i in range(0, len(img_gray), 3):
        for j in range(0, len(img_gray[i]), 3):
            bs.append(float(img_gray[i][j]))
            b = 256 - float(img_gray[i][j])
            color = img[i][j]
            color[0], color[-1] = color[-1], color[0]
            raio = (b / 255) * 4
            if raio >= 1.4:
                particules.append(Particle(raio, j, i, ball_color))
    print(len(particules))
    pygame.init()
    relogio = pygame.time.Clock()
    window = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Steering Behaviors")
    window.fill(gray)
    continua = True
    while continua:

        # Random Walker
        # target2 += pygame.Vector2(random.uniform(-5, 5), random.uniform(-5, 5))

        target2 = pygame.mouse.get_pos()
        # if target2[0] >= largura-10 or target2[0] <= 10 or target2[1] >= altura - 10 or target2[1] <= 10:
        #     target2 = pygame.Vector2(-200, -200)
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                continua = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    continua = False
                if event.key == pygame.K_r:
                    for v in particules:
                        v.position = pygame.Vector2(v.initial_position)

        
        window.fill(background)

        for v in particules:
            
            D = v.position - target2
            if D.magnitude_squared() < 2000:
                v.repulsion(target2)
                if v not in on_move:
                    on_move.add(v)
            elif v in on_move:
                v.seek(target=v.initial_position)
                if v.flag_on_move:
                    on_move.remove(v)
            pygame.draw.circle(window, v.color, v.position, v.b)



        t += 1
        # x = ("0"*(5 - len(str(t)))) + str(t)
        # pygame.image.save(window, f"output/{x}_screenshot.png")
        relogio.tick(fps)
        pygame.display.update()
    pygame.quit()



