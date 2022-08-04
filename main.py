from cv2 import cvtColor
from vehicles import *
import cv2 as cv
import random
import numpy as np
import pygame


altura = 900
largura = 900
gray = (50, 50, 50)
black = (0, 0, 0)
white = (255, 255, 255)
fps = 60

img = cv.imread("cic.png")
img = cv.resize(img, [900, 900])
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

print(img_gray)

bs = []
particules = []
for i in range(0, len(img_gray), 10):
    for j in range(0, len(img_gray[i]), 10):
        bs.append(float(img_gray[i][j]))
        b = float(img_gray[i][j])
        raio = (b / 255) * 5
        particules.append(Particle(raio, j, i))


pygame.init()
relogio = pygame.time.Clock()
window = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Steering Behaviors")
window.fill(gray)
continua = True
while continua:
    target2 = pygame.mouse.get_pos()
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

    
    window.fill(gray)

    for v in particules:
        
        D = v.position - target2
        if D.magnitude_squared() < 900:
            v.repulsion(target2)
        else:
            v.seek(target=v.initial_position)
        pygame.draw.circle(window, white, v.position, v.b)

    relogio.tick(fps)
    pygame.display.update()
pygame.quit()



