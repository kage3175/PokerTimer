import time
import pygame
import ctypes
from pygame.locals import *
import os
import timer
from TextObj import TextObj

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
  def putFilename(self, name):
    self.filename = name
  def getFilename(self):
    return self.filename
  
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
            if(rectNext.left<=position[0]<=rectNext.right and rectNext.top <= position[1] <= rectNext.bottom): #Next Button
              flagNext = True
              objControl = lstBlindObjs[selected]
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
                tempLst2 = [isbreak,[tempBox, lvl, dur, bb, sb, ante]]
                '''if tempLst[i][0] == 0: #Break
                  box = TextObj(font = fontBox, content = "Break", color=BLACK, relative="center", position=(midpoint[0]-round(400/screenScale), round((150+cnt*BLINDINTERVAL)/screenScale)))
                  lvl = TextObj(font = fontBox, content = str(level), color=BLACK, relative= "center", position=(midpoint[0]-round(400/screenScale), round((150+cnt*BLINDINTERVAL)/screenScale)))
                  dur = TextObj(font = fontBox, color=BLACK, content=str(tempLst[i][1]), relative="center", position=(midpoint[0] + round(300/screenScale), round((150+cnt*BLINDINTERVAL)/screenScale)))
                  bb = TextObj(font = fontBox, color=BLACK, content=str(tempLst[i][2]), relative="center", position=(midpoint[0] - round(225/screenScale), round((150+cnt*BLINDINTERVAL)/screenScale)))
                  sb = TextObj(font = fontBox, color=BLACK, content=str(tempLst[i][3]), relative="center", position=(midpoint[0] - round(50/screenScale), round((150+cnt*BLINDINTERVAL)/screenScale)))
                  ante = TextObj(font = fontBox, color=BLACK, content=str(tempLst[i][4]), relative="center", position=(midpoint[0] + round(125/screenScale), round((150+cnt*BLINDINTERVAL)/screenScale)))
                  temptext1 = fontBox.render("Break", True, BLACK)
                  objtemp1 = temptext1.get_rect()
                  objtemp1.center = (midpoint[0]-round(400/screenScale), round((150+cnt*BLINDINTERVAL)/screenScale))
                  temptext2 = fontBox.render(str(tempLst[i][1]), True, BLACK) # Duration
                  objtemp2 = temptext2.get_rect()
                  objtemp2.center = (midpoint[0] + round(300/screenScale), round((150+cnt*BLINDINTERVAL)/screenScale))
                  tempLst2 = [0,[tempBox,[temptext1,objtemp1], [temptext2,objtemp2]]]
                  #[0, [박스, Lvl, Duration, BB, SB, Ante]]
                else: #Blind
                  temptext1 = fontBox.render(str(level), True, BLACK) # Level
                  objtemp1 = temptext1.get_rect()
                  objtemp1.center = (midpoint[0]-round(400/screenScale), round((150+cnt*BLINDINTERVAL)/screenScale))
                  temptext2 = fontBox.render(str(tempLst[i][1]), True, BLACK) # Duration
                  objtemp2 = temptext2.get_rect()
                  objtemp2.center = (midpoint[0] + round(300/screenScale), round((150+cnt*BLINDINTERVAL)/screenScale))
                  temptext3 = fontBox.render(str(tempLst[i][2]), True, BLACK) # BB
                  objtemp3 = temptext3.get_rect()
                  objtemp3.center = (midpoint[0] - round(225/screenScale), round((150+cnt*BLINDINTERVAL)/screenScale))
                  temptext4 = fontBox.render(str(tempLst[i][3]), True, BLACK) # SB
                  objtemp4 = temptext4.get_rect()
                  objtemp4.center = (midpoint[0] - round(50/screenScale), round((150+cnt*BLINDINTERVAL)/screenScale))
                  temptext5 = fontBox.render(str(tempLst[i][4]), True, BLACK) # Ante
                  objtemp5 = temptext5.get_rect()
                  objtemp5.center = (midpoint[0] + round(125/screenScale), round((150+cnt*BLINDINTERVAL)/screenScale))
                  tempLst2 = [1,[tempBox,[temptext1,objtemp1], [temptext2,objtemp2], [temptext3,objtemp3], [temptext4, objtemp4], [temptext5, objtemp5]]]'''
                  
                lstBoxBlinds.insert(0,tempLst2)
                cnt+=1
              
              outfile = open('./doc/'+objControl.getFilename(), "w")
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
              outfile.close()
            elif(rectBack.left<=position[0]<=rectBack.right and rectBack.top <= position[1] <= rectBack.bottom): #Back Button
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

      
      for event in pygame.event.get():
        if event.type == KEYDOWN:
          if event.key == ord('q'):
            running = False
            gotomain = False
        elif event.type == MOUSEBUTTONDOWN:
          if event.button == 4 or event.button == 5:
            f = -1 if (event.button == 4) else 1
            
            for i in range(lstBlindObjs[selected].getNumBlinds()):
              #tempLst2 = [isbreak,[tempBox, lvl, dur, bb, sb, ante]]
              lstBoxBlinds[i][1][0].top = lstBoxBlinds[i][1][0].top + f*round(SCRLLFACTOR / screenScale) #박스
              for j in range(5):
                lstBoxBlinds[i][1][j+1].changePosition(relative = "top", position = lstBoxBlinds[i][1][j+1].getRect().top + f*round(SCRLLFACTOR / screenScale)) 
          if event.button == 1: ## 클릭
            position = pygame.mouse.get_pos()
            if(rectNext.left<=position[0]<=rectNext.right and rectNext.top<=position[1]<=rectNext.bottom):
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
            else:
              cntBreak, cntLvl = 0, 0
              for boxblinds in lstBoxBlinds:
                cntLvl += 1
                if lstBoxBlinds[i][0] == 0:
                  cntBreak+=1
                if 120/screenScale<tempbox.bottom<(CUTLINE)/screenScale:
                  if lstBoxBlinds[i][0] == 0:
                    if lstBoxBlinds[i][1][1].getRect().left <= position[0] <= lstBoxBlinds[i][1][1].getRect().right and lstBoxBlinds[i][1][1].getRect().top <= position[1]<= lstBoxBlinds[i][1][1].getRect().bottom:
                      lstBoxBlinds[i][1][1].changeContent(font = fontBox, content = str(cntLvl))
                      ### 작업 해야 함
              pass
      #### End of event for loop
                         
      screen.blit(imgBackground, (0,0))
      
      for i in range(lstBlindObjs[selected].getNumBlinds()):
        tempbox = lstBoxBlinds[i][1][0]
        if 120/screenScale<tempbox.bottom<(CUTLINE)/screenScale:
          
          if lstBoxBlinds[i][0] == 0: #Break
            pygame.draw.rect(screen,WHITE, tempbox)
            pygame.draw.rect(screen,BLACK, tempbox, width=4)
            blitText(screen, lstBoxBlinds[i][1][1], lstBoxBlinds[i][1][2])
          else:
            pygame.draw.rect(screen,GRAY, tempbox)
            pygame.draw.rect(screen,BLACK, tempbox, width=4)
            blitText(screen, lstBoxBlinds[i][1][1], lstBoxBlinds[i][1][2],lstBoxBlinds[i][1][3],lstBoxBlinds[i][1][4],lstBoxBlinds[i][1][5])
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
  else: return False
##################### End of main_load