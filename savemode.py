import time
import pygame
import ctypes
from pygame.locals import *
import os
import timer
from ClassObjs import *
import datetime
import tkinter as tk

K_NUM = [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_KP0, K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9]
BANNED = ["\\", "/", ":", "*", "?", "<", ">", "\"", "|", "left ctrl", "right ctrl", "tab", "`", "+"]
SHIFT = ["left shift", "right shift"]
STRNUM = ["1", "2", "3","4","5","6","7","8","9","0"]

WHITE = (255,255,255)
BLACK = (0,0,0)
PALEGRAY = (210,210,210)
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

TK_VAL = False

def confirmQuit():
  window = tk.Tk()
  window.title('Quit?')
  window.geometry("500x160+200+200")
  window.configure(bg = 'white')
  window.resizable(False, False)
  label = tk.Label(window, font = ("Arial", 25), bg = 'white', text = "Are you sure to Quit?")
  label.place(x=100, y=20)
  yesB = tk.Button(window, width=15, height= 2, relief="raised", overrelief="solid", borderwidth=4, font = ("Arial", 15), text= "Yes", command = lambda: close_window(window, True))
  yesB.place(x = 40, y = 80)
  noB = tk.Button(window, width=15, height= 2, relief="raised", overrelief="solid", borderwidth=4, font = ("Arial", 15), text= "No", command = lambda: close_window(window, False))
  noB.place(x = 280, y = 80)
  window.mainloop()

def close_window(window, isQuit):
  global TK_VAL
  TK_VAL = isQuit
  window.destroy()

