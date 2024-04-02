import pygame
from pygame.locals import *
import time
import ctypes
from ClassObjs import TextObj
import tkinter as tk
from ClassObjs import *
from enum import Enum

FONTPATH = {'NGothicR' : './font/NanumGothic.ttf', 'NSquareR' : './font/NanumSquareR.ttf'}
LSTLEVELS = []
LSTBLINDS = []

PALEGRAY = (180,180,180)
BACKGROUND = [60, 55, 230]

TK_VAL = False

PRIZEINTERVAL = 33

TK_LST = []

def blitBackground(screen, rect, screenScale):
  global BACKGROUND
  screen.fill(BACKGROUND)
  #pygame.draw.rect(screen, WHITE, rect, width=8)
  pygame.draw.line(screen, WHITE, (round(26/screenScale), round(176/screenScale)), (round(2018/screenScale), round(176/screenScale)), width=4)
  pygame.draw.line(screen, WHITE, (round(26/screenScale), round(276/screenScale)), (round(2018/screenScale), round(276/screenScale)), width=2)
  pygame.draw.line(screen, WHITE, (round(640/screenScale), round(375/screenScale)), (round(1408/screenScale), round(375/screenScale)), width=2)
  pygame.draw.line(screen, WHITE, (round(26/screenScale), round(590/screenScale)), (round(2018/screenScale), round(590/screenScale)), width=2)
  pygame.draw.line(screen, WHITE, (round(26/screenScale), round(905/screenScale)), (round(1024/screenScale), round(905/screenScale)), width=2)
  pygame.draw.line(screen, WHITE, (round(26/screenScale), round(955/screenScale)), (round(1024/screenScale), round(955/screenScale)), width=2)
  pygame.draw.line(screen, WHITE, (round(26/screenScale), round(1040/screenScale)), (round(2018/screenScale), round(1040/screenScale)), width=2)


  pygame.draw.line(screen, WHITE, (round(505/screenScale), round(905/screenScale)), (round(505/screenScale), round(1040/screenScale)), width=2)
  pygame.draw.line(screen, WHITE, (round(1408/screenScale), round(276/screenScale)), (round(1408/screenScale), round(590/screenScale)), width=2)
  pygame.draw.line(screen, WHITE, (round(640/screenScale), round(276/screenScale)), (round(640/screenScale), round(590/screenScale)), width=2)
  pygame.draw.line(screen, WHITE, (round(1024/screenScale), round(590/screenScale)), (round(1024/screenScale), round(1040/screenScale)), width=2)
#### End of blitBackground function

def focus_next_entry(event):
  event.widget.tk_focusNext().focus()
  return 'break'
#### End of focus_next_entry function

def finishPrizeInput(window, entries):
  global TK_LST
  TK_LST = []
  flag = False
  n=len(entries)
  rank1,rank2, prize=0,0,""
  templst = []
  for i in range(n):
    entry = entries[i]
    s = entry.get()
    if i%3 == 0: # 등수1
      flag = False
      try:
        rank1 = int(s)
      except:
        flag = True # 이 행은 무시하고 넘어가야 한다
    elif i%3 == 1 and not flag: #등수2
      try:
        rank2 = int(s)
        if rank2 < rank1:
          rank1,rank2 = rank2, rank1 #Swap
      except:
        flag = True
    elif not flag:
      if s: # Prize 칸이 비어있지 않으면
        prize = s
        if 11<=rank2<=20:
          th = "th: "
        elif rank2%10 == 1:
          th = TH[1]
        elif rank2%10 == 2:
          th = TH[2]
        elif rank2%10 == 3:
          th = TH[3]
        else:
          th = "th: "
        if rank1 != rank2:
          TK_LST.append(str(rank1)+"-"+str(rank2)+th+prize)
        else:
          TK_LST.append(str(rank1)+th+prize)
  window.destroy()
#### End of finishPrizeInput function

