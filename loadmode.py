import time
import pygame
import ctypes
from pygame.locals import *
import os
import timer
from TextObj import TextObj
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


class BlindFile:
  def __init__(self) -> None:
    self.title = ''
    self.type = 0
    self.numBlinds = 0
    self.lstDurations = []
    self.lstBlinds = []
    self.filename = ""
  def make(self, file):
    self.title = file.readline().strip()
    self.type = int(file.readline().strip())
    self.numBlinds = int(file.readline().strip())
    self.lstDurations = list(map(int, file.readline()[:-2].strip().split(",")))

    temp_blinds = file.readline().strip().replace("(", "").replace(")","")
    strlst_blinds = list(temp_blinds.split("$"))
    for str_ in strlst_blinds:
      temp_lst = list(map(int, str_.split(",")))
      self.lstBlinds.append(temp_lst)
  def getTitle(self):
    return self.title
  def getType(self):
    return self.type
  def getNumBlinds(self):
    return self.numBlinds
  def changeNumBlinds(self, num):
    self.numBlinds += num
  def getLstBlinds(self):
    return self.lstBlinds
  def getLstDurations(self):
    return self.lstDurations
  def updateLstDurations(self):
    self.lstDurations=[]
    for item in self.lstBlinds:
      if item[0] == 1 and item[1] not in self.lstDurations and item[1] != 0:
        self.lstDurations.append(item[1])
    self.lstDurations.sort(reverse=True)
  def putFilename(self, name):
    self.filename = name
  def getFilename(self):
    return self.filename
  def changeLstBlinds(self, idx1, idx2, content):
    self.lstBlinds[idx1][idx2] = content
  def addLevel(self):
    #### lstInfo = [Dur, BB, SB, Ante]
    self.lstBlinds.append([1,10,0,0,0])
    self.numBlinds += 1
  def deleteLevel(self, idx):
    try:
      self.lstBlinds.pop(idx)
    except:
      print("NotAvailableIdxError")
  def changeBlinds(self, idx, isBreak):
    if isBreak:
      self.lstBlinds[idx][0] = 0
      for i in range(3):
        self.lstBlinds[idx][i+2] = 0
    else:
      self.lstBlinds[idx][0] = 1

  
class BlindBox:
  def __init__(self) -> None:
    self.isBreak = False
    self.duration = 0
    self.SB = 0
    self.BB = 0
    self.Ante = 0
    self.level = 0
  
def blitText(surface, *textobjs):
  for text in textobjs:
    surface.blit(text.getText(), text.getRect())
  pass
#### End of blitText function

def mouseInRect(rectObj, position):
  return rectObj.left <= position[0] <= rectObj.right and rectObj.top <= position[1]<= rectObj.bottom

def processAscii(key):
  if key in [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]:
    return int(key) - 48
  elif key == K_KP0:
    return 0
  elif key == K_KP1:
    return 1
  elif key == K_KP2:
    return 2
  elif key == K_KP3:
    return 3
  elif key == K_KP4:
    return 4
  elif key == K_KP5:
    return 5
  elif key == K_KP6:
    return 6
  elif key == K_KP7:
    return 7
  elif key == K_KP8:
    return 8
  elif key == K_KP9:
    return 9
  else:
    return 0
#### End of processAscii
  
def updateFile(objControl):
  outfile = open('./doc/'+objControl.getFilename(), "w")
  print(objControl.getTitle(), file=outfile)
  print(objControl.getType(), file= outfile)
  objControl.updateLstDurations()
  templst = objControl.getLstDurations()
  print(str(objControl.getNumBlinds()), file=outfile)
  for i in range(len(templst)):
    print(str(templst[i]) + ",", end = "", file=outfile)
  print("", file=outfile)
  templst = objControl.getLstBlinds()
  for i in range(objControl.getNumBlinds()-1):
    print("("+str(templst[i][0])+","+str(templst[i][1])+","+str(templst[i][2])+","+str(templst[i][3])+ ","+str(templst[i][4])+")",end="$", file=outfile)
  i = objControl.getNumBlinds()-1
  print("("+str(templst[i][0])+","+str(templst[i][1])+","+str(templst[i][2])+","+str(templst[i][3])+ ","+str(templst[i][4])+")",end="", file=outfile)
  outfile.close()

