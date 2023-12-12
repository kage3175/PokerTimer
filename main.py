import pygame
from pygame.locals import *
import time
import random
import ctypes
import os

def main():
  running = True
  pygame.init()
  surface = pygame.display.set_mode((500,500))
  background = pygame.image.load('./img/background.jpg')
  while True:
    for event in pygame.event.get():
      if event.type == KEYDOWN:
        if event.key == ord('f'):
          user32 = ctypes.windll.user32
          screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
          scaled_img = pygame.transform.scale(background, screensize)
          surface = pygame.display.set_mode(screensize, FULLSCREEN)
        if event.key == ord('q'):
          pygame.quit()
        if event.key==pygame.K_ESCAPE:
          surface = pygame.display.set_mode((500,500))
    #####
    surface.blit(background, (0,0))
    pygame.display.flip()

main()
