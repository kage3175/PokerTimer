import pygame
from pygame.locals import *

GRAY = (100,100,100)
RED = (255,0,0)

pygame.init()
test = pygame.Rect(0,0,100,100)
screen = pygame.display.set_mode((500,500))
running = True
while running:
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == ord('q'):
        running = False
        pygame.quit()
  pygame.draw.rect(screen, )