def main_load():
  pygame.init()
  user32 = ctypes.windll.user32
  screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
  midpoint = screensize[0] / 2, screensize[1] / 2 # 화면 중앙점
  screenScale = 1152/screensize[1]
  screen = pygame.display.set_mode()
  imgBackground = pygame.image.load("./img/background.jpg")
  imgBackground = pygame.transform.scale(imgBackground, screensize)

  flagEmpty = False
  lstBlindObjs = []
  lstTextBlinds = []
  lstRectBlinds = []
  lstRectBackgrounds = []
  lstBoxBlinds=[] # (rect, text_blindbreak, text_level, text_SB, text_BB, text_Ante, up, down, delete)
  lstLevel, lstBlind = [],[]
  selected = -1
  
  dictType = {1:"BB Ante", 2:"All Ante"}
  fontTitle = pygame.font.Font('./font/NanumGothic.ttf', round(60/screenScale))
  fontEmpty = pygame.font.Font('./font/NanumGothic.ttf', round(120/screenScale))
  fontSup = pygame.font.Font('./font/NanumGothic.ttf', round(30/screenScale))
  fontButton = pygame.font.Font('./font/NanumGothicBold.ttf', round(80/screenScale))
  fontBox = pygame.font.Font('./font/NanumGothic.ttf', round(20/screenScale))

  try:
    lst_blindfiles = os.listdir('./doc')
    numFile = len(lst_blindfiles)
  except:
    print("Something wrong with opening doc folder")
  
  if numFile==0:
    flagEmpty = True
  else:
    lstTag = [False for _ in range(numFile)]
    cnt = 0
    for name in lst_blindfiles:
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
  rectDelete = pygame.Rect(0,0,round(20/screenScale), round(20/screenScale))

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
    if not flagNext:
      for event in pygame.event.get():
        if event.type == KEYDOWN:
          if event.key == ord('q'):
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
                tempLst2 = [isbreak,[tempBox, lvl, dur, bb, sb, ante],0]
                  
                lstBoxBlinds.append(tempLst2)
                cnt+=1
              
              '''outfile = open('./doc/'+objControl.getFilename(), "w")
              print(objControl.getTitle(), file=outfile)
              print(objControl.getType(), file= outfile)
              templst = objControl.getLstDurations()
              print(str(objControl.getNumBlinds()), file=outfile)
              for i in range(len(templst)):
                print(str(templst[i]) + ",", end = "", file=outfile)
              print("", file=outfile)
              templst = objControl.getLstBlinds()
              for i in range(objControl.getNumBlinds()-1):
                print("("+str(templst[i][0])+","+str(templst[i][1])+","+str(templst[i][2])+","+str(templst[i][3])+ ","+str(templst[i][4])+")",end="$", file=outfile)
              i = objControl.getNumBlinds()-1
              print("("+str(templst[i][0])+","+str(templst[i][1])+","+str(templst[i][2])+","+str(templst[i][3])+ ","+str(templst[i][4])+")",end="", file=outfile)
              outfile.close()'''
              updateFile(objControl)
              plusBox = pygame.Rect(0,0,round(900/screenScale),round(50/screenScale))
              plusBox.center = (midpoint[0], round((150+cnt*BLINDINTERVAL)/screenScale))
              textPlus = TextObj(font = fontBox, content="+", position=plusBox.center, relative="center", color=BLACK)
            elif mouseInRect(rectBack, position): #Back Button
              running = False
              gotomain = True
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
          elif event.button == 4: #scroll up
            #print("Scrllup")
            for i in range(numFile):
              lstRectBackgrounds[i][0].top = lstRectBackgrounds[i][0].top-round(SCRLLFACTOR / screenScale)
              lstRectBackgrounds[i][1].top = lstRectBackgrounds[i][1].top-round(SCRLLFACTOR / screenScale)
              for j in range(3):
                lstRectBlinds[i][j].top = lstRectBlinds[i][j].top-round(SCRLLFACTOR / screenScale)
          elif event.button == 5:
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
      pygame.display.flip()
      time.sleep(0.05)

      #####################
    else: #Next 눌렀을 때
      if selected == -1:
        flagNext = False
      elif flagFirst:
        flagFirst = False
        objControl = lstBlindObjs[selected]

      ##### KeyBoard events
      for event in pygame.event.get():
        if event.type == KEYDOWN:
          #print(event.key)
          if event.key == ord('q'):
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
            f = -1 if (event.button == 5) else 1
            
            for boxblinds in lstBoxBlinds:
              #tempLst2 = [isbreak,[tempBox, lvl, dur, bb, sb, ante]]
              boxblinds[1][0].top = boxblinds[1][0].top + f*round(SCRLLFACTOR / screenScale) #박스
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

              #print(objControl.getLstBlinds())
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
            else: # 글자 클릭했는지 확인
              
              cntBreak, cntLvl = 0, 0
              #tempLst2 = [isbreak,[tempBox, lvl, dur, bb, sb, ante]]
              cntIdx = 0
              for boxblinds in lstBoxBlinds:
                if boxblinds[0] == 0:
                  cntBreak+=1
                else:
                  cntLvl+=1
                  boxblinds[1][1].changeContent(font = fontBox, content = str(cntLvl))
                if 120/screenScale<boxblinds[1][0].bottom<(CUTLINE)/screenScale: # 화면 안에 나오는 애들 중
                  if boxblinds[0] == 0: #break인 경우
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
                  objControl.addLevel()
                  print("+")
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
      screen.blit(textSettingLevel.getText(), textSettingLevel.getRect())
      screen.blit(textSettingBB.getText(), textSettingBB.getRect())
      screen.blit(textSettingAnte.getText(), textSettingAnte.getRect())
      screen.blit(textSettingSB.getText(), textSettingSB.getRect())
      screen.blit(textSettingDur.getText(), textSettingDur.getRect())
      pygame.display.flip()
      time.sleep(0.05)
  #### End of main While



  pygame.quit()
  if gotomain:
    return True
  elif flagTimer:
    timer.main(lstBlind, lstLevel, title)
  else: 
    return False
  
##################### End of main_load