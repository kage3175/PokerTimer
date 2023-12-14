import timer
import time
import pygame
import ctypes
from pygame.locals import *

WHITE = (255,255,255)
BLACK = (0,0,0)


def main():
  pygame.init()
  user32 = ctypes.windll.user32
  screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
  midpoint = screensize[0] / 2, screensize[1] / 2 # 화면 중앙점
  screenScale = 1152/screensize[1]
  screen = pygame.display.set_mode()
  imgBackground = pygame.image.load("./img/background.jpg")
  imgBackground = pygame.transform.scale(imgBackground, screensize)
  
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == KEYDOWN:
        if event.key == ord('q'):
          running = False
        elif event.key == K_SPACE:
          pass
      if event.type == MOUSEBUTTONDOWN:
        position = pygame.mouse.get_pos()
        print(position)
    screen.blit(imgBackground,(0,0))
    pygame.display.flip()

main()