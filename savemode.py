import time
import pygame
import ctypes
from pygame.locals import *
import os
import timer
from ClassObjs import *
import datetime

K_NUM = [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_KP0, K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9]

WHITE = (255,255,255)
BLACK = (0,0,0)
PALEGRAY = (150,150,150)
GRAY = (200,200,200)
SELECTED = (200,50,50)
DARKGRAY = (75,75,75)
BLINDGRAY = (175,175,175)
BREAKGRAY = (215,215,215)

CUTLINE = 900
BOXHEIGHT = 210
SCRLLFACTOR = 25
BOXINTERVAL = 240
BLINDINTERVAL = 60

def main_save():
  r = True
  
  while r:
    pygame.init()
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
    midpoint = screensize[0] / 2, screensize[1] / 2 # 화면 중앙점
    screenScale = 1152/screensize[1]
    screen = pygame.display.set_mode()
    imgBackground = pygame.image.load("./img/background.jpg")
    imgBackground = pygame.transform.scale(imgBackground, screensize)

    fontTitle = pygame.font.Font('./font/NanumGothic.ttf', round(60/screenScale))
    fontEmpty = pygame.font.Font('./font/NanumGothic.ttf', round(120/screenScale))
    fontSup = pygame.font.Font('./font/NanumGothic.ttf', round(30/screenScale))
    fontButton = pygame.font.Font('./font/NanumGothicBold.ttf', round(80/screenScale))
    fontBox = pygame.font.Font('./font/NanumGothic.ttf', round(20/screenScale))

    textNext = TextObj(font= fontButton, content="Next", position=(midpoint[0] + round(300/screenScale), round(1030/screenScale)), relative="center", color=BLACK)
    textBack = TextObj(font = fontButton, content="Back", color=BLACK, relative="center", position=(midpoint[0] - round(300/screenScale), round(1030/screenScale)))

    rectNext = pygame.Rect(0,0,round(500/screenScale),round(140/screenScale))
    rectNext.center = (midpoint[0] + round(300/screenScale), round(1030/screenScale))
    rectBack = pygame.Rect(0,0,round(500/screenScale),round(140/screenScale))
    rectBack.center = (midpoint[0] - round(300/screenScale), round(1030/screenScale))

    running = True
    gotomain = False
    while running:
      for event in pygame.event.get():
        if event.type == KEYDOWN:
          if event.key == ord('q'):
            running = False
            gotomain = False
            r = False

      screen.blit(imgBackground, (0,0))
      pygame.draw.rect(screen, PALEGRAY, rectNext)
      pygame.draw.rect(screen, GRAY, rectNext, width = 4)
      screen.blit(textNext.getText(), textNext.getRect())
      pygame.draw.rect(screen, PALEGRAY, rectBack)
      pygame.draw.rect(screen, GRAY, rectBack, width = 4)
      screen.blit(textBack.getText(), textBack.getRect())
      pygame.display.flip()
      time.sleep(0.05)

    
    if not gotomain:
      r = False
      pygame.quit()
    else:
      pass