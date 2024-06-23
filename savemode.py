import time
import pygame
import ctypes
from pygame.locals import *
import os
import timer
from ClassObjs import *
import datetime
import tkinter as tk
import timer_simple

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
  label = tk.Label(window, font = ("./font/NanumGothicBold.ttf", 25), bg = 'white', text = "Are you sure to Quit?")
  label.place(y=20, relx = 0.5, anchor='n')
  yesB = tk.Button(window, width=15, height= 2, relief="raised", overrelief="solid", borderwidth=4, font = ("./font/NanumGothic.ttf", 15), text= "Yes", command = lambda: close_window(window, True))
  yesB.place(y = 75, relx=0.25, anchor='n')
  noB = tk.Button(window, width=15, height= 2, relief="raised", overrelief="solid", borderwidth=4, font = ("./font/NanumGothic.ttf", 15), text= "No", command = lambda: close_window(window, False))
  noB.place(y = 75, relx=0.75, anchor='n')
  window.mainloop()

def close_window(window, isQuit):
  global TK_VAL
  TK_VAL = isQuit
  window.destroy()

def caution(text = "Caution"):
  window = tk.Tk()
  window.title('Error')
  screen_width = window.winfo_screenwidth()
  screen_height = window.winfo_screenheight()
  width,height = 500,160

  x = (screen_width - width) // 2
  y = (screen_height - height) // 2 - 50
  window.geometry(f"{width}x{height}+{x}+{y}")
  window.configure(bg = 'white')
  window.resizable(False, False)
  label = tk.Label(window, font = ("./font/NanumGothicBold.ttf", 25), bg = 'white', text = text)
  label.place(y=20, anchor='n', relx=0.5)
  yesB = tk.Button(window, width=40, height= 2, relief="raised", overrelief="solid", borderwidth=4, font = ("./font/NanumGothic.ttf", 15), text= "Okay", command = lambda: close_window(window, False))
  yesB.place(y = 75, relx=0.5, anchor='n')
  window.mainloop()
  
def key2char(eventKey):
  key = pygame.key.name(eventKey)
  key = " " if (key == "space") else key
  key = key[1] if (key[0] == "[") else key
  return key

