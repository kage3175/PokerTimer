import pygame
from pygame.locals import *
import time
import ctypes
from ClassObjs import TextObj
import tkinter as tk
from ClassObjs import *

FONTPATH = {'NGothicR' : './font/NanumGothic.ttf', 'NSquareR' : './font/NanumSquareR.ttf'}
LSTLEVELS = []
LSTBLINDS = []

PALEGRAY = (180,180,180)
BACKGROUND = (60, 55, 230)

TK_VAL = False

PRIZEINTERVAL = 40

TK_LST = []

def blitBackground(screen, rect, screenScale):
  screen.fill(BACKGROUND)
  pygame.draw.rect(screen, WHITE, rect, width=8)
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

def focus_next_entry(event):
  event.widget.tk_focusNext().focus()
  return 'break'

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
  global LSTLEVELS, LSTBLINDS, TK_LST
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
  doubleClickTimer = 0
  dt = 0
  
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

  imgSettings = pygame.image.load("./img/settings.png")
  imgSettings = pygame.transform.smoothscale(imgSettings,(round(100/screenScale),round(100/screenScale)))
  imgBar = pygame.image.load("./img/test.png")
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
  fontPrize = pygame.font.Font('./font/NanumGothicBold.ttf', round(27/screenScale))


  ### location, loc 모음집
  locMainTimer = (midpoint[0], round(483/screenScale))
  locCurrBlind = (midpoint[0], midpoint[1] + round(155/screenScale))
  locSettings = (screensize[0] - round(70 /screenScale), screensize[1] - round(70 / screenScale))
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
  textVol = fontVolume.render("Volume", True, WHITE)
  objVol = textVol.get_rect()
  objVol.center = (midpoint[0] - round(600/screenScale), midpoint[1])

  lstTextPrize = []
  '''for i in range(18):
    temp = TextObj(font = fontPrize, content="1st: APL 1T", relative="topleft", color=WHITE, position=(round(1590/screenScale), round((210+PRIZEINTERVAL*i)/screenScale)))
    lstTextPrize.append(temp)'''


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
  rectSettings = imgSettings.get_rect()
  rectSettings.center = locSettings
  rectBar = imgBar.get_rect()
  rectBar.center = (midpoint[0] + round(100/screenScale), midpoint[1])
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

  rectNext = pygame.Rect(0,0,round(500/screenScale),round(140/screenScale))
  rectNext.center = (midpoint[0] + round(300/screenScale), round(1030/screenScale))
  rectBack = pygame.Rect(0,0,round(500/screenScale),round(140/screenScale))
  rectBack.center = (midpoint[0] - round(300/screenScale), round(1030/screenScale))
  bigRect = pygame.Rect(0,0,round(1996/screenScale),round(1096/screenScale))
  bigRect.topleft = (round(26/screenScale), round(28/screenScale))
  

  pauseEvent = True
  pause_start = time.time()
  pause_time = 0
  flagback = "quit"
  flagSettings = False
  barMove = False
  clickedNum = -1
  dictClicked = {0:textPlayersLeftnum, 1:textAvgChipsnum, 2:textTotalChipsnum, 3: textEntrantsnum, 4:textStartingStacknum}
  dictNum = {0:numPlayer, 1:numAverage, 2:numChips, 3:numEntries, 4:numStarting}

  while running:
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
        blitText(surface, textMainTimer, textTitleTournament, textCurrLevel, textSB, textBB, textAnte, textSBnum, textBBnum, textAntenum, textNextSB, textNextBB, textNextAnte, textAvgChips, textTotalChips, textStartingStack, textTimetoBreak, textNextSBnum, textNextBBnum, textNextAntenum, textAvgChipsnum, textTotalChipsnum, textStartingStacknum, textTimetoBreaknum, textEntrants, textPlayersLeft, textEntrantsnum, textPlayersLeftnum)
        pygame.draw.rect(surface, RED, rectPauseline, width=round(5/screenScale))
        surface.blit(pauseBox, rectPause)
        surface.blit(textPause.getText(), textPause.getRect())
        pygame.draw.circle(surface, RED, shutCenter, shutRadius)
        pygame.draw.circle(surface, BLACK, shutCenter, shutRadius, width = round(2/screenScale))
        surface.blit(imgUpDown, rectUpDown1)
        surface.blit(imgUpDown, rectUpDown2)
        surface.blit(imgSettings, rectSettings)
        surface.blit(imgPlayButton, rectPlayButton)
        surface.blit(imgPlusOneButton, rectPlusOneButton)
        surface.blit(imgMinusOneButton, rectMinusOneButton)
        surface.blit(imgLevelUpButton, rectLevelUpButton)
        surface.blit(imgLevelDownButton, rectLevelDownButton)
        for text in lstTextPrize:
          surface.blit(text.getText(), text.getRect())
      else:
        surface.fill(BACKGROUND)
        pygame.draw.line(surface, WHITE, (midpoint[0] - round(400/screenScale), midpoint[1]), (midpoint[0] + round(600/screenScale), midpoint[1]), width=4)
        surface.blit(imgBar, rectBar)
        surface.blit(textVol, objVol)
        pygame.draw.rect(surface, PALEGRAY, rectNext)
        pygame.draw.rect(surface, DARKGRAY, rectNext, width = round(4/screenScale))
        surface.blit(textNext.getText(), textNext.getRect())
        pygame.draw.rect(surface, PALEGRAY, rectBack)
        pygame.draw.rect(surface, DARKGRAY, rectBack, width = round(4/screenScale))
        surface.blit(textBack.getText(), textBack.getRect())
      pygame.display.flip()
      dt = clock.tick(FPS) / 1000
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
            '''if event.key == K_RIGHT: ### 1분 뒤로
              min, sec, total, newLevel, min_break, sec_break = timeupdate(min, sec, total, 60, currLevel, soundLevelup,lstBreakIdx)
              if newLevel != currLevel:
                currLevel = newLevel
                if LSTLEVELS[currLevel]==0: ### End of blind
                  while running:
                    running = endAction(surface, textPause, fontPause, rectPauseline, pauseBox, rectPause, shutCenter, shutRadius, screenScale)
                try:
                  #updateTextAfterTimeSkip(LSTBLINDS, currLevel, textCurrLevel, textSBnum, textBBnum, textAntenum, textNextSBnum, textNextBBnum, textNextAntenum):
                  cntBreak = updateTextAfterTimeSkip(LSTBLINDS, currLevel, textCurrLevel, textSBnum, textBBnum, textAntenum, textNextSBnum, textNextBBnum, textNextAntenum, cntBreak)
                except:
                  print("No levels left2")
              strTimer = makeTimerString(min, sec, total)
              textMainTimer.changeContent(content = strTimer, font = fontMainTimer)
              strBreakTimer = makeTimerString(min_break,sec_break,total)
              textTimetoBreaknum.changeContent(font = textTimetoBreaknum.getFont(), content = strBreakTimer)'''
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
            if doubleClickTimer == 0:
              doubleClickTimer = 0.001
            elif doubleClickTimer < 0.5:
              '''if mouseInRect(rectPrizeBox, position):
                prizeInput(screenScale)
                lstTextPrize = []
                for i in range(len(TK_LST)):
                  temp = TextObj(font = fontPrize, content=TK_LST[i], relative="topleft", color=WHITE, position=(round(1590/screenScale), round((210+PRIZEINTERVAL*i)/screenScale)))
                  lstTextPrize.append(temp)'''
              doubleClickTimer = 0
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
              if mouseInRect(rectSettings, position):
                flagSettings = True
                rectBar.centerx = midpoint[0] - round(400/screenScale) + round(volume * 1000)
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

            else:
              pygame.mouse.get_rel()
              if mouseInRect(rectBar, position):
                barMove = True
              elif mouseInRect(rectNext, position):
                flagSettings = False
                barMove = False
                vol = (rectBar.centerx - midpoint[0] + 400/screenScale) / float(1000)
                outfile = open("./doc/settings", "w")
                outfile.write(str(vol))
                outfile.close()
              elif mouseInRect(rectBack, position):
                flagSettings = False
                barMove = False
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
          volume = (rectBar.centerx - midpoint[0] + 400/screenScale) / float(1000)
          soundLevelup.set_volume(volume)
          soundLevelup.play()
      if doubleClickTimer != 0:
        doubleClickTimer += dt
        if doubleClickTimer>= 0.5:
          doubleClickTimer = 0
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
            if doubleClickTimer == 0:
              doubleClickTimer = 0.001
            elif doubleClickTimer < 0.5:
              '''if mouseInRect(rectPrizeBox, position):
                prizeInput(screenScale)
                lstTextPrize = []
                for i in range(len(TK_LST)):
                  temp = TextObj(font = fontPrize, content=TK_LST[i], relative="topleft", color=WHITE, position=(round(1590/screenScale), round((210+PRIZEINTERVAL*i)/screenScale)))
                  lstTextPrize.append(temp)'''
              doubleClickTimer = 0
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
    if doubleClickTimer != 0:
      doubleClickTimer += dt
      if doubleClickTimer>= 0.5:
        #print('single clicked!')
        doubleClickTimer = 0    
            
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
    blitText(surface, textMainTimer, textTitleTournament, textCurrLevel, textSB, textBB, textAnte, textSBnum, textBBnum, textAntenum, textNextSB, textNextBB, textNextAnte, textAvgChips, textTotalChips, textStartingStack, textTimetoBreak, textNextSBnum, textNextBBnum, textNextAntenum, textAvgChipsnum, textTotalChipsnum, textStartingStacknum, textTimetoBreaknum, textEntrants, textPlayersLeft, textEntrantsnum, textPlayersLeftnum)
    pygame.draw.circle(surface, RED, shutCenter, shutRadius)
    pygame.draw.circle(surface, BLACK, shutCenter, shutRadius, width = round(2/screenScale))
    surface.blit(imgUpDown, rectUpDown1)
    surface.blit(imgUpDown, rectUpDown2)
    surface.blit(imgPauseButton, rectPauseButton)
    surface.blit(imgPlusOneButton, rectPlusOneButton)
    surface.blit(imgMinusOneButton, rectMinusOneButton)
    surface.blit(imgLevelUpButton, rectLevelUpButton)
    surface.blit(imgLevelDownButton, rectLevelDownButton)
    for text in lstTextPrize:
      surface.blit(text.getText(), text.getRect())
    #clock.tick(FPS)
    pygame.display.flip()
    dt = clock.tick(FPS) / 1000
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