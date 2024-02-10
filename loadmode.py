import time
import pygame
import ctypes
from pygame.locals import *
import os
import timer
from ClassObjs import *
import tkinter as tk

PALEGRAY = (150,150,150)

TK_VAL = False

def mouseInRect(rectObj, position):
  return rectObj.left <= position[0] <= rectObj.right and rectObj.top <= position[1]<= rectObj.bottom

  
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

def main_load(vol):
  global TK_VAL
  user32 = ctypes.windll.user32
  screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
  midpoint = screensize[0] / 2, screensize[1] / 2 # 화면 중앙점
  screenScale = 1152/screensize[1]
  r = True

  while r:
    r = False
    pygame.init()

    fontTitle = pygame.font.Font('./font/NanumGothic.ttf', round(60/screenScale))
    fontEmpty = pygame.font.Font('./font/NanumGothic.ttf', round(120/screenScale))
    fontSup = pygame.font.Font('./font/NanumGothic.ttf', round(30/screenScale))
    fontButton = pygame.font.Font('./font/NanumGothicBold.ttf', round(80/screenScale))
    fontBox = pygame.font.Font('./font/NanumGothic.ttf', round(20/screenScale))
    
    screen = pygame.display.set_mode()
    imgBackground = pygame.image.load("./img/background.jpg")
    imgBackground = pygame.transform.scale(imgBackground, screensize)

    shutCenter = (screensize[0] - round(50/screenScale), round(50 /screenScale))
    shutRadius = 17

    flagEmpty = False
    lstBlindObjs = []
    lstTextBlinds = []
    lstRectBlinds = []
    lstRectBackgrounds = []
    lstBoxBlinds=[] # (rect, text_blindbreak, text_level, text_SB, text_BB, text_Ante, up, down, delete)
    lstLevel, lstBlind = [],[]
    selected = -1
    
    dictType = {1:"BB Ante", 2:"All Ante"}
    

    try:
      lst_blindfiles = os.listdir('./doc')
      numFile = len(lst_blindfiles) -1  ## Setting 하나 빼야함
    except Exception as e:
      print("Error occured while opening and listdir: ", e)
    
    if numFile==0:
      flagEmpty = True
    else:
      lstTag = [False for _ in range(numFile)]
      cnt = 0
      for name in lst_blindfiles:
        if name[-4] != ".":
          continue
        file = open('./doc/'+name, "r")
        obj = BlindFile()
        obj.make(file)
        obj.putFilename(name)
        file.close()
        lstBlindObjs.insert(0,obj)

        tempTitle = fontTitle.render(obj.getTitle(), True, BLACK)
        objTemp = tempTitle.get_rect()
        objTemp.topleft = (round(545/screenScale), round((110+cnt*BOXINTERVAL)/screenScale))
        tempType = fontSup.render("Type: " + dictType[obj.getType()], True, BLACK)
        objType = tempType.get_rect()
        objType.topleft = (round(550/screenScale), round((185+cnt*BOXINTERVAL)/screenScale))
        tempStr = ""
        tempLst = obj.getLstDurations()
        for i in range(len(tempLst)-1):
          tempStr = tempStr + str(tempLst[i]) + " / "
        tempStr = tempStr + str(tempLst[-1]) + " min"
        tempDurations = fontSup.render("Durations: " + tempStr, True, BLACK)
        objDurations = tempDurations.get_rect()
        objDurations.topleft = (round(550/screenScale), round((220+cnt*BOXINTERVAL)/screenScale))

        lstTextBlinds.insert(0,(tempTitle,tempType, tempDurations))
        lstRectBlinds.insert(0,(objTemp,objType, objDurations))

        tempRect = pygame.Rect(0,0,round(1000/screenScale),round(BOXHEIGHT/screenScale))
        tempRect.topleft = (round(525/screenScale), round((100+cnt*BOXINTERVAL)/screenScale))
        tempRectOutline = pygame.Rect(0,0,round(1000/screenScale),round(BOXHEIGHT/screenScale))
        tempRectOutline.topleft = (round(525/screenScale), round((100+cnt*BOXINTERVAL)/screenScale))
        lstRectBackgrounds.insert(0,(tempRect, tempRectOutline))
        cnt+=1
    #### End of reading files

  #region texts  

    textEmpty = TextObj(font= fontEmpty, content="There is no saved blind settings", position=midpoint, relative="center", color=WHITE)
    textNext = TextObj(font= fontButton, content="Next", position=(midpoint[0] + round(300/screenScale), round(1030/screenScale)), relative="center", color=BLACK)
    textBack = TextObj(font = fontButton, content="Back", color=BLACK, relative="center", position=(midpoint[0] - round(300/screenScale), round(1030/screenScale)))
    textSavenGo = TextObj(font=fontButton, content="Next", color=BLACK, relative="center", position=(midpoint[0] + round(300/screenScale), round(1030/screenScale)))
    textSettingLevel = TextObj(font = fontSup, content="Level", color=WHITE, relative="center", position = (midpoint[0]-round(400/screenScale), round(90/screenScale)))
    textSettingBB = TextObj(font = fontSup, content="BB", color=WHITE, relative="center", position=(midpoint[0] - round(225/screenScale), round(90/screenScale)))
    textSettingSB = TextObj(font = fontSup, content="SB", color=WHITE, relative="center", position=(midpoint[0] - round(50/screenScale), round(90/screenScale)))
    textSettingAnte = TextObj(font = fontSup, content="Ante", color=WHITE, relative="center", position=(midpoint[0] + round(125/screenScale), round(90/screenScale)))
    textSettingDur = TextObj(font = fontSup, content="Duration", color=WHITE, relative="center", position=(midpoint[0] + round(300/screenScale), round(90/screenScale)))

  #endregion

    rectNext = pygame.Rect(0,0,round(500/screenScale),round(140/screenScale))
    rectNext.center = (midpoint[0] + round(300/screenScale), round(1030/screenScale))
    rectBack = pygame.Rect(0,0,round(500/screenScale),round(140/screenScale))
    rectBack.center = (midpoint[0] - round(300/screenScale), round(1030/screenScale))
    rectSettings = pygame.Rect(0,0,round(2200/screenScale), round(120/screenScale))

    running = True

    
    gotomain = False
    flagNext = False
    flagTimer = False
    title=""
    selectedIdx = -1
    temp_input = 0
    objControl = None
    flagFirst = False

    while running:
      if TK_VAL:
        running = False
        gotomain = False
        continue
      if not flagNext: #### 아직 flag를 누르기 전, 그러니까 기존 Blind Structure에서 고르는 단계 
        for event in pygame.event.get():
          if event.type == KEYDOWN:
            if event.key == ord('q'):
              confirmQuit()
              if TK_VAL:
                running = False
                gotomain = False
          if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:# Left Click
              position = pygame.mouse.get_pos()
              if mouseInRect(rectNext, position): #Next Button
                flagNext = True
                flagFirst = True
                objControl = lstBlindObjs[selected]
                #print(objControl.getLstBlinds())
                tempLst = objControl.getLstBlinds()
                level = 1
                cnt = 0
                lstBoxBlinds = []
                for i in range(objControl.getNumBlinds()):
                  tempBox = pygame.Rect(0,0,round(900/screenScale),round(50/screenScale))
                  tempBox.center = (midpoint[0], round((150+cnt*BLINDINTERVAL)/screenScale))
                  rectDelete = pygame.Rect(0,0,round(25/screenScale), round(25/screenScale))
                  rectDelete.center = (midpoint[0] + round(480/screenScale), round((150+cnt*BLINDINTERVAL)/screenScale))
                  if tempLst[i][0] == 0:
                    lvl = TextObj(font = fontBox, content = "Break", color=BLACK, relative="center", position=(midpoint[0]-round(400/screenScale), round((150+cnt*BLINDINTERVAL)/screenScale)))
                  else:
                    lvl = TextObj(font = fontBox, content = str(level), color=BLACK, relative= "center", position=(midpoint[0]-round(400/screenScale), round((150+cnt*BLINDINTERVAL)/screenScale)))
                  dur = TextObj(font = fontBox, color=BLACK, content=str(tempLst[i][1]), relative="center", position=(midpoint[0] + round(300/screenScale), round((150+cnt*BLINDINTERVAL)/screenScale)))
                  bb = TextObj(font = fontBox, color=BLACK, content=str(tempLst[i][2]), relative="center", position=(midpoint[0] - round(225/screenScale), round((150+cnt*BLINDINTERVAL)/screenScale)))
                  sb = TextObj(font = fontBox, color=BLACK, content=str(tempLst[i][3]), relative="center", position=(midpoint[0] - round(50/screenScale), round((150+cnt*BLINDINTERVAL)/screenScale)))
                  ante = TextObj(font = fontBox, color=BLACK, content=str(tempLst[i][4]), relative="center", position=(midpoint[0] + round(125/screenScale), round((150+cnt*BLINDINTERVAL)/screenScale)))
                  isbreak = 0 if tempLst[i][0] == 0 else 1
                  level = level+1 if tempLst[i][0] == 1 else level
                  tempLst2 = [isbreak,[tempBox, lvl, dur, bb, sb, ante],0, rectDelete]
                    
                  lstBoxBlinds.append(tempLst2)
                  cnt+=1
                updateFile(objControl)
                plusBox = pygame.Rect(0,0,round(900/screenScale),round(50/screenScale))
                plusBox.center = (midpoint[0], round((150+cnt*BLINDINTERVAL)/screenScale))
                textPlus = TextObj(font = fontBox, content="+", position=plusBox.center, relative="center", color=BLACK)
              elif mouseInRect(rectBack, position): #Back Button
                running = False
                gotomain = True
              elif (((position[0] - shutCenter[0]) ** 2 + (position[1] - shutCenter[1]) ** 2) ** 0.5 <= shutRadius):
                confirmQuit()
              else:
                for i in range(numFile):
                  box = (lstRectBackgrounds[i][0].left, lstRectBackgrounds[i][0].right, lstRectBackgrounds[i][0].top, lstRectBackgrounds[i][0].bottom)
                  for j in range(len(lstTag)):
                    lstTag[j] = False
                    selected = -1
                  if 0 < lstRectBackgrounds[i][0].bottom < (CUTLINE)/screenScale:
                    if(box[0]<=position[0]<=box[1] and box[2]<=position[1]<=box[3]): #Clicked a box
                      lstTag[i] = True
                      selected = i
                      break
            elif event.button == 4 and lstRectBackgrounds[-1][0].bottom >= (CUTLINE - 100)/screenScale: #scroll up
              for i in range(numFile):
                lstRectBackgrounds[i][0].top = lstRectBackgrounds[i][0].top-round(SCRLLFACTOR / screenScale)
                lstRectBackgrounds[i][1].top = lstRectBackgrounds[i][1].top-round(SCRLLFACTOR / screenScale)
                for j in range(3):
                  lstRectBlinds[i][j].top = lstRectBlinds[i][j].top-round(SCRLLFACTOR / screenScale)
            elif event.button == 5 and lstRectBackgrounds[0][0].top <= 99/screenScale:
              for i in range(numFile):
                lstRectBackgrounds[i][0].top = lstRectBackgrounds[i][0].top+round(SCRLLFACTOR / screenScale)
                lstRectBackgrounds[i][1].top = lstRectBackgrounds[i][1].top+round(SCRLLFACTOR / screenScale)
                for j in range(3):
                  lstRectBlinds[i][j].top = lstRectBlinds[i][j].top+round(SCRLLFACTOR / screenScale)
        screen.blit(imgBackground, (0,0))
        if flagEmpty:
          screen.blit(textEmpty.getText(), textEmpty.getRect())
        else:
          for i in range(numFile):
            if 0< lstRectBackgrounds[i][0].bottom < (CUTLINE)/screenScale:
              if lstTag[i]:
                pygame.draw.rect(screen, SELECTED, lstRectBackgrounds[i][0])
              else:
                pygame.draw.rect(screen, PALEGRAY, lstRectBackgrounds[i][0])
              pygame.draw.rect(screen, GRAY, lstRectBackgrounds[i][1], width=4)
              for j in range(3):
                screen.blit(lstTextBlinds[i][j], lstRectBlinds[i][j])
        pygame.draw.rect(screen, PALEGRAY, rectNext)
        pygame.draw.rect(screen, GRAY, rectNext, width = 4)
        screen.blit(textNext.getText(), textNext.getRect())
        pygame.draw.rect(screen, PALEGRAY, rectBack)
        pygame.draw.rect(screen, GRAY, rectBack, width = 4)
        screen.blit(textBack.getText(), textBack.getRect())
        pygame.draw.line(screen,WHITE, (0,round(CUTLINE/screenScale)), (round(2048/screenScale),round(CUTLINE/screenScale)))
        pygame.draw.circle(screen, RED, shutCenter, shutRadius)
        pygame.draw.circle(screen, BLACK, shutCenter, shutRadius, width = 2)
        pygame.display.flip()

        #####################
      else: #Next 눌렀을 때, Structure 수정 단계
        if selected == -1:
          flagNext = False
        elif flagFirst:
          flagFirst = False
          objControl = lstBlindObjs[selected]

        ##### KeyBoard events
        for event in pygame.event.get():
          if event.type == KEYDOWN:
            if event.key == ord('q'):
              confirmQuit()
              if TK_VAL:
                running = False
                gotomain = False
            elif event.key in K_NUM or event.key == K_BACKSPACE:
              if selectedIdx != -1:
                temp_input = (temp_input*10 + processAscii(event.key)) if (event.key in K_NUM) else (temp_input//10)
                lstBoxBlinds[selectedIdx][1][lstBoxBlinds[selectedIdx][2]].changeContent(font = fontBox, content = str(temp_input))
            elif event.key == K_RETURN:
              if selectedIdx != -1:
                objControl.changeLstBlinds(selectedIdx, lstBoxBlinds[selectedIdx][2] - 1, temp_input)
                lstBoxBlinds[selectedIdx][2] = 0
                selectedIdx = -1
                temp_input = 0

          ###### MOUSE BUTTON DOWN Events    
          elif event.type == MOUSEBUTTONDOWN:
            if event.button == 4 or event.button == 5:
              if event.button == 4 and lstBoxBlinds[0][1][0].top >= 130/screenScale:
                pass
              elif event.button == 5 and lstBoxBlinds[-1][1][0].bottom <= (CUTLINE - 100) / screenScale:
                pass
              else:
                f = -1 if (event.button == 5) else 1
                
                for boxblinds in lstBoxBlinds:
                  #tempLst2 = [isbreak,[tempBox, lvl, dur, bb, sb, ante]]
                  boxblinds[1][0].top = boxblinds[1][0].top + f*round(SCRLLFACTOR / screenScale) #박스
                  boxblinds[3].top = boxblinds[3].top + f*round(SCRLLFACTOR / screenScale)
                  for j in range(5):
                    boxblinds[1][j+1].changePosition(relative = "top", position = (boxblinds[1][j+1].getRect().centerx, boxblinds[1][j+1].getRect().top + f*round(SCRLLFACTOR / screenScale))) 
                plusBox.top = plusBox.top + f*round(SCRLLFACTOR / screenScale)
                textPlus.changePosition(relative = "top", position=(textPlus.getRect().centerx, textPlus.getRect().top + f*round(SCRLLFACTOR / screenScale)))
            if event.button == 1: ## 클릭
              if selectedIdx != -1:
                objControl.changeLstBlinds(selectedIdx, lstBoxBlinds[selectedIdx][2] - 1, temp_input)
                lstBoxBlinds[selectedIdx][2] = 0
                selectedIdx = -1
                temp_input = 0
              position = pygame.mouse.get_pos()
              if mouseInRect(rectNext, position): # Next 버튼 눌렀을 때 flagTimer true로

                updateFile(objControl)
                flagTimer = True
                running = False
                templst = lstBlindObjs[selected].getLstBlinds()
                lstLevel = [0]
                lstBlind = [0]
                title = lstBlindObjs[selected].getTitle()
                for item in templst:
                  lstLevel.append(item[1])
                  if item[1] == 0:
                    lstBlind.append(0)
                  else:
                    lstBlind.append(item[2:5])
              elif mouseInRect(rectBack, position): # Back 버튼
                flagNext=False
                gotomain = True
                
                continue
              elif (((position[0] - shutCenter[0]) ** 2 + (position[1] - shutCenter[1]) ** 2) ** 0.5 <= shutRadius):
                confirmQuit()
              else: # 글자 클릭했는지 확인
                
                cntBreak, cntLvl = 0, 0
                #tempLst2 = [isbreak,[tempBox, lvl, dur, bb, sb, ante]]
                flagUp = False
                cntIdx = 0
                idxDelete = 0
                for boxblinds in lstBoxBlinds:
                  if flagUp:  #### delete 이벤트 발생으로 한 칸씩 위로 올려야할 때
                    boxblinds[1][0].top = boxblinds[1][0].top - round(BLINDINTERVAL/screenScale) #박스
                    boxblinds[3].top = boxblinds[3].top - round(BLINDINTERVAL/screenScale)
                    for j in range(5):
                      boxblinds[1][j+1].changePosition(relative = "top", position = (boxblinds[1][j+1].getRect().centerx, boxblinds[1][j+1].getRect().top - round(BLINDINTERVAL/screenScale))) 
                  if boxblinds[0] == 0:
                    cntBreak+=1
                  else:
                    cntLvl+=1
                    boxblinds[1][1].changeContent(font = fontBox, content = str(cntLvl))
                  if 120/screenScale<boxblinds[1][0].bottom<(CUTLINE)/screenScale: # 화면 안에 나오는 애들 중
                    if mouseInRect(boxblinds[3], position) and not flagUp:
                      objControl.deleteLevel(cntIdx)
                      idxDelete = cntIdx
                      flagUp = True
                      if boxblinds[0] == 1:
                        cntLvl -= 1
                      continue
                    elif boxblinds[0] == 0: #break인 경우
                      if mouseInRect(boxblinds[1][1].getRect(), position):
                        cntLvl+=1
                        boxblinds[1][1].changeContent(font = fontBox, content = str(cntLvl))
                        boxblinds[0] = 1
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
                if flagUp:
                  plusBox.top = plusBox.top - round(BLINDINTERVAL/screenScale)
                  textPlus.changePosition(relative = "top", position=(textPlus.getRect().centerx, textPlus.getRect().top - round(BLINDINTERVAL/screenScale)))
                  flagUp = False
                  lstBoxBlinds.pop(idxDelete)
                  
                if 120/screenScale<plusBox.bottom<(CUTLINE)/screenScale:
                  if mouseInRect(plusBox, position):
                    tempBox = pygame.Rect(0,0,round(900/screenScale),round(50/screenScale))
                    tempBox.center = plusBox.center
                    rectDelete = pygame.Rect(0,0,round(25/screenScale), round(25/screenScale))
                    rectDelete.center = (midpoint[0] + round(480/screenScale), round((150+cnt*BLINDINTERVAL)/screenScale))
                    lvl = TextObj(font = fontBox, content=str(cntLvl+1), color=BLACK, relative="center", position=(midpoint[0] - round(400/screenScale), tempBox.centery))
                    dur = TextObj(font = fontBox, content='10', color=BLACK, relative="center", position=(midpoint[0] + round(300/screenScale), tempBox.centery))
                    bb = TextObj(font = fontBox, content='0', color=BLACK, relative="center", position=(midpoint[0] - round(225/screenScale), tempBox.centery))

                    sb = TextObj(font = fontBox, content='0', color=BLACK, relative="center", position=(midpoint[0] - round(50/screenScale), tempBox.centery))
                    ante = TextObj(font = fontBox, content='0', color=BLACK, relative="center", position=(midpoint[0] + round(125/screenScale), tempBox.centery))
                    lstBoxBlinds.append([1,[tempBox, lvl, dur, bb, sb, ante], 0, rectDelete])
                    plusBox.top = plusBox.top + round(BLINDINTERVAL/screenScale)
                    textPlus.changePosition(relative="top", position=(textPlus.getRect().centerx,textPlus.getRect().top + round(BLINDINTERVAL/screenScale)))
                    objControl.addLevel()
        #### End of event for loop
                          
        screen.blit(imgBackground, (0,0))
        
        for boxblinds in lstBoxBlinds:
          tempbox = boxblinds[1][0]
          if 120/screenScale<tempbox.bottom<(CUTLINE)/screenScale:  
            if boxblinds[0] == 0: #Break
              pygame.draw.rect(screen,WHITE, tempbox)
              pygame.draw.rect(screen,BLACK, tempbox, width=4)
              blitText(screen, boxblinds[1][1], boxblinds[1][2])
            else:
              pygame.draw.rect(screen,GRAY, tempbox)
              pygame.draw.rect(screen,BLACK, tempbox, width=4)
              blitText(screen, boxblinds[1][1], boxblinds[1][2],boxblinds[1][3],boxblinds[1][4],boxblinds[1][5])
              if boxblinds[2] != 0: # 무언가 클릭됐을 때
                pygame.draw.rect(screen, WHITE, boxblinds[1][boxblinds[2]].getRect())
                blitText(screen, boxblinds[1][boxblinds[2]])
            pygame.draw.rect(screen, RED, boxblinds[3])  ### Delete button
            pygame.draw.rect(screen, BLACK, boxblinds[3], width = 3)
        #### End of for loop printing boxes on screen
        if 120/screenScale<plusBox.bottom<(CUTLINE)/screenScale:
          pygame.draw.rect(screen, GRAY, plusBox)
          pygame.draw.rect(screen, BLACK, plusBox, width=4)
          screen.blit(textPlus.getText(), textPlus.getRect())        
        pygame.draw.rect(screen, DARKGRAY, rectSettings)
        pygame.draw.line(screen, BLACK, (0,round(120/screenScale)), (round(2200/screenScale),round(120/screenScale)), width=5)
        pygame.draw.line(screen,WHITE, (0,round(CUTLINE/screenScale)), (round(2048/screenScale),round(CUTLINE/screenScale)))
        pygame.draw.rect(screen, PALEGRAY, rectNext)
        pygame.draw.rect(screen, GRAY, rectNext, width = 4)
        screen.blit(textSavenGo.getText(), textSavenGo.getRect())
        pygame.draw.rect(screen, PALEGRAY, rectBack)
        pygame.draw.rect(screen, GRAY, rectBack, width = 4)
        screen.blit(textBack.getText(), textBack.getRect())
        pygame.draw.line(screen,WHITE, (0,round(CUTLINE/screenScale)), (round(2048/screenScale),round(CUTLINE/screenScale)))
        blitText(screen, textSettingLevel, textSettingBB, textSettingAnte, textSettingDur, textSettingSB)
        pygame.draw.circle(screen, RED, shutCenter, shutRadius)
        pygame.draw.circle(screen, BLACK, shutCenter, shutRadius, width = 2)
        pygame.display.flip()
    #### End of main While



    pygame.quit()
    if gotomain:
      return True
    elif flagTimer:
      flag = timer.main(lstBlind, lstLevel, title, True, vol)
      if flag == 0:
        r = False
      else: r = True
    else: 
      return False
  
##################### End of main_load