def mouseInRect(rectObj, position):
  return rectObj.left <= position[0] <= rectObj.right and rectObj.top <= position[1]<= rectObj.bottom

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
    fontEntry = pygame.font.Font('./font/NanumGothic.ttf', round(100/screenScale))

    textNext = TextObj(font= fontButton, content="Next", position=(midpoint[0] + round(300/screenScale), round(1030/screenScale)), relative="center", color=BLACK)
    textBack = TextObj(font = fontButton, content="Back", color=BLACK, relative="center", position=(midpoint[0] - round(300/screenScale), round(1030/screenScale)))
    textEntryTitle = TextObj(font = fontEntry, content="Enter the Title", color = PALEGRAY, relative="center", position = (midpoint[0], midpoint[1] - round(100/screenScale)))
    textSettingLevel = TextObj(font = fontSup, content="Level", color=WHITE, relative="center", position = (midpoint[0]-round(400/screenScale), round(90/screenScale)))
    textSettingBB = TextObj(font = fontSup, content="BB", color=WHITE, relative="center", position=(midpoint[0] - round(225/screenScale), round(90/screenScale)))
    textSettingSB = TextObj(font = fontSup, content="SB", color=WHITE, relative="center", position=(midpoint[0] - round(50/screenScale), round(90/screenScale)))
    textSettingAnte = TextObj(font = fontSup, content="Ante", color=WHITE, relative="center", position=(midpoint[0] + round(125/screenScale), round(90/screenScale)))
    textSettingDur = TextObj(font = fontSup, content="Duration", color=WHITE, relative="center", position=(midpoint[0] + round(300/screenScale), round(90/screenScale)))

    rectNext = pygame.Rect(0,0,round(500/screenScale),round(140/screenScale))
    rectNext.center = (midpoint[0] + round(300/screenScale), round(1030/screenScale))
    rectBack = pygame.Rect(0,0,round(500/screenScale),round(140/screenScale))
    rectBack.center = (midpoint[0] - round(300/screenScale), round(1030/screenScale))
    rectEntryTitle = pygame.Rect(0,0,round(1500/screenScale),round(250/screenScale))
    rectEntryTitle.center = (midpoint[0], midpoint[1] - round(100/screenScale))
    rectSettings = pygame.Rect(0,0,round(2200/screenScale), round(120/screenScale))

    plusBox = pygame.Rect(0,0,round(900/screenScale),round(50/screenScale))
    plusBox.center = (midpoint[0], round(150/screenScale))
    textPlus = TextObj(font = fontBox, content="+", position=plusBox.center, relative="center", color=BLACK)

    running = True
    gotomain = False

    flagTimer = False
    tempstr = ""
    flagModTitle = False
    flagShift = False
    title = ""
    flagNext = False
    objControl = None

    while running:
      if TK_VAL:
        running = False
        r = False
        gotomain = False
        continue

      if not flagNext:
        for event in pygame.event.get():
          if event.type == KEYDOWN:
            if flagModTitle:
              key = pygame.key.name(event.key)
              key = " " if (key == "space") else key
              key = key[1] if (key[0] == "[") else key
              if key in SHIFT:
                flagShift = True
              elif event.key == K_BACKSPACE:
                if len(tempstr) > 0:
                  tempstr = tempstr[:-1]
                  textEntryTitle.changeContent(font = fontEntry, content = tempstr)
              elif event.key != K_RETURN and key not in BANNED:
                if flagShift:
                  key = "_" if (key == "-") else key
                  if key in STRNUM:
                    key = ""
                  key = key.capitalize()
                tempstr = tempstr + key
                textEntryTitle.changeContent(font = fontEntry, content = tempstr)
              if event.key == K_RETURN:
                flagModTitle = False
            elif event.key == ord('q'):
              confirmQuit()
          elif event.type == KEYUP:
            key = pygame.key.name(event.key)
            if key in SHIFT:
              flagShift = False
          elif event.type == MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            if event.button == 1:
              if mouseInRect(rectEntryTitle, position) and not flagModTitle:
                textEntryTitle.changeContent(font = fontEntry, content = tempstr)
                textEntryTitle.changeColor(BLACK)
                flagModTitle = True
              if flagModTitle and not mouseInRect(rectEntryTitle, position):
                flagModTitle = False
              elif mouseInRect(rectBack, position):
                running = False
                gotomain = True
              if mouseInRect(rectNext, position):
                print(1)
                if tempstr == "":
                  pass
                else:
                  title = tempstr
                  flagNext = True

        screen.blit(imgBackground, (0,0))
        pygame.draw.rect(screen, PALEGRAY, rectNext)
        pygame.draw.rect(screen, GRAY, rectNext, width = 4)
        pygame.draw.rect(screen, PALEGRAY, rectBack)
        pygame.draw.rect(screen, GRAY, rectBack, width = 4)
        pygame.draw.rect(screen, WHITE, rectEntryTitle)
        pygame.draw.rect(screen, GRAY, rectEntryTitle, width=5)
        blitText(screen, textNext, textBack, textEntryTitle)
        pygame.display.flip()

      else: ############################################################## 제목 입력 끝난 다음
        objControl = BlindFile()
        ### box = [isbreak,[rectBoxs], [lvl, dur, bb, sb, ante]]   Break이면 isBreak 0, lvl이면 1 기타(Plus 등)는 2
        lstBoxs = [[2, [plusBox], [textPlus]]] # PlusBox가 항상 마지막 인덱스
        for event in pygame.event.get():
          if event.type == KEYDOWN:
            if event.key == ord('q'):
              confirmQuit()
          if event.type == MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            if event.button == 4 or event.button == 5:
              if event.button == 4 and lstBoxs[0][1][0].top >= 130/screenScale:
                pass
              elif event.button == 5 and lstBoxs[-1][1][0].bottom <= (CUTLINE - 100) / screenScale:
                pass
              else:
                f = -1 if (event.button == 5) else 1
                for lstObj in lstBoxs:
                  for rect in lstObj[1]:
                    rect.top = rect.top + f*round(SCRLLFACTOR / screenScale) #박스
                  for textObj in lstObj[2]:
                    textObj.changePosition(relative = "top", position = (textObj.getRect().centerx, textObj.getRect().top + f*round(SCRLLFACTOR / screenScale))) 
            if event.button == 1:
              if mouseInRect(rectNext, position):
                print("Next")
                '''
                해야함

                objControl.getNumBlinds == 0 이면 안 넘어가게 주의
                '''
              elif mouseInRect(rectBack, position):
                tempstr = ""
                title = ""
                flagModTitle = False
                flagNext = False
                flagShift = False
                textEntryTitle.changeContent(font = fontEntry, content = "Enter the Title")
                textEntryTitle.changeColor(PALEGRAY)
              elif mouseInRect(lstBoxs[-1][1][0], position): ### plusBox 누른경우
                pass
                '''
                해야함

                '''
              '''else: # 글자 클릭했는지 확인
                
                cntBreak, cntLvl = 0, 0
                #tempLst2 = [isbreak,[tempBox], [lvl, dur, bb, sb, ante]]
                cntIdx = 0
                for i in range(len(lstBoxs)):
                  if lstBoxs[0] == 0:
                    cntBreak+=1
                  elif lstBoxs[0] == 1:
                    cntLvl+=1
                    lstBoxs[i][2][0].changeContent(font = fontBox, content = str(cntLvl))
                  if 120/screenScale<lstBoxs[i][1][0].bottom<(CUTLINE)/screenScale: # 화면 안에 나오는 애들 중
                    if lstBoxs[i][0] == 0: #break인 경우
                      if mouseInRect(lstBoxs[i][1][0].getRect(), position):
                        cntLvl+=1
                        lstBoxs[i][1][0].changeContent(font = fontBox, content = str(cntLvl))
                        lstBoxs[i][0] = 1 ###여까지함
                        objControl.changeBlinds(cntIdx, False)
                        ### 작업 해야 함
                    else: # Level인 경우
                      if mouseInRect(boxblinds[1][1].getRect(), position): # Lvl
                        cntBreak+=1
                        boxblinds[1][1].changeContent(font = fontBox, content = "Break")
                        for i in range(3):
                          boxblinds[1][i+3].changeContent(font = fontBox, content = "0")
                        boxblinds[0] = 0
                        objControl.changeBlinds(cntIdx, True)
                        cntLvl-=1
                      elif mouseInRect(boxblinds[1][2].getRect(), position): # Duration
                        boxblinds[2] = 2
                        selectedIdx = cntIdx
                      elif mouseInRect(boxblinds[1][3].getRect(), position): # bb
                        boxblinds[2] = 3
                        selectedIdx = cntIdx
                      elif mouseInRect(boxblinds[1][4].getRect(), position): # sb
                        boxblinds[2] = 4
                        selectedIdx = cntIdx
                      elif mouseInRect(boxblinds[1][5].getRect(), position): # ante
                        boxblinds[2] = 5
                        selectedIdx = cntIdx
                  cntIdx += 1
                if 120/screenScale<plusBox.bottom<(CUTLINE)/screenScale:
                  if mouseInRect(plusBox, position):
                    tempBox = pygame.Rect(0,0,round(900/screenScale),round(50/screenScale))
                    tempBox.center = plusBox.center
                    lvl = TextObj(font = fontBox, content=str(cntLvl+1), color=BLACK, relative="center", position=(midpoint[0] - round(400/screenScale), tempBox.centery))
                    dur = TextObj(font = fontBox, content='10', color=BLACK, relative="center", position=(midpoint[0] + round(300/screenScale), tempBox.centery))
                    bb = TextObj(font = fontBox, content='0', color=BLACK, relative="center", position=(midpoint[0] - round(225/screenScale), tempBox.centery))

                    sb = TextObj(font = fontBox, content='0', color=BLACK, relative="center", position=(midpoint[0] - round(50/screenScale), tempBox.centery))
                    ante = TextObj(font = fontBox, content='0', color=BLACK, relative="center", position=(midpoint[0] + round(125/screenScale), tempBox.centery))
                    lstBoxBlinds.append([1,[tempBox, lvl, dur, bb, sb, ante], 0])
                    plusBox.top = plusBox.top + BLINDINTERVAL/screenScale
                    textPlus.changePosition(relative="top", position=(textPlus.getRect().centerx,textPlus.getRect().top + BLINDINTERVAL/screenScale))
                    objControl.addLevel()'''
        screen.blit(imgBackground, (0,0))
        pygame.draw.rect(screen, PALEGRAY, rectNext)
        pygame.draw.rect(screen, GRAY, rectNext, width = 4)
        pygame.draw.rect(screen, PALEGRAY, rectBack)
        pygame.draw.rect(screen, GRAY, rectBack, width = 4)
        blitText(screen, textNext, textBack)
        pygame.draw.rect(screen, DARKGRAY, rectSettings)
        pygame.draw.line(screen, BLACK, (0,round(120/screenScale)), (round(2200/screenScale),round(120/screenScale)), width=5)
        pygame.draw.line(screen,WHITE, (0,round(CUTLINE/screenScale)), (round(2048/screenScale),round(CUTLINE/screenScale)))
        for i in range(len(lstBoxs)):
          if 120/screenScale<lstBoxs[i][1][0].bottom<(CUTLINE)/screenScale:
            for rect in lstBoxs[i][1]:
              pygame.draw.rect(screen, GRAY, rect)
              pygame.draw.rect(screen, BLACK, rect, width=4)
            for text in lstBoxs[i][2]:
              screen.blit(text.getText(), text.getRect())
        blitText(screen, textSettingLevel, textSettingBB, textSettingAnte, textSettingDur, textSettingSB, textPlus)
        pygame.display.flip()

    r = False
    pygame.quit()
    if gotomain:
      return True
    if flagTimer:
      flag=timer.main()
      if flag == 0:
        r = False
      else: r = True
    else:
      return False