import pygame
from pygame.locals import *
import time
import random
import ctypes
import os

FONTPATH = {'NGothicR' : './font/NanumGothic.ttf', 'NSquareR' : './font/NanumSquareR.ttf'}
TESTMIN, TESTSEC, TESTTOTAL = 1,10,70

BLACK = (0,0,0)
WHITE = (255,255,255)

def timeupdate(minute, second, total, amount):
  if total < amount:
    minute, second, total = 0,0,0
  elif amount >= 0:
    if second < amount:
      minute -= (amount // 60 + 1)
      second = second + 60 - amount % 60
      total -= amount
    else:
      second -= amount
      total -= amount
  else: #### amount가 음수일 때, 즉 시간을 증가시킬 때
    pass
  return minute, second, total

def makeTimerString(min, sec, total):
  return str(min).zfill(2) + ':' + str(sec).zfill(2)

def levelupdate(amount):
  pass 

def main():
  running = True
  pygame.init()
  
  user32 = ctypes.windll.user32
  screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
  print(screensize)
  surface = pygame.display.set_mode(screensize, FULLSCREEN)
  surface.fill(BLACK)

  fontMainTimer = pygame.font.Font(FONTPATH['NGothicR'], 32)

  start_time = time.time()
  timer = 0
  pause_time = 0
  min, sec, total = TESTMIN, TESTSEC,TESTTOTAL
  strTimer = makeTimerString(min, sec, total)
  textMainTimer = fontMainTimer.render(strTimer, True, WHITE)

  while running:
    for event in pygame.event.get():
      if event.type == KEYDOWN:
        if event.key == ord('q'):
          pygame.quit()
          running = False
        if event.key==pygame.K_ESCAPE:
          surface = pygame.display.set_mode((500,500))
    #####
    if(time.time() - start_time + pause_time > timer):
      timer+=1
      min, sec, total = timeupdate(min, sec, total, 1)
      strTimer = makeTimerString(min, sec, total)
      textMainTimer = fontMainTimer.render(strTimer, antialias=True, color=WHITE)
    surface.blit(textMainTimer, (200,200))
    pygame.display.flip()

main()
