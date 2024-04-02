from pygame.locals import *
from enum import Enum

K_NUM = [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_KP0, K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9]
BANNED = ["\\", "/", ":", "*", "?", "<", ">", "\"", "|", "`", "+", "\'"]
SHIFT = ["left shift", "right shift"]
STRNUM = ["1", "2", "3","4","5","6","7","8","9","0"]
SHIFTED = {'`':'~','1':'!','2':'@','3':'#','4':'$','5':'%','6':'^','7':'&','8':'*','9':'(','0':')',';':':','\'':'\"',',':'<','.':'>','/':'?','\\':'|','+':'+', '[' : '{', ']':'}', '-':'_'}
TH = {1:"st: ", 2:"nd: ", 3:"rd: "}
FPS = 60

WHITE = (240,240,240)
BLACK = (0,0,0)
PALEGRAY = (210,210,210)
GRAY = (200,200,200)
SELECTED = (200,50,50)
DARKGRAY = (75,75,75)
BLINDGRAY = (175,175,175)
BREAKGRAY = (215,215,215)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BRIGHTRED = (255,10,10)
YELLOW = (220,220,90)



CUTLINE = 900
BOXHEIGHT = 210
SCRLLFACTOR = 25
BOXINTERVAL = 240
BLINDINTERVAL = 60

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
      self.rect.centery = position[1]
      self.rect.right = position[0]
    elif relative == "lcenter":
      self.rect.centery = position[1]
      self.rect.left = position[0]
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
  def getFont(self):
    return self.font
  
class Relative(Enum):
  CENTER = 2
  TOPLEFT = 1
  RCENTER = 3
  LCENTER = 4
  TOPRIGHT = 5
  BOTTOMLEFT = 6
  BOTTOMRIGHT = 7

class ImgObj:
  def __init__(self, fileAdrress, position, relative = "topleft", scalable = False, size = (50,50)) -> None:
    self.fileAddress = fileAdrress
    self.rect = None
    self.position = position
    self.size = size
    self.img = None
    self.relative = relative
    try:
      self.img = pygame.image.load(self.fileAddress)
      if scalable:
        try:
          self.img = pygame.transform.smoothscale(self.img, size)
        except:
          self.img = pygame.transform.scale(self.img, size)
      self.rect = self.img.get_rect()
      if self.relative == Relative.TOPLEFT:
        self.rect.topleft = position
      elif self.relative == Relative.CENTER:
        self.rect.center = position
    except:
      print("Failed to Open the img File at " + self.fileAddress)
  def getImg(self):
    return self.img
  def getRect(self):
    return self.rect
  
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
    except Exception as e:
      print("Error while deleting level in TextObj: ", e)
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
  def make_deNovo(self, filename, title, type, numBlinds, lstBlinds):
    self.numBlinds = numBlinds
    self.lstBlinds = lstBlinds
    self.filename = filename
    self.type = type
    self.title = title
    self.updateLstDurations()
#### End of BlindFile Class

def blitText(surface, *textobjs):
  for text in textobjs:
    surface.blit(text.getText(), text.getRect())
#### End of blitText function

def updateFile(objControl):
  try:
    outfile = open('./doc/'+objControl.getFilename(), "w")
  except Exception as e:
    print("Error while opening file at ./doc directory:", e)
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
  
def mouseInRect(rectObj, position):
  return rectObj.left <= position[0] <= rectObj.right and rectObj.top <= position[1]<= rectObj.bottom
#### End of processAscii