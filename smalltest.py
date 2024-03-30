import pygame
import time
import ctypes
from pygame.locals import *
from ClassObjs import *

start = time.time()

pygame.init()
  
clock = pygame.time.Clock()
FPS = 60
total_fps = 0

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
print(screensize)
midpoint = screensize[0] / 2, screensize[1] / 2 # 화면 중앙점
screenScale = 1152/screensize[1]
screen = pygame.display.set_mode(screensize, FULLSCREEN)
fontTest = pygame.font.Font('./font/NanumGothic.ttf', round(50/screenScale))
test1 = TextObj(font = fontTest, content="test1", position=(midpoint[0], midpoint[1] - 50), relative="center", color=WHITE)
test2 = TextObj(font = fontTest, content="test2", position=(midpoint[0], midpoint[1] - 100), relative="center", color=WHITE)
tests = [test1, test2]
flagStop = False
while True:
  clock.tick(10)
  total_fps+=1
  if not flagStop:
    for test in tests:
      test.changePosition(relative="center", position=[test.getPos()[0], test.getPos()[1] - 2 * (total_fps % 2)])
  else:
    if time.time() - stopTime >= 1:
      flagStop = False
      stopTime = 0
      for i in range(2):
        tests[i].changePosition(relative="center", position=(midpoint[0], midpoint[1] - 50 * (i+1)))
  if tests[-1].getPos()[1] <= midpoint[1] - 200 and not flagStop:
    stopTime = time.time()
    flagStop = True
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == ord('q'):
        pygame.quit()
  screen.fill(BLACK)
  for test in tests:
    screen.blit(test.getText(), test.getRect())
  pygame.display.flip()