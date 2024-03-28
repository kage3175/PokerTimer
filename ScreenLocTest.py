import pygame
from ClassObjs import *
import ctypes


pygame.init()

clock = pygame.time.Clock()
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
print(screensize)
midpoint = screensize[0] / 2, screensize[1] / 2 # 화면 중앙점
screenScale = 1152/screensize[1]
screen = pygame.display.set_mode()

img = pygame.image.load('./img/Aria_Style.png')
img = pygame.transform.scale(img, screensize)

while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
    elif event.type == KEYDOWN:
      if event.key == ord('q'):
        pygame.quit()
    elif event.type == MOUSEBUTTONDOWN:
      if event.button == 1:
        position = pygame.mouse.get_pos()
        print(position)

  screen.blit(img, (0,0))
  pygame.display.flip()
  clock.tick(FPS)