def prizeInput(screenScale):
  window = tk.Tk()
  window.title('Prize')
  screen_width = window.winfo_screenwidth()
  screen_height = window.winfo_screenheight()
  width,height = round(800/screenScale), round(1000/screenScale)

  x = (screen_width - width) // 2
  y = (screen_height - height) // 2 - 50
  window.geometry(f"{width}x{height}+{x}+{y}")
  window.configure(bg = 'gray90')
  window.resizable(False, False)
  for i in range(18):
    labelRank = tk.Label(window, font = ("./font/NanumGothic.ttf", round(20/screenScale)), bg = 'gray90', text = "Rank: ")
    labelRank.place(x=round(15/screenScale),y=round(50*i/screenScale)+round(20/screenScale))
    labelWave = tk.Label(window, font = ("./font/NanumGothic.ttf", round(20/screenScale)), bg = 'gray90', text = "~")
    labelWave.place(x=round(160/screenScale), y=round(50*i/screenScale)+round(20/screenScale))
    labelPrize = tk.Label(window, font = ("./font/NanumGothic.ttf", round(20/screenScale)), bg = 'gray90', text = "Prize: ")
    labelPrize.place(x=round(290/screenScale), y=round(50*i/screenScale)+round(20/screenScale))
  button = tk.Button(window, width=round(50/screenScale), height=round(2/screenScale), bg='white', relief="raised", overrelief="solid", borderwidth=4, font = ("./font/NanumGothic.ttf", 15), text= "Okay", command=lambda: finishPrizeInput(window, entries))
  button.place(relx=0.5, y=round(920/screenScale), anchor='n')
  entries = []
  for i in range(54):
    entry = tk.Entry(window, font="Helvetica 20")
    entry.bind('<Tab>', focus_next_entry)
    if i%3 == 0:
      entry.place(x=round(95/screenScale), y=round(50/screenScale)*(i//3)+round(20/screenScale),width=round(60/screenScale), height=round(30/screenScale))
    elif i%3==1:
      entry.place(x=round(195/screenScale), y=round(50/screenScale)*(i//3)+round(20/screenScale),width=round(60/screenScale), height=round(30/screenScale))
    else:
      entry.place(x=round(370/screenScale), y=round(50/screenScale)*(i//3)+round(20/screenScale),width=round(380/screenScale), height=round(30/screenScale))
    entries.append(entry)
  
  window.mainloop()
#### End of prizeInput function

def timeupdate(minute, second, total, amount, currLevel, soundlvlup, lstBreakIdx):
  global LSTLEVELS, LSTBLINDS
  level = currLevel
  if total < amount:
    minute, second, total, level = levelupdate(minute, second, total, amount, currLevel, soundlvlup, 1)
  elif amount >= 0:
    if second < amount:
      minute -= 1
      second = second + 60 - amount
      total -= amount
    else:
      second -= amount
      total -= amount
  #### End of timeupdate function
    
  else: #### amount가 음수일 때, 즉 시간을 증가시킬 때
    if LSTLEVELS[currLevel]*60 < total-amount:
      minute, second, total, level = levelupdate(minute, second, total, amount, currLevel, soundlvlup, -1)
    elif second-amount >= 60:
      minute += 1
      second = second +60 + amount
      total -=amount
    else:
      second-=amount
      total-=amount
  min_break, sec_break = minute,second
  i = lstBreakIdx[level]
  temp = level+1
  while(temp < i):
    min_break +=LSTLEVELS[temp]
    temp+=1
  return minute, second, total, level, min_break, sec_break
#### End of timeupdate function

def makeTimerString(min, sec, total):
  return str(min).zfill(2) + ':' + str(sec).zfill(2)
#### End of makeTimerString function

def levelupdate(minute, second, total, amount, currLevel, soundlvlup, updown):
  global LSTLEVELS, LSTBLINDS
  amount_min = -amount // 60
  soundlvlup.play()
  level = (currLevel+updown) if (currLevel+updown >= 0) else (0)
  if updown > 0: # RIGHT 키 눌러서 다음 블라인드로 넘어갈 때
    min, sec, tot = minute + LSTLEVELS[level], second, total + LSTLEVELS[level] * 60
    min -= 1
    sec = second + 60 - amount
    tot -= amount
  else:
    if level == 0: ## 최초 레벨일 때
      min, sec = LSTLEVELS[1], 0
      level = 1
    else:
      min, sec = amount_min - 1, second
    tot = min*60+sec
  return min, sec,tot,level
#### End of levelupdate function

def blitText(surface, *textobjs):
  for text in textobjs:
    surface.blit(text.getText(), text.getRect())
#### End of blitText function
    
def blitImg(surface, *imgobjs):
  for img in imgobjs:
    surface.blit(img.getImg(), img.getRect())
#### End of blitImg function

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
  label.place(x=100, y=20)
  yesB = tk.Button(window, width=15, height= 2, relief="raised", overrelief="solid", borderwidth=4, font = ("./font/NanumGothic.ttf", 15), text= "Yes", command = lambda: close_window(window, True))
  yesB.place(x = 40, y = 80)
  noB = tk.Button(window, width=15, height= 2, relief="raised", overrelief="solid", borderwidth=4, font = ("./font/NanumGothic.ttf", 15), text= "No", command = lambda: close_window(window, False))
  noB.place(x = 280, y = 80)
  window.mainloop()

def close_window(window, isQuit):
  global TK_VAL
  TK_VAL = isQuit
  window.destroy()

  
def updateTextAfterTimeSkip(LSTBLINDS, currLevel, textCurrLevel, textSBnum, textBBnum, textAntenum, textNextSBnum, textNextBBnum, textNextAntenum, cntBreak):
  if LSTBLINDS[currLevel][0] == 0:   ## 현재 레벨이 브레이크인 경우
    cntBreak+=1
    textCurrLevel.changeColor(BRIGHTRED)
    textCurrLevel.changeContent(font = textCurrLevel.getFont(), content = "Break")
    textSBnum.changeContent(font = textSBnum.getFont(), content = "Break")
    textBBnum.changeContent(font = textBBnum.getFont(), content = "Break")
    textAntenum.changeContent(font = textAntenum.getFont(), content = "Break")
  else:
    textCurrLevel.changeColor(WHITE)
    textCurrLevel.changeContent(font = textCurrLevel.getFont(), content = 'Level '+str(currLevel-cntBreak))
    textSBnum.changeContent(font = textSBnum.getFont(), content = format(LSTBLINDS[currLevel][0], ","))
    textBBnum.changeContent(font = textBBnum.getFont(), content = format(LSTBLINDS[currLevel][1], ","))
    if LSTBLINDS[currLevel][2] != 0:
      temp_str = format(LSTBLINDS[currLevel][2], ",")
    else:
      temp_str = "-"
    textAntenum.changeContent(font = textAntenum.getFont(), content = temp_str)
  if LSTBLINDS[currLevel+1][0] == 0:
    temp_str1 = "Break"
    temp_str2 = "Break"
    temp_str = "Break"
  else:
    temp_str1 = format(LSTBLINDS[currLevel+1][0], ",")
    temp_str2 = format(LSTBLINDS[currLevel+1][1], ",")
    if LSTBLINDS[currLevel+1][2] != 0:
      temp_str = format(LSTBLINDS[currLevel+1][2], ",")
    else:
      temp_str = "-"
  textNextSBnum.changeContent(font = textNextSBnum.getFont(), content = temp_str1)
  textNextBBnum.changeContent(font = textNextBBnum.getFont(), content = temp_str2)
  textNextAntenum.changeContent(font = textNextAntenum.getFont(), content = temp_str)
  return cntBreak

def endAction(surface, textPause, fontPause, rectPauseline, pauseBox, rectPause, shutCenter, shutRadius, screenScale):
  global TK_VAL
  textPause.changeContent(font = fontPause, content = "No more blinds")
  pygame.draw.rect(surface, RED, rectPauseline, width=round(5/screenScale))
  surface.blit(pauseBox, rectPause)
  surface.blit(textPause.getText(), textPause.getRect())
  pygame.draw.circle(surface, RED, shutCenter, shutRadius)
  pygame.draw.circle(surface, BLACK, shutCenter, shutRadius, width = round(2/screenScale))
  pygame.display.flip()
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == ord('q'):
        confirmQuit()
        if TK_VAL:
          running = False
    if event.type == MOUSEBUTTONDOWN:
      if event.button == 1:
        position = pygame.mouse.get_pos()
        if (((position[0] - shutCenter[0]) ** 2 + (position[1] - shutCenter[1]) ** 2) ** 0.5 <= shutRadius):
          confirmQuit()
          if TK_VAL:
            running = False
  time.sleep(0.1)
  return running

def main(lstBLINDS, lstLevels,title, isLoad, vol):
  #print(lstBLINDS, ",", lstLevels, ", \"", title, "\"",", isLoad, ",", vol)
  volume = vol
  global LSTLEVELS, LSTBLINDS, TK_LST, BACKGROUND
  LSTLEVELS = lstLevels
  LSTLEVELS.append(100)

  LSTBLINDS = lstBLINDS
  LSTBLINDS.append((0,0,0))

  lstBreakIdx = [0 for _ in range(len(LSTLEVELS))]
  running = True
  pygame.init()
  
  clock = pygame.time.Clock()
  
  user32 = ctypes.windll.user32
  screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
  midpoint = screensize[0] / 2, screensize[1] / 2 # 화면 중앙점
  screenScale = 1152/screensize[1]
  surface = pygame.display.set_mode(screensize, FULLSCREEN)
  soundLevelup = pygame.mixer.Sound("./sound/levelup.mp3")
  soundLevelup.set_volume(volume)

  ### location, loc 모음집
  locMainTimer = (midpoint[0], round(483/screenScale))
  locCurrBlind = (midpoint[0], midpoint[1] + round(155/screenScale))
  locSettings = (screensize[0] - round(70 /screenScale), screensize[1] - round(70 / screenScale))

  infile = open('./settings/colors', 'r')
  bgColor = infile.readline()
  bgColor = list(map(int, bgColor.split()))
  BACKGROUND = bgColor
  bgUndo = BACKGROUND.copy()
  infile.close()

  pauseBox = pygame.Surface((round(800/screenScale),round(100/screenScale)))
  pauseBox.set_alpha(128)
  pauseBox.fill(YELLOW)

  shutCenter = (screensize[0] - round(50/screenScale), round(50 /screenScale))
  shutRadius = 17

  start_time = time.time()
  timer = 0
  pause_time = 0
  currLevel = 1
  cntBreak = 0
  min, sec, total = LSTLEVELS[currLevel], 0, LSTLEVELS[currLevel]*60
  strTimer = makeTimerString(min, sec, total)
  
  temp = len(LSTLEVELS)-2
  for i in range(len(LSTLEVELS)-2,0,-1):
    if LSTBLINDS[i][0] == 0:
      temp = i
    lstBreakIdx[i-1] = temp
  min_break, sec_break = min,sec
  temp= currLevel+1
  i = lstBreakIdx[currLevel]
  while(temp < i):
    min_break +=LSTLEVELS[temp]
    temp+=1
  strBreakTimer = makeTimerString(min_break,sec_break,total)

  '''imgSettings = pygame.image.load("./img/settings.png")
  imgSettings = pygame.transform.smoothscale(imgSettings,(round(100/screenScale),round(100/screenScale)))'''
  imgSettings = ImgObj(fileAdrress="./img/settings.png", position=locSettings, relative=Relative.CENTER, scalable=True, size = (round(100/screenScale),round(100/screenScale)))
  '''imgBar = pygame.image.load("./img/bar.png")
  imgBar = pygame.transform.scale(imgBar, (round(60/screenScale), round(120/screenScale)))'''
  imgBar = ImgObj(fileAdrress="./img/bar.png", position=(midpoint[0] + round(100/screenScale), midpoint[1] + round(150/screenScale)), relative=Relative.CENTER, scalable=True, size = (round(60/screenScale), round(120/screenScale)))
  imgRBar = pygame.image.load("./img/Rbar.png")
  imgRBar = pygame.transform.scale(imgRBar, (round(40/screenScale), round(80/screenScale)))
  imgGBar = pygame.image.load("./img/Gbar.png")
  imgGBar = pygame.transform.scale(imgGBar, (round(40/screenScale), round(80/screenScale)))
  imgBBar = pygame.image.load("./img/Bbar.png")
  imgBBar = pygame.transform.scale(imgBBar, (round(40/screenScale), round(80/screenScale)))
  imgUpDown = pygame.image.load("./img/Aria_updown.png")
  imgUpDown = pygame.transform.scale(imgUpDown,(round(55/screenScale),round(70/screenScale)))
  imgPauseButton = pygame.image.load("./img/pauseButton.png")
  imgPauseButton = pygame.transform.scale(imgPauseButton,(round(55/screenScale),round(55/screenScale)))
  imgPlayButton = pygame.image.load("./img/playButton.png")
  imgPlayButton = pygame.transform.smoothscale(imgPlayButton,(round(55/screenScale),round(55/screenScale)))
  imgPlusOneButton = pygame.image.load("./img/plusOne.png")
  imgPlusOneButton = pygame.transform.scale(imgPlusOneButton,(round(55/screenScale),round(55/screenScale)))
  imgMinusOneButton = pygame.image.load("./img/minusOne.png")
  imgMinusOneButton = pygame.transform.scale(imgMinusOneButton,(round(55/screenScale),round(55/screenScale)))
  imgLevelUpButton = pygame.image.load("./img/levelUp.png")
  imgLevelUpButton = pygame.transform.smoothscale(imgLevelUpButton,(round(55/screenScale),round(55/screenScale)))
  imgLevelDownButton = pygame.image.load("./img/levelDown.png")
  imgLevelDownButton = pygame.transform.smoothscale(imgLevelDownButton,(round(55/screenScale),round(55/screenScale)))
  imgPrizeButton = pygame.image.load("./img/prize.png")
  imgPrizeButton = pygame.transform.smoothscale(imgPrizeButton,(round(55/screenScale),round(55/screenScale)))


  #### font, font 모음집
  fontTitle = pygame.font.Font('./font/NanumSquareEB.ttf', round(65/screenScale))
  fontMainTimer = pygame.font.Font('./font/NanumSquareEB.ttf', round(200/screenScale))
  fontLevel = pygame.font.Font('./font/NanumSquareB.ttf', round(70/screenScale))
  fontLeftObjs = pygame.font.Font('./font/NanumSquareEB.ttf', round(60/screenScale))
  fontRightObjs = pygame.font.Font('./font/NanumSquareB.ttf', round(42/screenScale))
  fontLeftSmall = pygame.font.Font('./font/NanumGothicExtraBold.ttf', round(30/screenScale))
  fontPause = pygame.font.Font('./font/NanumGothicBold.ttf', round(80/screenScale))
  fontButton = pygame.font.Font('./font/NanumGothicBold.ttf', round(80/screenScale))
  fontVolume = pygame.font.Font('./font/NanumGothic.ttf', round(80/screenScale))

  fontRGB = pygame.font.Font('./font/NanumGothic.ttf', round(45/screenScale))
  fontPrize = pygame.font.Font('./font/SeoulNamsanEB.ttf', round(30/screenScale))


  
  #locTextBlind = (midpoint[0] + round(150/screenScale), midpoint[1] + round(115/screenScale))
  #locTextTEXTBlind = (midpoint[0] - round(200/screenScale), midpoint[1] + round(115/screenScale))

  #region texts

  #### text 모음집
  textMainTimer = TextObj(font = fontMainTimer, content = strTimer, position=locMainTimer, relative='center', color=WHITE)
  textTitleTournament = TextObj(font = fontTitle, content=title, position=(midpoint[0],round(230/screenScale)), relative='center', color=WHITE)
  textCurrLevel = TextObj(font = fontLevel, content='Level '+ str(currLevel), position=(midpoint[0], round(326/screenScale)), relative='center', color=WHITE)
  textSB = TextObj(font = fontLeftObjs, content='Small Blind:', position=(round(505/screenScale), round(605/screenScale)), relative='topright', color=WHITE)
  textBB = TextObj(font = fontLeftObjs, content='Big Blind:', position=(round(505/screenScale), round(680/screenScale)), relative='topright', color=WHITE)
  textAnte = TextObj(font = fontLeftObjs, content='Ante:', position=(round(505/screenScale), round(755/screenScale)), relative='topright', color=WHITE)
  temp = "-" if LSTBLINDS[currLevel][2] == 0 else format(LSTBLINDS[currLevel][2], ",")
  textSBnum = TextObj(font = fontLeftObjs, content=format(LSTBLINDS[currLevel][0], ","), position=(round(515/screenScale), round(605/screenScale)), relative='topleft', color=WHITE)
  textBBnum = TextObj(font = fontLeftObjs, content=format(LSTBLINDS[currLevel][1], ","), position=(round(515/screenScale), round(680/screenScale)), relative='topleft', color=WHITE)
  textAntenum = TextObj(font = fontLeftObjs, content=temp, position=(round(515/screenScale), round(755/screenScale)), relative='topleft', color=WHITE)
  
  textPause = TextObj(font = fontPause, content="Game Paused", color=BLACK, position=locMainTimer, relative="center")
  textNextSB = TextObj(font = fontRightObjs, content='Next Small Blind:', position=(round(1500/screenScale), round(605/screenScale)), relative='topright', color=WHITE)
  textNextBB = TextObj(font = fontRightObjs, content='Next Big Blind:', position=(round(1500/screenScale), round(660/screenScale)), relative='topright', color=WHITE)
  textNextAnte = TextObj(font = fontRightObjs, content='Next Ante:', position=(round(1500/screenScale), round(715/screenScale)), relative='topright', color=WHITE)
  textAvgChips = TextObj(font = fontRightObjs, content='Average Chips:', position=(round(1500/screenScale), round(770/screenScale)), relative='topright', color=WHITE)
  textTotalChips = TextObj(font = fontRightObjs, content='Total Chips:', position=(round(1500/screenScale), round(825/screenScale)), relative='topright', color=WHITE)
  textStartingStack = TextObj(font = fontRightObjs, content='Starting Stack:', position=(round(1500/screenScale), round(880/screenScale)), relative='topright', color=WHITE)
  textTimetoBreak = TextObj(font = fontRightObjs, content='Time to Break:', position=(round(1500/screenScale), round(935/screenScale)), relative='topright', color=WHITE)

  textNextSBnum = TextObj(font = fontRightObjs, content=format(LSTBLINDS[currLevel+1][0], ","), position=(round(1510/screenScale), round(605/screenScale)), relative='topleft', color=WHITE)
  textNextBBnum = TextObj(font = fontRightObjs, content=format(LSTBLINDS[currLevel+1][1], ","), position=(round(1510/screenScale), round(660/screenScale)), relative='topleft', color=WHITE)
  temp = "-" if LSTBLINDS[currLevel][2] == 0 else format(LSTBLINDS[currLevel+1][2], ",")
  textNextAntenum = TextObj(font = fontRightObjs, content=temp, position=(round(1510/screenScale), round(715/screenScale)), relative='topleft', color=WHITE)
  textAvgChipsnum = TextObj(font = fontRightObjs, content='0', position=(round(1510/screenScale), round(770/screenScale)), relative='topleft', color=WHITE)
  textTotalChipsnum = TextObj(font = fontRightObjs, content='0', position=(round(1510/screenScale), round(825/screenScale)), relative='topleft', color=WHITE)
  textStartingStacknum = TextObj(font = fontRightObjs, content='0', position=(round(1510/screenScale), round(880/screenScale)), relative='topleft', color=WHITE)
  textTimetoBreaknum = TextObj(font = fontRightObjs, content=strBreakTimer, position=(round(1510/screenScale), round(935/screenScale)), relative='topleft', color=WHITE)

  textEntrants = TextObj(font = fontLeftSmall, content='Entrants', position=(round(266/screenScale), round(930/screenScale)), relative='center', color=WHITE)
  textPlayersLeft = TextObj(font = fontLeftSmall, content='Players Left', position=(round(765/screenScale), round(930/screenScale)), relative='center', color=WHITE)
  textEntrantsnum = TextObj(font = fontLeftObjs, content='0', position=(round(266/screenScale), round(998/screenScale)), relative='center', color=WHITE)
  textPlayersLeftnum = TextObj(font = fontLeftObjs, content='0', position=(round(765/screenScale), round(998/screenScale)), relative='center', color=WHITE)

  textNext = TextObj(font= fontButton, content="Save", position=(midpoint[0] + round(300/screenScale), round(1030/screenScale)), relative="center", color=BLACK)
  textBack = TextObj(font = fontButton, content="Back", color=BLACK, relative="center", position=(midpoint[0] - round(300/screenScale), round(1030/screenScale)))
  textVol = TextObj(font = fontVolume, content="Volume", position=(midpoint[0] - round(475/screenScale), midpoint[1] + 150), relative="rcenter", color=WHITE)
  textBgSetting = TextObj(font = fontVolume, content="Background", position=(midpoint[0] - round(325/screenScale), midpoint[1] - round(400/screenScale)), relative="center", color=WHITE)
  textR = TextObj(font = fontRGB, content="R", position=(midpoint[0] - round(650/screenScale), midpoint[1] - round(300/screenScale)), relative="center", color=RED)
  textG = TextObj(font = fontRGB, content="G", position=(midpoint[0] - round(650/screenScale), midpoint[1] - round(200/screenScale)), relative="center", color=GREEN)
  textB = TextObj(font = fontRGB, content="B", position=(midpoint[0] - round(650/screenScale), midpoint[1] - round(100/screenScale)), relative="center", color=BLUE)

  textPrizeRight = TextObj(font = fontLeftSmall, content='Prize', position=(round(1713/screenScale), round(306/screenScale)), relative='center', color=WHITE)

  lstTextPrize = []


  #endregion

  numPlayer, numChips, numAverage, numEntries, numStarting = 0,0,0,0,0
  temp_input = 0

  #### rect 모음집
  rectMidPoint = pygame.Rect(0,0,20,20)
  rectMidPoint.center = midpoint
  rectPause = pygame.Rect(0,0,round(800/screenScale),round(100/screenScale))
  rectPause.center = locMainTimer
  rectPauseline = pygame.Rect(0,0,round(800/screenScale),round(100/screenScale))
  rectPauseline.center = locMainTimer
  '''rectSettings = imgSettings.get_rect()
  rectSettings.center = locSettings'''
  '''rectBar = imgBar.get_rect()
  rectBar.center = (midpoint[0] + round(100/screenScale), midpoint[1] + round(150/screenScale))'''
  xRbar, xGbar, xBbar = midpoint[0] - round(((255 - BACKGROUND[0]) * 2 + 90)/screenScale), midpoint[0] - round(((255 - BACKGROUND[1]) * 2 + 90)/screenScale), midpoint[0] - round(((255 - BACKGROUND[2]) * 2 + 90)/screenScale)
  rectRBar = imgRBar.get_rect()
  rectRBar.center = (xRbar, midpoint[1] - round(300/screenScale))
  rectGBar = imgGBar.get_rect()
  rectGBar.center = (xGbar, midpoint[1] - round(200/screenScale))
  rectBBar = imgBBar.get_rect()
  rectBBar.center = (xBbar, midpoint[1] - round(100/screenScale))
  rectUpDown1 = imgUpDown.get_rect()
  rectUpDown1.centery = round(998/screenScale)
  rectUpDown1.right = round(500/screenScale)
  rectUpDown2 = imgUpDown.get_rect()
  rectUpDown2.centery = round(998/screenScale)
  rectUpDown2.right = round(1019/screenScale)
  rectPauseButton = imgPauseButton.get_rect()
  rectPauseButton.center = (midpoint[0], round(1079/screenScale))
  rectPlayButton = imgPlayButton.get_rect()
  rectPlayButton.center = (midpoint[0], round(1079/screenScale))
  rectPlusOneButton = imgPlusOneButton.get_rect()
  rectPlusOneButton.center = (midpoint[0] + round(65), round(1079/screenScale))
  rectMinusOneButton = imgMinusOneButton.get_rect()
  rectMinusOneButton.center = (midpoint[0] - round(65), round(1079/screenScale))
  rectLevelUpButton = imgLevelUpButton.get_rect()
  rectLevelUpButton.center = (midpoint[0] + round(130), round(1079/screenScale))
  rectLevelDownButton = imgLevelDownButton.get_rect()
  rectLevelDownButton.center = (midpoint[0] - round(130), round(1079/screenScale))
  rectPrizeButton = imgPrizeButton.get_rect()
  rectPrizeButton.center = (midpoint[0] - round(195), round(1079/screenScale))
  rectNext = pygame.Rect(0,0,round(500/screenScale),round(140/screenScale))
  rectNext.center = (midpoint[0] + round(300/screenScale), round(1030/screenScale))
  rectBack = pygame.Rect(0,0,round(500/screenScale),round(140/screenScale))
  rectBack.center = (midpoint[0] - round(300/screenScale), round(1030/screenScale))
  rectPrizeBoxRight = pygame.Rect(0,0,round(610/screenScale),round(60/screenScale))
  rectPrizeBoxRight.topleft = (round(1408/screenScale), round(276/screenScale))
  bigRect = pygame.Rect(0,0,round(1996/screenScale),round(1096/screenScale))
  bigRect.topleft = (round(26/screenScale), round(28/screenScale))
  

  pauseEvent = True
  pause_start = time.time()
  pause_time = 0
  flagback = "quit"
  flagSettings = False
  flagPrizeStop = False
  flagCounter = False
  prizeStopTimer = 0
  barMove, rbarMove, gbarMove, bbarMove = False, False, False, False
  clickedNum = -1
  dictClicked = {0:textPlayersLeftnum, 1:textAvgChipsnum, 2:textTotalChipsnum, 3: textEntrantsnum, 4:textStartingStacknum}
  dictNum = {0:numPlayer, 1:numAverage, 2:numChips, 3:numEntries, 4:numStarting}

  totalFPS = 0

  while running:
    totalFPS += 1
    if flagPrizeStop and (time.time() - prizeStopTimer > 5) and len(lstTextPrize) > 7:
      flagCounter = True
      for i in range(len(lstTextPrize)): # 위치 초기화
        #position=(round(1425/screenScale), round((342+PRIZEINTERVAL*i)/screenScale))
        lstTextPrize[i].changePosition(relative = "topleft", position=(round(1425/screenScale), round((342+PRIZEINTERVAL*i)/screenScale)))
    if flagCounter and (time.time() - prizeStopTimer > 10) and len(lstTextPrize) > 7:
      flagPrizeStop, flagCounter = False, False
      prizeStopTimer = 0
    if len(lstTextPrize) > 7 and not flagPrizeStop:
      for text in lstTextPrize:
        text.changePosition(relative = "topleft", position = [text.getPos()[0], text.getPos()[1] - 1 * (totalFPS % 2)])
      if lstTextPrize[-1].getRect().bottom <= 580:
        print(2)
        flagPrizeStop = True
        prizeStopTimer = time.time()
    if TK_VAL:
      running = False
      continue
    if pauseEvent:
      flag = True
      
      if not flagSettings:
        blitBackground(surface, bigRect, screenScale)

        if clickedNum != -1:
          try:
            pygame.draw.rect(surface, PALEGRAY, dictClicked[clickedNum].getRect())
          except:
            print("clickedNum Error")
        for text in lstTextPrize:
          if (round(340/screenScale) <= text.getRect().bottom <= round(587/screenScale)):
            surface.blit(text.getText(), text.getRect())
        pygame.draw.rect(surface, BACKGROUND, rectPrizeBoxRight)
        pygame.draw.rect(surface, WHITE, rectPrizeBoxRight, width=2)
        blitText(surface, textMainTimer, textTitleTournament, textCurrLevel, textSB, textBB, textAnte, textSBnum, textBBnum, textAntenum, textNextSB, textNextBB, textNextAnte, textAvgChips, textTotalChips, textStartingStack, textTimetoBreak, textNextSBnum, textNextBBnum, textNextAntenum, textAvgChipsnum, textTotalChipsnum, textStartingStacknum, textTimetoBreaknum, textEntrants, textPlayersLeft, textEntrantsnum, textPlayersLeftnum, textPrizeRight)
        pygame.draw.rect(surface, RED, rectPauseline, width=round(5/screenScale))
        surface.blit(pauseBox, rectPause)
        surface.blit(textPause.getText(), textPause.getRect())
        pygame.draw.circle(surface, RED, shutCenter, shutRadius)
        pygame.draw.circle(surface, BLACK, shutCenter, shutRadius, width = round(2/screenScale))
        surface.blit(imgUpDown, rectUpDown1)
        surface.blit(imgUpDown, rectUpDown2)
        #surface.blit(imgSettings, rectSettings)
        blitImg(surface, imgSettings)
        surface.blit(imgPlayButton, rectPlayButton)
        surface.blit(imgPlusOneButton, rectPlusOneButton)
        surface.blit(imgMinusOneButton, rectMinusOneButton)
        surface.blit(imgLevelUpButton, rectLevelUpButton)
        surface.blit(imgLevelDownButton, rectLevelDownButton)
        surface.blit(imgPrizeButton, rectPrizeButton)
        pygame.draw.rect(surface, WHITE, bigRect, width=8)
      else:
        surface.fill(BACKGROUND)
        pygame.draw.line(surface, WHITE, (midpoint[0] - round(400/screenScale), midpoint[1] + round(150/screenScale)), (midpoint[0] + round(600/screenScale), midpoint[1] + round(150/screenScale)), width=4) # Volume line
        #surface.blit(imgBar, rectBar)
        blitImg(surface, imgBar)
        blitText(surface, textVol, textBgSetting, textR, textG, textB)
        pygame.draw.rect(surface, PALEGRAY, rectNext)
        pygame.draw.rect(surface, DARKGRAY, rectNext, width = round(4/screenScale))
        surface.blit(textNext.getText(), textNext.getRect())
        pygame.draw.rect(surface, PALEGRAY, rectBack)
        pygame.draw.rect(surface, DARKGRAY, rectBack, width = round(4/screenScale))
        pygame.draw.line(surface, WHITE, (midpoint[0] - round(600/screenScale), midpoint[1] - round(300/screenScale)), (midpoint[0] - round(90/screenScale), midpoint[1] - round(300/screenScale)), width = 2) # Bg R line
        pygame.draw.line(surface, WHITE, (midpoint[0] - round(600/screenScale), midpoint[1] - round(200/screenScale)), (midpoint[0] - round(90/screenScale), midpoint[1] - round(200/screenScale)), width = 2) # Bg G line
        pygame.draw.line(surface, WHITE, (midpoint[0] - round(600/screenScale), midpoint[1] - round(100/screenScale)), (midpoint[0] - round(90/screenScale), midpoint[1] - round(100/screenScale)), width = 2) # Bg B line
        surface.blit(textBack.getText(), textBack.getRect())
        surface.blit(imgRBar, rectRBar)
        surface.blit(imgGBar, rectGBar)
        surface.blit(imgBBar, rectBBar)
      pygame.display.flip()
      clock.tick(FPS)
      pause_time_to_add = pause_start - time.time()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        elif event.type == KEYDOWN:
          if not flagSettings:
            if event.key == K_SPACE:
              soundLevelup.play()
              pauseEvent = False
              flag = False
              textSBnum.changeContent(font = textSBnum.getFont(), content = format(LSTBLINDS[currLevel][0], ","))
              textBBnum.changeContent(font = textBBnum.getFont(), content = format(LSTBLINDS[currLevel][1], ","))
              if LSTBLINDS[currLevel][2] != 0:
                textAntenum.changeContent(font = fontLeftObjs, content = format(LSTBLINDS[currLevel][2], ","))
            if event.key in K_NUM or event.key == K_BACKSPACE:
              if clickedNum != -1:
                temp_input = (temp_input*10 + processAscii(event.key)) if (event.key in K_NUM) else (temp_input//10)
                dictClicked[clickedNum].changeColor(BLACK)
                dictClicked[clickedNum].changeContent(font=dictClicked[clickedNum].getFont(), content= format(temp_input, ","))
            if pygame.key.name(event.key) == "return" or pygame.key.name(event.key) == "enter":
              if clickedNum != -1: ### dictClicked = {0:textPlayernum, 1:textAveragenum, 2:textChipsinplaynum, 3: textEntriesnum, 4:textStartingstacknum}
                dictNum[clickedNum] = temp_input
                dictClicked[clickedNum].changeColor(WHITE)
                dictClicked[clickedNum].changeContent(font = dictClicked[clickedNum].getFont(), content = format(dictNum[clickedNum], ","))
                if (clickedNum==0 or clickedNum ==2) and dictNum[0]>0:
                  dictNum[1] = dictNum[2] // dictNum[0]
                  textAvgChipsnum.changeColor(WHITE)
                  textAvgChipsnum.changeContent(font = textAvgChipsnum.getFont(), content = format(dictNum[1], ","))                  
              temp_input = 0
              clickedNum=-1
            if event.key == K_RIGHT or event.key == K_LEFT: ### 1분 뒤로
              factor = 60 if event.key == K_RIGHT else -60
              min, sec, total, newLevel, min_break, sec_break = timeupdate(min, sec, total, factor, currLevel, soundLevelup,lstBreakIdx)
              if newLevel != currLevel:
                currLevel = newLevel
                if LSTLEVELS[currLevel]==0: ### End of blind
                  while running:
                    running = endAction(surface, textPause, fontPause, rectPauseline, pauseBox, rectPause, shutCenter, shutRadius, screenScale)
                try:
                  cntBreak = updateTextAfterTimeSkip(LSTBLINDS, currLevel, textCurrLevel, textSBnum, textBBnum, textAntenum, textNextSBnum, textNextBBnum, textNextAntenum, cntBreak)
                except:
                  print("No levels left")
              strTimer = makeTimerString(min, sec, total)
              textMainTimer.changeContent(content = strTimer, font = fontMainTimer)
              strBreakTimer = makeTimerString(min_break,sec_break,total)
              textTimetoBreaknum.changeContent(font = textTimetoBreaknum.getFont(), content = strBreakTimer)
          if event.key == ord('q'):
            confirmQuit()
          if event.key == K_ESCAPE:
            surface = pygame.display.set_mode((500,500))
          
        elif event.type == MOUSEBUTTONDOWN:
          if event.button == 1:
            position = pygame.mouse.get_pos()
            if not flagSettings:
              temp_input = 0
              if clickedNum!=-1:
                dictClicked[clickedNum].changeColor(WHITE)
                dictClicked[clickedNum].changeContent(font = dictClicked[clickedNum].getFont(), content = format(dictNum[clickedNum], ","))
                clickedNum=-1
              elif mouseInRect(textPlayersLeftnum.getRect(), position):
                clickedNum=0
              elif mouseInRect(textAvgChipsnum.getRect(), position):
                clickedNum=1
              elif mouseInRect(textTotalChipsnum.getRect(), position):
                clickedNum=2
              elif mouseInRect(textEntrantsnum.getRect(), position):
                clickedNum=3
              elif mouseInRect(textStartingStacknum.getRect(), position):
                clickedNum=4
              elif (((position[0] - shutCenter[0]) ** 2 + (position[1] - shutCenter[1]) ** 2) ** 0.5 <= shutRadius):
                confirmQuit()
              if mouseInRect(imgSettings.getRect(), position):
                flagSettings = True
                bgUndo = BACKGROUND.copy()
                xRbar, xGbar, xBbar = rectRBar.centerx, rectGBar.centerx, rectBBar.centerx
                imgBar.getRect().centerx = midpoint[0] - round(400/screenScale) + round(volume * 1000)
              if (round(445/screenScale)<=position[0]<=round(500/screenScale) and round(961/screenScale)<=position[1]<= round(988/screenScale)): #entrants up button
                # dictNum = {0:numPlayer, 1:numAverage, 2:numChips, 3:numEntries, 4:numStarting}
                dictNum[3] += 1
                dictClicked[3].changeContent(font = dictClicked[3].getFont(), content=str(dictNum[3]))
              elif (round(445/screenScale)<=position[0]<=round(500/screenScale) and round(1007/screenScale)<=position[1]<= round(1032/screenScale)):
                if(dictNum[3] > 0):
                  dictNum[3] -= 1
                  dictClicked[3].changeContent(font = dictClicked[3].getFont(), content=str(dictNum[3]))
              elif (round(964/screenScale)<=position[0]<=round(1019/screenScale) and round(961/screenScale)<=position[1]<= round(988/screenScale)): #player up button
                # dictNum = {0:numPlayer, 1:numAverage, 2:numChips, 3:numEntries, 4:numStarting}
                dictNum[0] += 1
                dictClicked[0].changeContent(font = dictClicked[0].getFont(), content=str(dictNum[0]))
                dictNum[1] = round(dictNum[2]/dictNum[0])
                dictClicked[1].changeContent(font = dictClicked[1].getFont(), content=str(dictNum[1]))
              elif (round(964/screenScale)<=position[0]<=round(1019/screenScale) and round(1007/screenScale)<=position[1]<= round(1032/screenScale)): #player down button
                # dictNum = {0:numPlayer, 1:numAverage, 2:numChips, 3:numEntries, 4:numStarting}\
                if dictNum[0] > 0:
                  dictNum[0] -= 1
                  dictClicked[0].changeContent(font = dictClicked[0].getFont(), content=str(dictNum[0]))
                  if dictNum[0] != 0:
                    dictNum[1] = round(dictNum[2]/dictNum[0])
                    dictClicked[1].changeContent(font = dictClicked[1].getFont(), content=str(dictNum[1]))
              elif mouseInRect(rectPlusOneButton, position) or mouseInRect(rectMinusOneButton, position):
                factor = 60 if mouseInRect(rectPlusOneButton, position) else -60
                min, sec, total, newLevel, min_break, sec_break = timeupdate(min, sec, total, factor, currLevel, soundLevelup,lstBreakIdx)
                if newLevel != currLevel:
                  currLevel = newLevel
                  if LSTLEVELS[currLevel]==0: ### End of blind
                    while running:
                      running = endAction(surface, textPause, fontPause, rectPauseline, pauseBox, rectPause, shutCenter, shutRadius, screenScale)
                  try:
                    cntBreak = updateTextAfterTimeSkip(LSTBLINDS, currLevel, textCurrLevel, textSBnum, textBBnum, textAntenum, textNextSBnum, textNextBBnum, textNextAntenum, cntBreak)

                  except:
                    print("No levels left")
                strTimer = makeTimerString(min, sec, total)
                textMainTimer.changeContent(content = strTimer, font = fontMainTimer)
                strBreakTimer = makeTimerString(min_break,sec_break,total)
                textTimetoBreaknum.changeContent(font = textTimetoBreaknum.getFont(), content = strBreakTimer)
              elif mouseInRect(rectPlayButton, position):
                soundLevelup.play()
                pauseEvent = False
                flag = False
                textSBnum.changeContent(font = textSBnum.getFont(), content = format(LSTBLINDS[currLevel][0], ","))
                textBBnum.changeContent(font = textBBnum.getFont(), content = format(LSTBLINDS[currLevel][1], ","))
                if LSTBLINDS[currLevel][2] != 0:
                  textAntenum.changeContent(font = fontLeftObjs, content = format(LSTBLINDS[currLevel][2], ","))
              elif (mouseInRect(rectLevelUpButton, position) and LSTLEVELS[currLevel] != 0) or (mouseInRect(rectLevelDownButton, position) and LSTLEVELS[currLevel - 1] != 0): 
                currLevel = currLevel + 1 if mouseInRect(rectLevelUpButton, position) else currLevel - 1
                min, sec, total = LSTLEVELS[currLevel], 0, 60 * min
                min_break = min
                temp= currLevel+1
                i = lstBreakIdx[currLevel]
                while(temp < i):
                  min_break +=LSTLEVELS[temp]
                  temp+=1
                strBreakTimer = makeTimerString(min_break,sec_break,total)
                try:
                  cntBreak = updateTextAfterTimeSkip(LSTBLINDS, currLevel, textCurrLevel, textSBnum, textBBnum, textAntenum, textNextSBnum, textNextBBnum, textNextAntenum, cntBreak)
                  soundLevelup.play()
                except:
                  print("No levels left")
                strTimer = makeTimerString(min, sec, total)
                textMainTimer.changeContent(content = strTimer, font = fontMainTimer)
                strBreakTimer = makeTimerString(min_break,sec_break,total)
                textTimetoBreaknum.changeContent(font = textTimetoBreaknum.getFont(), content = strBreakTimer)
              elif mouseInRect(rectPrizeButton, position):
                prizeInput(screenScale)
                lstTextPrize = []
                flagPrizeStop = True
                prizeStopTimer = time.time()
                for i in range(len(TK_LST)):
                  temp = TextObj(font = fontPrize, content=TK_LST[i], relative="topleft", color=WHITE, position=(round(1425/screenScale), round((342+PRIZEINTERVAL*i)/screenScale)))
                  lstTextPrize.append(temp)
            else:
              pygame.mouse.get_rel()
              if mouseInRect(imgBar.getRect(), position):
                barMove = True
              elif mouseInRect(rectRBar, position):
                rbarMove = True
              elif mouseInRect(rectGBar, position):
                gbarMove = True
              elif mouseInRect(rectBBar, position):
                bbarMove = True
              elif mouseInRect(rectNext, position):
                flagSettings = False
                barMove, rbarMove, gbarMove, bbarMove = False, False, False, False
                vol = (imgBar.getRect().centerx - midpoint[0] + 400/screenScale) / float(1000)
                outfile = open("./settings/vol", "w")
                outfile.write(str(vol))
                outfile.close()
                outfile = open('./settings/colors', 'w')
                outfile.write(str(BACKGROUND[0]) + " " + str(BACKGROUND[1]) + " " + str(BACKGROUND[2]))
                outfile.close()
              elif mouseInRect(rectBack, position):
                flagSettings = False
                barMove, rbarMove, gbarMove, bbarMove = False, False, False, False
                BACKGROUND = bgUndo.copy()
                rectRBar.centerx, rectGBar.centerx, rectBBar.centerx = xRbar, xGbar, xBbar
        elif event.type == MOUSEMOTION and flagSettings:
          if barMove:
            x,y,z = pygame.mouse.get_pressed()
            if x:
              mx, my = pygame.mouse.get_rel()
              imgBar.getRect().x += mx
              if imgBar.getRect().centerx < midpoint[0] - round(400/screenScale):
                imgBar.getRect().centerx = midpoint[0] - round(400/screenScale)
              if imgBar.getRect().centerx > midpoint[0] + round(600/screenScale):
                imgBar.getRect().centerx = midpoint[0] + round(600/screenScale)
          elif rbarMove:
            x,y,z = pygame.mouse.get_pressed()
            if x:
              mx, my = pygame.mouse.get_rel()
              rectRBar.x += mx
              if rectRBar.centerx < midpoint[0] - round(600/screenScale):
                rectRBar.centerx = midpoint[0] - round(600/screenScale)
              if rectRBar.centerx > midpoint[0] - round(90/screenScale):
                rectRBar.centerx = midpoint[0] - round(90/screenScale)
          elif gbarMove:
            x,y,z = pygame.mouse.get_pressed()
            if x:
              mx, my = pygame.mouse.get_rel()
              rectGBar.x += mx
              if rectGBar.centerx < midpoint[0] - round(600/screenScale):
                rectGBar.centerx = midpoint[0] - round(600/screenScale)
              if rectGBar.centerx > midpoint[0] - round(90/screenScale):
                rectGBar.centerx = midpoint[0] - round(90/screenScale)
          elif bbarMove:
            x,y,z = pygame.mouse.get_pressed()
            if x:
              mx, my = pygame.mouse.get_rel()
              rectBBar.x += mx
              if rectBBar.centerx < midpoint[0] - round(600/screenScale):
                rectBBar.centerx = midpoint[0] - round(600/screenScale)
              if rectBBar.centerx > midpoint[0] - round(90/screenScale):
                rectBBar.centerx = midpoint[0] - round(90/screenScale)
        elif event.type == MOUSEBUTTONUP and flagSettings:
          if barMove:
            volume = (imgBar.getRect().centerx - midpoint[0] + 400/screenScale) / float(1000)
            soundLevelup.set_volume(volume)
            soundLevelup.play()
          elif rbarMove:
            r = 255 - round(((midpoint[0] - rectRBar.centerx) * screenScale - 90) / 2)
            r = r if r >= 0 else 0
            r = r if r <= 255 else 255
            BACKGROUND[0] = r
          elif gbarMove:
            r = 255 - round(((midpoint[0] - rectGBar.centerx) * screenScale - 90) / 2)
            r = r if r >= 0 else 0
            r = r if r <= 255 else 255
            BACKGROUND[1] = r
          elif bbarMove:
            r = 255 - round(((midpoint[0] - rectBBar.centerx) * screenScale - 90) / 2)
            r = r if r >= 0 else 0
            r = r if r <= 255 else 255
            BACKGROUND[2] = r
            #print(r, rectBBar.center)
          barMove, rbarMove, gbarMove, bbarMove = False, False, False, False
          
      if flag:
        continue
      else:
        pause_time += pause_time_to_add
        pauseEvent = False
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == KEYDOWN:
        if event.key == ord('q'):
          confirmQuit()
        if event.key == K_ESCAPE:
          surface = pygame.display.set_mode((500,500))
        if event.key == K_SPACE:
          if pauseEvent:
            pauseEvent = False
          else:
            pause_start = time.time()
            pauseEvent = True
            continue
            
        if event.key in K_NUM or event.key == K_BACKSPACE:
          if clickedNum != -1:
            temp_input = (temp_input*10 + processAscii(event.key)) if (event.key in K_NUM) else (temp_input//10)
            dictClicked[clickedNum].changeColor(BLACK)
            dictClicked[clickedNum].changeContent(font = dictClicked[clickedNum].getFont(), content = format(temp_input, ","))
          elif event.key == K_BACKSPACE:
            if isLoad:
              flagback = "load"
            else:
              flagback = "save"
            running = False
        if pygame.key.name(event.key) == "return" or pygame.key.name(event.key) == "enter":
          if clickedNum != -1:
            dictNum[clickedNum]=temp_input
            dictClicked[clickedNum].changeColor(WHITE)
            dictClicked[clickedNum].changeContent(font = dictClicked[clickedNum].getFont(), content = format(dictNum[clickedNum], ","))
            if (clickedNum==0 or clickedNum==2) and dictNum[0] > 0:
              dictNum[1] = dictNum[2] // dictNum[0]
              textAvgChipsnum.changeColor(WHITE)
              textAvgChipsnum.changeContent(font = textAvgChipsnum.getFont(), content = format(dictNum[1], ","))
          temp_input = 0
          clickedNum = -1
        if event.key == K_RIGHT or event.key == K_LEFT: ### 1분 뒤로
          factor = 60 if event.key == K_RIGHT else -60
          min, sec, total, newLevel, min_break, sec_break = timeupdate(min, sec, total, factor, currLevel, soundLevelup,lstBreakIdx)
          if newLevel != currLevel:
            currLevel = newLevel
            if LSTLEVELS[currLevel]==0: ### End of blind
              while running:
                running = endAction(surface, textPause, fontPause, rectPauseline, pauseBox, rectPause, shutCenter, shutRadius, screenScale)
            try:
              cntBreak = updateTextAfterTimeSkip(LSTBLINDS, currLevel, textCurrLevel, textSBnum, textBBnum, textAntenum, textNextSBnum, textNextBBnum, textNextAntenum, cntBreak)

            except:
              print("No levels left")
          strTimer = makeTimerString(min, sec, total)
          textMainTimer.changeContent(content = strTimer, font = fontMainTimer)
          strBreakTimer = makeTimerString(min_break,sec_break,total)
          textTimetoBreaknum.changeContent(font = textTimetoBreaknum.getFont(), content = strBreakTimer)
        
      elif event.type == MOUSEBUTTONDOWN:
          if event.button == 1:
            position = pygame.mouse.get_pos()
            temp_input = 0
            if clickedNum!=-1:
              dictClicked[clickedNum].changeColor(WHITE)
              dictClicked[clickedNum].changeContent(font = dictClicked[clickedNum].getFont(), content = format(dictNum[clickedNum], ","))
              clickedNum=-1
            elif mouseInRect(textPlayersLeftnum.getRect(), position):
              clickedNum=0
            elif mouseInRect(textAvgChipsnum.getRect(), position):
              clickedNum=1
            elif mouseInRect(textTotalChipsnum.getRect(), position):
              clickedNum=2
            elif mouseInRect(textEntrantsnum.getRect(), position):
              clickedNum=3
            elif mouseInRect(textStartingStacknum.getRect(), position):
              clickedNum=4
            if (((position[0] - shutCenter[0]) ** 2 + (position[1] - shutCenter[1]) ** 2) ** 0.5 <= shutRadius):
              confirmQuit()
            if (round(445/screenScale)<=position[0]<=round(500/screenScale) and round(961/screenScale)<=position[1]<= round(988/screenScale)): #entrants up button
              # dictNum = {0:numPlayer, 1:numAverage, 2:numChips, 3:numEntries, 4:numStarting}
              dictNum[3] += 1
              dictClicked[3].changeContent(font = dictClicked[3].getFont(), content=str(dictNum[3]))
            elif (round(445/screenScale)<=position[0]<=round(500/screenScale) and round(1007/screenScale)<=position[1]<= round(1032/screenScale)):
              if(dictNum[3] > 0):
                dictNum[3] -= 1
                dictClicked[3].changeContent(font = dictClicked[3].getFont(), content=str(dictNum[3]))
            elif (round(964/screenScale)<=position[0]<=round(1019/screenScale) and round(961/screenScale)<=position[1]<= round(988/screenScale)): #player up button
                # dictNum = {0:numPlayer, 1:numAverage, 2:numChips, 3:numEntries, 4:numStarting}
              dictNum[0] += 1
              dictClicked[0].changeContent(font = dictClicked[0].getFont(), content=str(dictNum[0]))
              dictNum[1] = round(dictNum[2]/dictNum[0])
              dictClicked[1].changeContent(font = dictClicked[1].getFont(), content=str(dictNum[1]))
            elif (round(964/screenScale)<=position[0]<=round(1019/screenScale) and round(1007/screenScale)<=position[1]<= round(1032/screenScale)): #player down button
              # dictNum = {0:numPlayer, 1:numAverage, 2:numChips, 3:numEntries, 4:numStarting}\
              if dictNum[0] > 0:
                dictNum[0] -= 1
                dictClicked[0].changeContent(font = dictClicked[0].getFont(), content=str(dictNum[0]))
                if dictNum[0] != 0:
                  dictNum[1] = round(dictNum[2]/dictNum[0])
                  dictClicked[1].changeContent(font = dictClicked[1].getFont(), content=str(dictNum[1]))
            elif mouseInRect(rectPlusOneButton, position) or mouseInRect(rectMinusOneButton, position):
              factor = 60 if mouseInRect(rectPlusOneButton, position) else -60
              min, sec, total, newLevel, min_break, sec_break = timeupdate(min, sec, total, factor, currLevel, soundLevelup,lstBreakIdx)
              if newLevel != currLevel:
                currLevel = newLevel
                if LSTLEVELS[currLevel]==0: ### End of blind
                  while running:
                    running = endAction(surface, textPause, fontPause, rectPauseline, pauseBox, rectPause, shutCenter, shutRadius, screenScale)
                try:
                  cntBreak = updateTextAfterTimeSkip(LSTBLINDS, currLevel, textCurrLevel, textSBnum, textBBnum, textAntenum, textNextSBnum, textNextBBnum, textNextAntenum, cntBreak)

                except:
                  print("No levels left")
              strTimer = makeTimerString(min, sec, total)
              textMainTimer.changeContent(content = strTimer, font = fontMainTimer)
              strBreakTimer = makeTimerString(min_break,sec_break,total)
              textTimetoBreaknum.changeContent(font = textTimetoBreaknum.getFont(), content = strBreakTimer)
            elif mouseInRect(rectPauseButton, position):
              if pauseEvent:
                pauseEvent = False
              else:
                pause_start = time.time()
                pauseEvent = True
                continue
            elif (mouseInRect(rectLevelUpButton, position) and LSTLEVELS[currLevel] != 0) or (mouseInRect(rectLevelDownButton, position) and LSTLEVELS[currLevel - 1] != 0):
              currLevel = currLevel + 1 if mouseInRect(rectLevelUpButton, position) else currLevel - 1
              min, sec, total = LSTLEVELS[currLevel], 0, 60 * min
              min_break = min
              temp= currLevel+1
              i = lstBreakIdx[currLevel]
              while(temp < i):
                min_break +=LSTLEVELS[temp]
                temp+=1
              strBreakTimer = makeTimerString(min_break,sec_break,total)
              try:
                cntBreak = updateTextAfterTimeSkip(LSTBLINDS, currLevel, textCurrLevel, textSBnum, textBBnum, textAntenum, textNextSBnum, textNextBBnum, textNextAntenum, cntBreak)
                soundLevelup.play()
              except:
                print("No levels left")
              strTimer = makeTimerString(min, sec, total)
              textMainTimer.changeContent(content = strTimer, font = fontMainTimer)
              strBreakTimer = makeTimerString(min_break,sec_break,total)
              textTimetoBreaknum.changeContent(font = textTimetoBreaknum.getFont(), content = strBreakTimer)
            elif mouseInRect(rectPrizeButton, position):
              prizeInput(screenScale)
              lstTextPrize = []
              flagPrizeStop = True
              prizeStopTimer = time.time()
              for i in range(len(TK_LST)):
                temp = TextObj(font = fontPrize, content=TK_LST[i], relative="topleft", color=WHITE, position=(round(1590/screenScale), round((342+PRIZEINTERVAL*i)/screenScale)))
                lstTextPrize.append(temp)

    #####
    if(time.time() - start_time + pause_time > timer): ### 매 1초마다
      timer+=1
      min, sec, total, newLevel, min_break, sec_break = timeupdate(min, sec, total, 1, currLevel, soundLevelup,lstBreakIdx)
      if newLevel != currLevel:
        currLevel = newLevel
        if LSTLEVELS[currLevel]==0: ### End of blind
          while running:
            running = endAction(surface, textPause, fontPause, rectPauseline, pauseBox, rectPause, shutCenter, shutRadius, screenScale)
        try:
          cntBreak = updateTextAfterTimeSkip(LSTBLINDS, currLevel, textCurrLevel, textSBnum, textBBnum, textAntenum, textNextSBnum, textNextBBnum, textNextAntenum, cntBreak)
        except:
          print("No levels left")
      strTimer = makeTimerString(min, sec, total)
      textMainTimer.changeContent(content = strTimer, font = fontMainTimer)
      strBreakTimer = makeTimerString(min_break,sec_break,total)
      textTimetoBreaknum.changeContent(font = fontRightObjs, content = strBreakTimer)
    blitBackground(surface, bigRect, screenScale)
    if clickedNum != -1:
      pygame.draw.rect(surface, PALEGRAY, dictClicked[clickedNum].getRect())
    for text in lstTextPrize:
      if (round(340/screenScale) <= text.getRect().bottom <= round(587/screenScale)):
        surface.blit(text.getText(), text.getRect())
    pygame.draw.rect(surface, BACKGROUND, rectPrizeBoxRight)
    pygame.draw.rect(surface, WHITE, rectPrizeBoxRight, width=2)
    blitText(surface, textMainTimer, textTitleTournament, textCurrLevel, textSB, textBB, textAnte, textSBnum, textBBnum, textAntenum, textNextSB, textNextBB, textNextAnte, textAvgChips, textTotalChips, textStartingStack, textTimetoBreak, textNextSBnum, textNextBBnum, textNextAntenum, textAvgChipsnum, textTotalChipsnum, textStartingStacknum, textTimetoBreaknum, textEntrants, textPlayersLeft, textEntrantsnum, textPlayersLeftnum, textPrizeRight)
    pygame.draw.circle(surface, RED, shutCenter, shutRadius)
    pygame.draw.circle(surface, BLACK, shutCenter, shutRadius, width = round(2/screenScale))
    surface.blit(imgUpDown, rectUpDown1)
    surface.blit(imgUpDown, rectUpDown2)
    surface.blit(imgPauseButton, rectPauseButton)
    surface.blit(imgPlusOneButton, rectPlusOneButton)
    surface.blit(imgMinusOneButton, rectMinusOneButton)
    surface.blit(imgLevelUpButton, rectLevelUpButton)
    surface.blit(imgLevelDownButton, rectLevelDownButton)
    surface.blit(imgPrizeButton, rectPrizeButton)
    
    
    #clock.tick(FPS)
    pygame.draw.rect(surface, WHITE, bigRect, width=8)
    pygame.display.flip()
    clock.tick(FPS) / 1000
  soundLevelup.stop()
  pygame.quit()
  if flagback == "load":
    return 1
  elif flagback == "save":
    return 2
  else:
    return 0
#### End of main function
  
main([0, [100, 200, 0], [200, 400, 0], [300, 600, 0], [400, 800, 0], [0, 0, 0], [500, 1000, 1000], [600, 1200, 1200], [800, 1600, 1600], [1000, 2000, 2000], [1500, 3000, 3000], [0, 0, 0], [2000, 4000, 4000], [2500, 5000, 5000], [3000, 6000, 6000], [4000, 8000, 8000], [5000, 10000, 10000], [5500, 11000, 11000], [6000, 12000, 12000], [8000, 16000, 16000], [10000, 20000, 20000], [15000, 30000, 30000], [20000, 40000, 40000], [100000, 200000, 200000]] , [0, 15, 15, 15, 15, 10, 15, 15, 15, 15, 15, 10, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12] , "Sample Structure1" , True , 0.5)