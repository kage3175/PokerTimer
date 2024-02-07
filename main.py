import time
import pygame
import ctypes
from pygame.locals import *
import loadmode, savemode

WHITE = (255,255,255)
BLACK = (0,0,0)
PALEGRAY = (150,150,150)
GRAY = (200,200,200)


def main():
  flagRun = True
  while flagRun:

    pygame.init()
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
    midpoint = screensize[0] / 2, screensize[1] / 2 # 화면 중앙점
    screenScale = 1152/screensize[1]
    screen = pygame.display.set_mode()
    imgBackground = pygame.image.load("./img/background.jpg")
    imgBackground = pygame.transform.scale(imgBackground, screensize)

    fontButton = pygame.font.Font('./font/NanumSquareB.ttf', round(100/screenScale))

    locSave = (midpoint[0], midpoint[1] - round(200/screenScale))
    locLoad = (midpoint[0], midpoint[1] + round(200/screenScale))

    textSave = fontButton.render("New Structure", True, BLACK)
    objSave = textSave.get_rect()
    objSave.center = locSave
    textLoad = fontButton.render("Load", True, BLACK)
    objLoad = textLoad.get_rect()
    objLoad.center = locLoad


    rectSave = pygame.Rect(0,0,round(800/screenScale),round(300/screenScale))
    rectSave.center = locSave
    rectSaveOutline = pygame.Rect(0,0,round(800/screenScale),round(300/screenScale))
    rectSaveOutline.center = locSave
    rectLoad = pygame.Rect(0,0,round(800/screenScale),round(300/screenScale))
    rectLoad.center = locLoad
    rectLoadOutline = pygame.Rect(0,0,round(800/screenScale),round(300/screenScale))
    rectLoadOutline.center = locLoad

    mode = 0
    running = True
    while running:
      for event in pygame.event.get():
        if event.type == KEYDOWN:
          if event.key == ord('q'):
            running = False
            mode = 0
            flagRun=False
          elif event.key == K_SPACE:
            pass
        if event.type == MOUSEBUTTONDOWN:
          position = pygame.mouse.get_pos()
          #print(position)
          if(rectSave.left<=position[0]<=rectSave.right and rectSave.top <= position[1] <= rectSave.bottom):
            print("Save")
            mode = 2
            running = False
          if(rectLoad.left<=position[0]<=rectLoad.right and rectLoad.top <= position[1] <= rectLoad.bottom):
            #print("Load")
            mode = 1
            running = False
      screen.blit(imgBackground,(0,0))
      pygame.draw.rect(screen, PALEGRAY, rectSave)
      pygame.draw.rect(screen, GRAY, rectSaveOutline, width = 4)
      screen.blit(textSave, objSave)
      pygame.draw.rect(screen, PALEGRAY, rectLoad)
      pygame.draw.rect(screen, GRAY, rectLoadOutline, width = 4)
      screen.blit(textLoad, objLoad)
      pygame.display.flip()

    pygame.quit()
    if mode == 0:
      pass
    elif mode == 1: # Loadmode
      flagRun = loadmode.main_load()
    elif mode == 2: # Savemode
      flagRun = savemode.main_save()
################ End of main

main()