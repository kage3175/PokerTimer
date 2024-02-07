from pygame.locals import *

K_NUM = [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_KP0, K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9]
BANNED = ["\\", "/", ":", "*", "?", "<", ">", "\"", "|", "left ctrl", "right ctrl", "tab", "`", "+", "up", "down", "right", "left", "enter"]
SHIFT = ["left shift", "right shift"]
STRNUM = ["1", "2", "3","4","5","6","7","8","9","0"]

class TextObj:
  def __init__(self, font, content = "",position = (0,0), relative = "topleft", color = (0,0,0)) -> None:
    self.content = content
    self.text = font.render(content, True, color)
    self.rect = self.text.get_rect()
    self.position = position
    self.relative = relative
    self.color = color
    self.clicked = False
    self.font = font
    if relative == "topleft":
      self.rect.topleft = position
    elif relative == "center":
      self.rect.center = position
    elif relative == "rcenter":
      self.rect.centery = position[0]
      self.rect.right = position[1]
    elif relative == "lcenter":
      self.rect.centery = position[0]
      self.rect.left = position[1]
    elif relative == "topright":
      self.rect.topright = position
  def changePosition(self, relative = "topleft", position = (0,0)):
    self.relative = relative
    if relative == "topleft":
      self.rect.topleft = position
    elif relative == "bottom":
      self.rect.bottom = position
    elif relative == "center":
      self.rect.center = position
    elif relative == "right":
      self.rect.right = position
    elif relative == "left":
      self.rect.left = position
    elif relative == "top":
      self.rect.top = position[1]
      self.rect.centerx=position[0]
    self.position = position
  def getRect(self):
    return self.rect
  def changeColor(self, color):
    self.color = color
    self.text = self.font.render(self.content, True, self.color)
    self.rect = self.text.get_rect()
    if self.relative == "topleft":
      self.rect.topleft = self.position
    elif self.relative == "center":
      self.rect.center = self.position
    elif self.relative == "rcenter":
      self.rect.centery = self.position[0]
      self.rect.right = self.position[1]
    elif self.relative == "lcenter":
      self.rect.centery = self.position[0]
      self.rect.left = self.position[1]
    elif self.relative == "topright":
      self.rect.topright = self.position
    elif self.relative == "top":
      self.rect.centerx = self.position[0]
      self.rect.top = self.position[1]
  def changeContent(self, font, content = ""):
    self.content = content
    self.text = font.render(content, True, self.color)
    self.rect = self.text.get_rect()
    self.font = font
    if self.relative == "topleft":
      self.rect.topleft = self.position
    elif self.relative == "center":
      self.rect.center = self.position
    elif self.relative == "rcenter":
      self.rect.centery = self.position[0]
      self.rect.right = self.position[1]
    elif self.relative == "lcenter":
      self.rect.centery = self.position[0]
      self.rect.left = self.position[1]
    elif self.relative == "topright":
      self.rect.topright = self.position
    elif self.relative == "top":
      self.rect.centerx = self.position[0]
      self.rect.top = self.position[1]
  def getContent(self):
    return self.content
  def getText(self):
    return self.text
  def click(self):
    self.clicked=not self.clicked
  def getPos(self):
    return self.position
  
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
  def appendLevel(self, lstInfo):
    self.lstBlinds.append(lstInfo)
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
  def setTitle(self, title):
    self.title = title
  def setType(self, type):
    self.type = type
#### End of BlindFile Class

def blitText(surface, *textobjs):
  for text in textobjs:
    surface.blit(text.getText(), text.getRect())
#### End of blitText function

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
#### End of updateFile function
  
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