import pygame
from pygame.locals import *

def mouseInRect(rectObj, position):
  return rectObj.left <= position[0] <= rectObj.right and rectObj.top <= position[1]<= rectObj.bottom

pygame.init()
clock = pygame.time.Clock()

WIDTH = 500
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('test')
img = pygame.image.load("./img/test.png")
rectImg = img.get_rect()
rectImg.center = (round(WIDTH/2), round(HEIGHT/2))

MOVE = False
running = True

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      pygame.quit()
    elif event.type == MOUSEBUTTONDOWN and event.button == 1:
      pygame.mouse.get_rel()
      position = pygame.mouse.get_pos()
      if mouseInRect(rectImg, position):
        MOVE = True
    elif event.type == MOUSEBUTTONUP and event.button == 1:
      MOVE = False
    elif event.type == MOUSEMOTION:
      if MOVE:
        x,y,z = pygame.mouse.get_pressed()
        if x:
          mx, my = pygame.mouse.get_rel()
          rectImg.x += mx
          rectImg.y += my
          rectImg.top = 0 if rectImg.top < 0 else rectImg.top
          rectImg.left = 0 if rectImg.left < 0 else rectImg.left
          rectImg.bottom = HEIGHT if rectImg.bottom > HEIGHT else rectImg.bottom
          rectImg.right = WIDTH if rectImg.right > HEIGHT else rectImg.right
  screen.fill((255,255,255))
  screen.blit(img, rectImg)
  pygame.display.flip()
  clock.tick(60)