def main_save(vol, style):
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

    shutCenter = (screensize[0] - round(50/screenScale), round(50 /screenScale))
    shutRadius = 17

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
    textSettingBB = TextObj(font = fontSup, content="BB", color=WHITE, relative="center", position=(midpoint[0] - round(50/screenScale), round(90/screenScale)))
    textSettingSB = TextObj(font = fontSup, content="SB", color=WHITE, relative="center", position=(midpoint[0] - round(225/screenScale), round(90/screenScale)))
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
    selectedIdx = -1
    temp_input = 0
    tabbedOnly = False

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
              key = key2char(event.key)
              if key in SHIFT:
                flagShift = True
              elif event.key == K_BACKSPACE:
                if len(tempstr) > 0:
                  tempstr = tempstr[:-1]
                  textEntryTitle.changeContent(font = fontEntry, content = tempstr)
              elif len(key) >= 2:
                pass
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
                if tempstr == "":
                  pass
                else:
                  title = tempstr
                  flagNext = True
                  lstBoxs = [[2, [plusBox], [textPlus], 0]] # PlusBox가 항상 마지막 인덱스
              elif (((position[0] - shutCenter[0]) ** 2 + (position[1] - shutCenter[1]) ** 2) ** 0.5 <= shutRadius):
                confirmQuit()
        screen.blit(imgBackground, (0,0))
        pygame.draw.rect(screen, PALEGRAY, rectNext)
        pygame.draw.rect(screen, GRAY, rectNext, width = 4)
        pygame.draw.rect(screen, PALEGRAY, rectBack)
        pygame.draw.rect(screen, GRAY, rectBack, width = 4)
        pygame.draw.rect(screen, WHITE, rectEntryTitle)
        pygame.draw.rect(screen, GRAY, rectEntryTitle, width=5)
        blitText(screen, textNext, textBack, textEntryTitle)
        pygame.draw.circle(screen, RED, shutCenter, shutRadius)
        pygame.draw.circle(screen, BLACK, shutCenter, shutRadius, width = 2)
        pygame.display.flip()

      else: ############################################################## 제목 입력 끝난 다음
        
        ### box = [isbreak,[rectBoxs], [lvl, dur, bb, sb, ante], clickedIdx]   Break이면 isBreak 0, lvl이면 1 기타(Plus 등)는 2
        for event in pygame.event.get():
          if event.type == KEYDOWN:
            if event.key == ord('q'):
              confirmQuit()
            elif selectedIdx != -1:
              if event.key in K_NUM or event.key == K_BACKSPACE:
                temp_input = (temp_input*10 + processAscii(event.key)) if (event.key in K_NUM) else (temp_input//10)
                str_input = f"{temp_input:,}"
                lstBoxs[selectedIdx][2][lstBoxs[selectedIdx][3]].changeContent(font = fontBox, content = str_input)
                tabbedOnly = False
              elif pygame.key.name(event.key) == "return" or pygame.key.name(event.key) == "enter":
                lstBoxs[selectedIdx][3] = 0
                selectedIdx = -1
                temp_input = 0
                tabbedOnly = False
              elif event.key == K_TAB:
                if selectedIdx == len(lstBoxs)-2 and lstBoxs[selectedIdx][3] == 1:
                  lstBoxs[selectedIdx][3] = 0
                  if not tabbedOnly:
                    temp_input = 1 if (temp_input <= 0) else temp_input
                    str_input = f"{temp_input:,}"
                    lstBoxs[selectedIdx][2][1].changeContent(font = fontBox, content = str_input)
                  selectedIdx = -1
                elif lstBoxs[selectedIdx][3] != 1: #Duration이 선택된게 아닌 경우
                  if not tabbedOnly:
                    str_input = f"{temp_input:,}"
                    lstBoxs[selectedIdx][2][lstBoxs[selectedIdx][3]].changeContent(font = fontBox, content = str_input)
                  tabbedOnly = True
                  if lstBoxs[selectedIdx][3] != 4:
                    lstBoxs[selectedIdx][3] = lstBoxs[selectedIdx][3] + 1
                  else:
                    lstBoxs[selectedIdx][3] = 1
                  temp_input = 0
                else: #Duration이 선택됐던 경우
                  if not tabbedOnly:
                    temp_input = 1 if (temp_input == 0) else temp_input
                    str_input = f"{temp_input:,}"
                    lstBoxs[selectedIdx][2][lstBoxs[selectedIdx][3]].changeContent(font = fontBox, content = str_input)
                  tabbedOnly = True
                  lstBoxs[selectedIdx][3] = 0
                  selectedIdx += 1
                  f = -1
                  for lstObj in lstBoxs:
                    for rect in lstObj[1]:
                      rect.top = rect.top + f*round(BLINDINTERVAL / screenScale) #박스
                    for textObj in lstObj[2]:
                      textObj.changePosition(relative = "top", position = (textObj.getRect().centerx, textObj.getRect().top + f*round(BLINDINTERVAL / screenScale)))
                    try:
                      lstObj[4].top = lstObj[4].top + f*round(BLINDINTERVAL / screenScale)
                    except:
                      pass
                  if lstBoxs[selectedIdx][0] == 0: #Break
                    lstBoxs[selectedIdx][3] = 1
                    temp_input = 0
                  else:
                    lstBoxs[selectedIdx][3] = 2
                    temp_input = 0
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
                  try:
                    lstObj[4].top = lstObj[4].top + f*round(SCRLLFACTOR / screenScale)
                  except:
                    pass
            if event.button == 1:
              if selectedIdx != -1:
                if not tabbedOnly:
                  temp_input = 1 if lstBoxs[selectedIdx][3] == 1 and temp_input <= 0 else temp_input
                  str_input = f"{temp_input:,}"
                  lstBoxs[selectedIdx][2][lstBoxs[selectedIdx][3]].changeContent(font = fontBox, content = str_input)
                lstBoxs[selectedIdx][3] = 0
                selectedIdx = -1
                temp_input = 0
              elif mouseInRect(rectNext, position):   #Next 버튼을 눌렀을 때
                if len(lstBoxs) <= 1:
                  caution("You need at least one level")
                else:
                  objControl = BlindFile()
                  filename = title + "_" + str(round(time.time())) + '.bld'
                  structueType = 1
                  numBlinds = len(lstBoxs) - 1
                  templst = []
                  #tempLst2 = [isbreak,[tempBox], [lvl, dur, bb, sb, ante], clickedIdx]
                  for i in range(numBlinds):
                    isBreak = lstBoxs[i][0]
                    dur = int(lstBoxs[i][2][1].getContent())
                    bb = int(lstBoxs[i][2][2].getContent())
                    sb = int(lstBoxs[i][2][3].getContent())
                    ante = int(lstBoxs[i][2][4].getContent())
                    templst.append([isBreak, dur, bb, sb, ante])
                  objControl.make_deNovo(filename=filename, title=title, type=structueType, numBlinds=numBlinds, lstBlinds=templst)
                  updateFile(objControl)
                  flagTimer = True
                  running = False
                  templst = objControl.getLstBlinds()
                  lstLevel = [0]
                  lstBlind = [0]
                  title = objControl.getTitle()
                  for item in templst:
                    lstLevel.append(item[1])
                    if item[1] == 0:
                      lstBlind.append(0)
                    else:
                      lstBlind.append(item[2:5])
              elif mouseInRect(rectBack, position):
                tempstr = ""
                title = ""
                flagModTitle = False
                flagNext = False
                flagShift = False
                textEntryTitle.changeContent(font = fontEntry, content = "Enter the Title")
                textEntryTitle.changeColor(PALEGRAY)
              elif (((position[0] - shutCenter[0]) ** 2 + (position[1] - shutCenter[1]) ** 2) ** 0.5 <= shutRadius):
                confirmQuit()
              else: # 글자 클릭했는지 확인
                
                cntBreak, cntLvl = 0, 0
                flagUp = False
                idxDelete = 0
                #tempLst2 = [isbreak,[tempBox], [lvl, dur, bb, sb, ante], clickedIdx, rectDelete]
                for i in range(len(lstBoxs)):
                  if flagUp:
                    try:
                      lstBoxs[i][4].top = lstBoxs[i][4].top - round(BLINDINTERVAL/screenScale)
                      lstBoxs[i][1][0].top = lstBoxs[i][1][0].top - round(BLINDINTERVAL/screenScale) #박스
                      
                      for j in range(5):
                        lstBoxs[i][2][j].changePosition(relative = "top", position = (lstBoxs[i][2][j].getRect().centerx, lstBoxs[i][2][j].getRect().top - round(BLINDINTERVAL/screenScale)))
                    except:  #### plusBox의 케이스
                      pass
                  if lstBoxs[i][0] == 0:
                    cntBreak+=1
                  elif lstBoxs[i][0] == 1:
                    cntLvl+=1
                    lstBoxs[i][2][0].changeContent(font = fontBox, content = str(cntLvl))
                  if 120/screenScale<lstBoxs[i][1][0].bottom<(CUTLINE)/screenScale: # 화면 안에 나오는 애들 중
                    try:
                      if mouseInRect(lstBoxs[i][4], position) and not flagUp:
                        flagUp = True
                        idxDelete = i
                        if lstBoxs[i][0] == 1:
                          cntLvl -= 1
                        continue
                    except:   ### plusBox인 경우는 오류가 나니까
                      pass
                    if lstBoxs[i][0] == 0: #break인 경우
                      if mouseInRect(lstBoxs[i][2][0].getRect(), position):
                        cntLvl+=1
                        lstBoxs[i][2][0].changeContent(font = fontBox, content = str(cntLvl))
                        lstBoxs[i][0] = 1
                      elif mouseInRect(lstBoxs[i][2][1].getRect(), position): #Break Duration
                        lstBoxs[i][3] = 1
                        selectedIdx = i
                        tabbedOnly = True
                    elif lstBoxs[i][0] == 1: # Level인 경우
                      if mouseInRect(lstBoxs[i][2][0].getRect(), position): # Lvl
                        cntBreak+=1
                        lstBoxs[i][2][0].changeContent(font = fontBox, content = "Break")
                        for j in range(3):
                          lstBoxs[i][2][j+2].changeContent(font = fontBox, content = "0")
                        lstBoxs[i][0] = 0
                        cntLvl-=1
                      elif mouseInRect(lstBoxs[i][2][1].getRect(), position): # Duration
                        lstBoxs[i][3] = 1
                        selectedIdx = i
                      elif mouseInRect(lstBoxs[i][2][2].getRect(), position): # bb
                        lstBoxs[i][3] = 2
                        selectedIdx = i
                      elif mouseInRect(lstBoxs[i][2][3].getRect(), position): # sb
                        lstBoxs[i][3] = 3
                        selectedIdx = i
                      elif mouseInRect(lstBoxs[i][2][4].getRect(), position): # ante
                        lstBoxs[i][3] = 4
                        selectedIdx = i
                      tabbedOnly = True if selectedIdx != -1 else False
                    else: # PlusBox
                      if 120/screenScale<lstBoxs[i][1][0].bottom<(CUTLINE)/screenScale and mouseInRect(lstBoxs[i][1][0], position):
                        tempBox = pygame.Rect(0,0,round(900/screenScale),round(50/screenScale))
                        tempBox.center = lstBoxs[i][1][0].center
                        rectDelete = pygame.Rect(0,0,round(25/screenScale), round(25/screenScale))
                        rectDelete.center = (tempBox.centerx + round(480/screenScale), tempBox.centery)
                        lvl = TextObj(font = fontBox, content=str(cntLvl+1), color=BLACK, relative="center", position=(midpoint[0] - round(400/screenScale), tempBox.centery))
                        dur = TextObj(font = fontBox, content='10', color=BLACK, relative="center", position=(midpoint[0] + round(300/screenScale), tempBox.centery))
                        bb = TextObj(font = fontBox, content='0', color=BLACK, relative="center", position=(midpoint[0] - round(225/screenScale), tempBox.centery))

                        sb = TextObj(font = fontBox, content='0', color=BLACK, relative="center", position=(midpoint[0] - round(50/screenScale), tempBox.centery))
                        ante = TextObj(font = fontBox, content='0', color=BLACK, relative="center", position=(midpoint[0] + round(125/screenScale), tempBox.centery))
                        lstBoxs[i][1][0].top = lstBoxs[i][1][0].top + BLINDINTERVAL/screenScale
                        lstBoxs[i][2][0].changePosition(relative="top", position=(lstBoxs[i][2][0].getRect().centerx,lstBoxs[i][2][0].getRect().top + BLINDINTERVAL/screenScale))
                        templst = lstBoxs.pop()
                        lstBoxs.append([1,[tempBox], [lvl, dur, bb, sb, ante], 0, rectDelete])
                        lstBoxs.append(templst)
                if flagUp:
                  lstBoxs[-1][1][0].top = lstBoxs[-1][1][0].top - round(BLINDINTERVAL/screenScale)
                  lstBoxs[-1][2][0].changePosition(relative = "top", position=(lstBoxs[-1][2][0].getRect().centerx, lstBoxs[-1][2][0].getRect().top - round(BLINDINTERVAL/screenScale)))
                  flagUp = False
                  lstBoxs.pop(idxDelete)
        screen.blit(imgBackground, (0,0))
        pygame.draw.rect(screen, PALEGRAY, rectNext)
        pygame.draw.rect(screen, GRAY, rectNext, width = 4)
        pygame.draw.rect(screen, PALEGRAY, rectBack)
        pygame.draw.rect(screen, GRAY, rectBack, width = 4)
        blitText(screen, textNext, textBack)
        for i in range(len(lstBoxs)):
          if 120/screenScale<lstBoxs[i][1][0].bottom<(CUTLINE)/screenScale:
            
            if lstBoxs[i][0] == 0: #Break의 경우
              pygame.draw.rect(screen, WHITE, lstBoxs[i][1][0])
              pygame.draw.rect(screen, BLACK, lstBoxs[i][1][0], width=4)
              
              #screen.blit(lstBoxs[i][2][0].getText(), lstBoxs[i][2][0].getRect())
              if lstBoxs[i][3] != 0:
                pygame.draw.rect(screen, GRAY, lstBoxs[i][2][lstBoxs[i][3]].getRect())
              blitText(screen, lstBoxs[i][2][0], lstBoxs[i][2][1])
            else:
              for rect in lstBoxs[i][1]:
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, BLACK, rect, width=4)
              for text in lstBoxs[i][2]:
                screen.blit(text.getText(), text.getRect())
              if lstBoxs[i][3] != 0: # 무언가 클릭됐을 때
                pygame.draw.rect(screen, WHITE, lstBoxs[i][2][lstBoxs[i][3]].getRect())
                blitText(screen, lstBoxs[i][2][lstBoxs[i][3]])
            try:
              pygame.draw.rect(screen, RED, lstBoxs[i][4])  ### Delete button
              pygame.draw.rect(screen, BLACK, lstBoxs[i][4], width = 3)
            except:
              pass
        pygame.draw.rect(screen, DARKGRAY, rectSettings)
        pygame.draw.line(screen, BLACK, (0,round(120/screenScale)), (round(2200/screenScale),round(120/screenScale)), width=5)
        pygame.draw.line(screen,WHITE, (0,round(CUTLINE/screenScale)), (round(2048/screenScale),round(CUTLINE/screenScale)))
        blitText(screen, textSettingLevel, textSettingBB, textSettingAnte, textSettingDur, textSettingSB, textPlus)
        pygame.draw.circle(screen, RED, shutCenter, shutRadius)
        pygame.draw.circle(screen, BLACK, shutCenter, shutRadius, width = 2)
        pygame.display.flip()

    r = False
    pygame.quit()
    if gotomain:
      return True
    if flagTimer:
      if style == 1:
        flag = timer_simple.main(lstBlind, lstLevel, title, True, vol)
      else:
        flag = timer.main(lstBlind, lstLevel, title, True, vol)
      if flag == 0:
        r = False
      else: r = True
    else:
      return False