import time
import pygame
import ctypes
from pygame.locals import *
import loadmode, savemode
import tkinter as tk
from ClassObjs import *


TK_VAL = False

def confirmQuit():
  window = tk.Tk()
  window.title('Quit?')
  screen_width = window.winfo_screenwidth()
  screen_height = window.winfo_screenheight()
  width,height = 500,160

  x = (screen_width - width) // 2
  y = (screen_height - height) // 2 - 50
  window.geometry(f"{width}x{height}+{x}+{y}")
  window.configure(bg = 'white')
  window.resizable(False, False)
  label = tk.Label(window, font = ("Arial", 25), bg = 'white', text = "Are you sure to Quit?")
  label.place(y=20, relx = 0.5, anchor='n')
  yesB = tk.Button(window, width=15, height= 2, relief="raised", overrelief="solid", borderwidth=4, font = ("Arial", 15), text= "Yes", command = lambda: close_window(window, True))
  yesB.place(y = 75, relx=0.25, anchor='n')
  noB = tk.Button(window, width=15, height= 2, relief="raised", overrelief="solid", borderwidth=4, font = ("Arial", 15), text= "No", command = lambda: close_window(window, False))
  noB.place(y = 75, relx=0.75, anchor='n')
  window.mainloop()

def close_window(window, isQuit):
  global TK_VAL
  TK_VAL = isQuit
  window.destroy()

def mouseInRect(rectObj, position):
  return rectObj.left <= position[0] <= rectObj.right and rectObj.top <= position[1]<= rectObj.bottom


def main():
  flagRun = True
  while flagRun:

    pygame.init()
    clock = pygame.time.Clock()
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
    midpoint = screensize[0] / 2, screensize[1] / 2 # 화면 중앙점
    screenScale = 1152/screensize[1]
    screen = pygame.display.set_mode()
    imgBackground = pygame.image.load("./img/background.jpg")
    imgBackground = pygame.transform.scale(imgBackground, screensize)
    imgSettings = pygame.image.load("./img/settings.png")
    imgSettings = pygame.transform.scale(imgSettings,(round(100/screenScale),round(100/screenScale)))
    imgBar = pygame.image.load("./img/test.png")

    shutCenter = (screensize[0] - round(50/screenScale), round(50 /screenScale))
    shutRadius = 17

    fontButton = pygame.font.Font('./font/NanumSquareB.ttf', round(100/screenScale))

    locSave = (midpoint[0], midpoint[1] - round(200/screenScale))
    locLoad = (midpoint[0], midpoint[1] + round(200/screenScale))
    locSettings = (screensize[0] - round(70 /screenScale), screensize[1] - round(70 / screenScale))

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
    rectSettings = imgSettings.get_rect()
    rectSettings.center = locSettings
    rectBar = imgBar.get_rect()
    rectBar.center = (midpoint[0] + round(100/screenScale), midpoint[1])

    mode = 0
    running = True
    flagSettings = False
    barMove = False

    vol = 0.5
    while running:
      if TK_VAL:
        running = False
        mode = 0
        flagRun=False
      for event in pygame.event.get():
        if event.type == KEYDOWN:
          if event.key == ord('q'):
            confirmQuit()
          elif event.key == K_SPACE:
            pass
          if event.key == ord('b') and flagSettings:
            flagSettings = False
            barMove = False
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
          position = pygame.mouse.get_pos()
          if not flagSettings:
            if mouseInRect(rectSave, position):
              mode = 2
              running = False
            elif mouseInRect(rectLoad, position):
              mode = 1
              running = False
            elif (((position[0] - shutCenter[0]) ** 2 + (position[1] - shutCenter[1]) ** 2) ** 0.5 <= shutRadius):
              confirmQuit()
            elif mouseInRect(rectSettings, position):
              flagSettings = True
              settingfile = open("./doc/settings", "r")
              vol = float(settingfile.readline().replace("\n", ""))
              settingfile.close()
              rectBar.centerx = midpoint[0] - round(400/screenScale) + round(vol * 1000)
          else:
            pygame.mouse.get_rel()
            if mouseInRect(rectBar, position):
              barMove = True
        elif event.type == MOUSEMOTION and flagSettings and barMove:
          x,y,z = pygame.mouse.get_pressed()
          if x:
            mx, my = pygame.mouse.get_rel()
            rectBar.x += mx
            if rectBar.centerx < midpoint[0] - round(400/screenScale):
              rectBar.centerx = midpoint[0] - round(400/screenScale)
            if rectBar.centerx > midpoint[0] + round(600/screenScale):
              rectBar.centerx = midpoint[0] + round(600/screenScale)
        elif event.type == MOUSEBUTTONUP and flagSettings and barMove:
          barMove = False
          vol = (rectBar.centerx - midpoint[0] + 400/screenScale) / float(1000)
          outfile = open("./doc/settings", "w")
          outfile.write(str(vol))
          outfile.close()

      screen.blit(imgBackground,(0,0))
      if not flagSettings:
        pygame.draw.rect(screen, PALEGRAY, rectSave)
        pygame.draw.rect(screen, DARKGRAY, rectSaveOutline, width = 6)
        screen.blit(textSave, objSave)
        pygame.draw.rect(screen, PALEGRAY, rectLoad)
        pygame.draw.rect(screen, DARKGRAY, rectLoadOutline, width = 6)
        screen.blit(textLoad, objLoad)
        pygame.draw.circle(screen, RED, shutCenter, shutRadius)
        pygame.draw.circle(screen, BLACK, shutCenter, shutRadius, width = 2)
        screen.blit(imgSettings, rectSettings)
      else:
        pygame.draw.line(screen, WHITE, (midpoint[0] - round(400/screenScale), midpoint[1]), (midpoint[0] + round(600/screenScale), midpoint[1]), width=4)
        screen.blit(imgBar, rectBar)
      pygame.display.flip()
      clock.tick(FPS)

    pygame.quit()
    settingfile = open("./doc/settings", "r")
    vol = float(settingfile.readline().replace("\n", ""))
    settingfile.close()
    if mode == 0:
      pass
    elif mode == 1: # Loadmode
      flagRun = loadmode.main_load(vol)
    elif mode == 2: # Savemode
      flagRun = savemode.main_save(vol)
################ End of main

if __name__ == "__main__":
  main()