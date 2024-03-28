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

TK_VAL = False

PRIZEINTERVAL = 40

TK_LST = []

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
  pass
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

  
def updateTextAfterTimeSkip(LSTBLINDS, currLevel, textCurrLevel, textBlind, textBBAnte, fontBlind, fontNextLevelnum, fontTitleTournament, textNextBBAntenum, textNextBlindnum, cntBreak):
  if LSTBLINDS[currLevel][0] == 0:   ## 현재 레벨이 브레이크인 경우
    cntBreak+=1
    textCurrLevel.changeColor(BRIGHTRED)
    textCurrLevel.changeContent(font = fontTitleTournament, content = "Break")
    textBlind.changeContent(font = fontBlind, content = "- / -")
    textBBAnte.changeContent(font = fontBlind, content = "-")
  else:
    textCurrLevel.changeColor(WHITE)
    textCurrLevel.changeContent(font = fontTitleTournament, content = 'Level '+str(currLevel-cntBreak))
    textBlind.changeContent(font = fontBlind, content = format(LSTBLINDS[currLevel][0], ",")+" / "+format(LSTBLINDS[currLevel][1], ","))
    if LSTBLINDS[currLevel][2] != 0:
      temp_str = format(LSTBLINDS[currLevel][2], ",")
    else:
      temp_str = "-"
    textBBAnte.changeContent(font = fontBlind, content = temp_str)
  if LSTBLINDS[currLevel+1][0] == 0:
    temp_str1 = "- / -"
    temp_str = "-"
  else:
    temp_str1 = format(LSTBLINDS[currLevel+1][0], ",") + " / " + format(LSTBLINDS[currLevel+1][1], ",")
    if LSTBLINDS[currLevel+1][2] != 0:
      temp_str = format(LSTBLINDS[currLevel+1][2], ",")
    else:
      temp_str = "-"
  textNextBlindnum.changeContent(font = fontNextLevelnum, content = temp_str1)
  textNextBBAntenum.changeContent(font = fontNextLevelnum, content = temp_str)
  return cntBreak

def endAction(surface, textPause, fontPause, rectPauseline, rectNextLevel, pauseBox, rectPause, shutCenter, shutRadius, screenScale):
  global TK_VAL
  textPause.changeContent(font = fontPause, content = "No more blinds")
  pygame.draw.rect(surface, RED, rectPauseline, width=round(5/screenScale))
  pygame.draw.rect(surface, PALEGRAY, rectNextLevel, width = round(3/screenScale))
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
  volume = vol
  print(lstBLINDS, lstLevels, title, isLoad, vol)
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

  imgBackground = pygame.image.load("./img/background.jpg")
  imgBackground = pygame.transform.scale(imgBackground, screensize)
  imgSettings = pygame.image.load("./img/settings.png")
  imgSettings = pygame.transform.scale(imgSettings,(round(100/screenScale),round(100/screenScale)))
  imgBar = pygame.image.load("./img/test.png")
  surface.blit(imgBackground,(0,0))

  #### font, font 모음집
  fontMainTimer = pygame.font.Font('./font/NanumSquareB.ttf', round(270 / screenScale))
  fontTitleTournament = pygame.font.Font('./font/NanumGothic.ttf', round(60 / screenScale))
  fontBlind = pygame.font.Font('./font/NanumGothicBold.ttf', round(55 / screenScale))
  fontSide = pygame.font.Font('./font/NanumGothicExtraBold.ttf', round(40/screenScale))
  fontSideNum = pygame.font.Font('./font/NanumGothic.ttf', round(40/screenScale))
  fontPause = pygame.font.Font('./font/NanumGothicBold.ttf', round(80/screenScale))
  fontNextLevel = pygame.font.Font("./font/NanumGothic.ttf", round(40/screenScale))
  fontNextLevelnum = pygame.font.Font('./font/NanumGothic.ttf', round(35/screenScale))
  fontButton = pygame.font.Font('./font/NanumGothicBold.ttf', round(80/screenScale))
  fontVolume = pygame.font.Font('./font/NanumGothic.ttf', round(80/screenScale))
  fontPrize = pygame.font.Font('./font/NanumGothicBold.ttf', round(27/screenScale))


  ### location, loc 모음집
  locMainTimer = (midpoint[0], midpoint[1] - round(200 / screenScale))
  locTitleTournament = (midpoint[0], midpoint[1] - round(440 /screenScale))
  locTextCurrLevel = (midpoint[0], midpoint[1] + round(20 /screenScale))
  locCurrBlind = (midpoint[0], midpoint[1] + round(155/screenScale))
  locNextLevel = (midpoint[0], midpoint[1] + round(285/screenScale))
  locSettings = (screensize[0] - round(70 /screenScale), screensize[1] - round(70 / screenScale))
  #locTextBlind = (midpoint[0] + round(150/screenScale), midpoint[1] + round(115/screenScale))
  #locTextTEXTBlind = (midpoint[0] - round(200/screenScale), midpoint[1] + round(115/screenScale))

  #region texts

  #### text 모음집
  textMainTimer = TextObj(font=fontMainTimer, content= strTimer, position=locMainTimer, relative="center", color=WHITE)
  textTitleTournament = TextObj(content=title, position = locTitleTournament, relative="center", color=PALEGRAY, font=fontTitleTournament)
  textCurrLevel = TextObj(font = fontTitleTournament, content='Level '+ str(currLevel), relative="center", color=WHITE, position=locTextCurrLevel)
  textBlind = TextObj(font = fontBlind, content=format(LSTBLINDS[currLevel][0], ",") + " / " + format(LSTBLINDS[currLevel][1], ","), relative="rcenter", position = (midpoint[1] + round(110/screenScale), midpoint[0] + round(430/screenScale)), color=WHITE)
  textTEXTBlind = TextObj(font = fontBlind, content="BLINDS", position=(midpoint[1] + round(110/screenScale), midpoint[0] - round(450/screenScale)), relative="lcenter", color=WHITE)
  textTEXTBBAnte = TextObj(font = fontBlind, content="BB Ante", position=(midpoint[1] + round(190/screenScale), midpoint[0] - round(450/screenScale)), relative="lcenter", color=WHITE)
  temp = "-" if LSTBLINDS[currLevel][2] == 0 else format(LSTBLINDS[currLevel][2], ",")
  textBBAnte = TextObj(font=fontBlind, content=temp, position=(midpoint[1] + round(190/screenScale), midpoint[0] + round(430/screenScale)), relative="rcenter", color=WHITE)
  textTEXTPlayer = TextObj(font=fontSide, content="Players", position=(round(80/screenScale),round(110/screenScale)), relative="topleft", color=WHITE)
  textPlayernum = TextObj(font = fontSideNum, content="0", position= (round(80/screenScale),round(165/screenScale)), relative="topleft", color=WHITE)
  textAverage = TextObj(font = fontSide, content="Average Chips", position=(round(80/screenScale),round(265/screenScale)), relative="topleft", color=WHITE)
  textAveragenum = TextObj(font = fontSideNum, content="0", position=(round(80/screenScale),round(320/screenScale)), relative="topleft", color=WHITE)
  textChipsinplay = TextObj(font = fontSide, content="Chips in Play", position=(round(80/screenScale),round(420/screenScale)), relative="topleft", color=WHITE)
  textChipsinplaynum = TextObj(font=fontSideNum, content="0", position=(round(80/screenScale),round(475/screenScale)), relative="topleft", color=WHITE)
  textEntries = TextObj(font = fontSide, content="Entries", position=(round(80/screenScale),round(575/screenScale)), relative="topleft", color=WHITE)
  textEntriesnum = TextObj(font = fontSideNum, content="0", color=WHITE, position=(round(80/screenScale),round(630/screenScale)), relative="topleft")
  textStartingstack = TextObj(font=fontSide, content="Starting Stacks", color=WHITE, relative="topleft", position=(round(80/screenScale),round(730/screenScale)))
  textStartingstacknum = TextObj(font = fontSideNum, color=WHITE, content="0", relative="topleft", position=(round(80/screenScale),round(785/screenScale)))
  textTimeBreak = TextObj(font=fontSide, content="Time to Break", color=WHITE, position= (round(80/screenScale),round(885/screenScale)), relative="topleft")
  textTimeBreaknum = TextObj(font=fontSideNum, content=strBreakTimer, color=WHITE, relative="topleft", position=(round(80/screenScale),round(940/screenScale)))
  textPause = TextObj(font = fontPause, content="Game Paused", color=BLACK, position=locMainTimer, relative="center")
  textNextLevel = TextObj(font = fontNextLevel, content="Next Level", color=PALEGRAY, position=locNextLevel, relative="center")
  textNextBlind = TextObj(font = fontNextLevelnum, content="Blinds", color=PALEGRAY, position=(midpoint[0]-round(240/screenScale),midpoint[1] + round(345/screenScale)), relative="topleft")
  textNextBBAnte = TextObj(font = fontNextLevelnum, content="BB Ante", color=PALEGRAY, position=(midpoint[0]-round(240/screenScale),midpoint[1] + round(400/screenScale)), relative="topleft")
  textNextBlindnum = TextObj(font = fontNextLevelnum, color=PALEGRAY, content=format(LSTBLINDS[currLevel+1][0], ",") + " / " + format(LSTBLINDS[currLevel+1][1], ","), position= (midpoint[0]+round(240/screenScale),midpoint[1] + round(345/screenScale)), relative="topright")
  temp = "-" if LSTBLINDS[currLevel+1][2] == 0 else format(LSTBLINDS[currLevel+1][2], ",")
  textNextBBAntenum = TextObj(font=fontNextLevelnum, content=temp, color=PALEGRAY, position=(midpoint[0]+round(240/screenScale),midpoint[1] + round(400/screenScale)), relative="topright")
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
  rectMainTimer = pygame.Rect(0,0,round(1050/screenScale),round(350/screenScale))
  rectMainTimer.center = locMainTimer
  rectMidPoint = pygame.Rect(0,0,20,20)
  rectMidPoint.center = midpoint
  rectCurrBlind = pygame.Rect(0,0,round(1000/screenScale), round(190/screenScale))
  rectCurrBlind.center = locCurrBlind
  rectPause = pygame.Rect(0,0,round(800/screenScale),round(100/screenScale))
  rectPause.center = locMainTimer
  rectPauseline = pygame.Rect(0,0,round(800/screenScale),round(100/screenScale))
  rectPauseline.center = locMainTimer
  rectNextLevel = pygame.Rect(0,0,round(600/screenScale),round(145/screenScale))
  rectNextLevel.center = (midpoint[0], midpoint[1] + round(390/screenScale))
  rectSettings = imgSettings.get_rect()
  rectSettings.center = locSettings
  rectBar = imgBar.get_rect()
  rectBar.center = (midpoint[0] + round(100/screenScale), midpoint[1])
  rectNext = pygame.Rect(0,0,round(500/screenScale),round(140/screenScale))
  rectNext.center = (midpoint[0] + round(300/screenScale), round(1030/screenScale))
  rectBack = pygame.Rect(0,0,round(500/screenScale),round(140/screenScale))
  rectBack.center = (midpoint[0] - round(300/screenScale), round(1030/screenScale))
  rectPrizeBox = pygame.Rect(0,0,round(420/screenScale), round(780/screenScale))
  rectPrizeBox.topleft = (round(1580/screenScale), round(200/screenScale))
  

  pauseEvent = True
  pause_start = time.time()
  pause_time = 0
  flagback = "quit"
  flagSettings = False
  barMove = False
  clickedNum = -1
  dictClicked = {0:textPlayernum, 1:textAveragenum, 2:textChipsinplaynum, 3: textEntriesnum, 4:textStartingstacknum}
  dictNum = {0:numPlayer, 1:numAverage, 2:numChips, 3:numEntries, 4:numStarting}

  while running:
    if TK_VAL:
      running = False
      continue
    if pauseEvent:
      flag = True
      surface.blit(imgBackground,(0,0))
      if not flagSettings:
        if clickedNum != -1:
          try:
            pygame.draw.rect(surface, PALEGRAY, dictClicked[clickedNum].getRect())
          except:
            print("clickedNum Error")
        blitText(surface, textMainTimer, textTitleTournament, textCurrLevel, textBlind, textTEXTBlind, textTEXTBBAnte, textBBAnte, textTEXTPlayer, textPlayernum, textAverage, textAveragenum, textChipsinplay, textChipsinplaynum, textEntries, textEntriesnum, textStartingstack, textStartingstacknum, textTimeBreak, textTimeBreaknum, textNextLevel, textNextBlind, textNextBBAnte, textNextBlindnum, textNextBBAntenum)
        pygame.draw.rect(surface, WHITE, rectMainTimer, width=round(3/screenScale))
        pygame.draw.rect(surface, WHITE, rectCurrBlind, width=round(3/screenScale))
        pygame.draw.rect(surface, RED, rectPauseline, width=round(5/screenScale))
        pygame.draw.rect(surface, PALEGRAY, rectNextLevel, width = round(3/screenScale))
        surface.blit(pauseBox, rectPause)
        surface.blit(textPause.getText(), textPause.getRect())
        pygame.draw.circle(surface, RED, shutCenter, shutRadius)
        pygame.draw.circle(surface, BLACK, shutCenter, shutRadius, width = round(2/screenScale))
        surface.blit(imgSettings, rectSettings)
        pygame.draw.rect(surface, DARKGRAY, rectPrizeBox, width=round(3/screenScale))
        for text in lstTextPrize:
          surface.blit(text.getText(), text.getRect())
      else:
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
      dt = clock.tick(30) / 1000
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
              textBlind.changeContent(font = fontBlind, content = format(LSTBLINDS[currLevel][0], ",")+" / "+format(LSTBLINDS[currLevel][1], ","))
              if LSTBLINDS[currLevel][2] != 0:
                textBBAnte.changeContent(font = fontBlind, content = format(LSTBLINDS[currLevel][2], ","))
            if event.key in K_NUM or event.key == K_BACKSPACE:
              if clickedNum != -1:
                temp_input = (temp_input*10 + processAscii(event.key)) if (event.key in K_NUM) else (temp_input//10)
                dictClicked[clickedNum].changeColor(BLACK)
                dictClicked[clickedNum].changeContent(font=fontSideNum, content= format(temp_input, ","))
            if pygame.key.name(event.key) == "return" or pygame.key.name(event.key) == "enter":
              if clickedNum != -1: ### dictClicked = {0:textPlayernum, 1:textAveragenum, 2:textChipsinplaynum, 3: textEntriesnum, 4:textStartingstacknum}
                dictNum[clickedNum] = temp_input
                dictClicked[clickedNum].changeColor(WHITE)
                dictClicked[clickedNum].changeContent(font = fontSideNum, content = format(dictNum[clickedNum], ","))
                if (clickedNum==0 or clickedNum ==2) and dictNum[0]>0:
                  dictNum[1] = dictNum[2] // dictNum[0]
                  textAveragenum.changeColor(WHITE)
                  textAveragenum.changeContent(font = fontSideNum, content = format(dictNum[1], ","))                  
              temp_input = 0
              clickedNum=-1
            if event.key == K_RIGHT: ### 1분 뒤로
              min, sec, total, newLevel, min_break, sec_break = timeupdate(min, sec, total, 60, currLevel, soundLevelup,lstBreakIdx)
              if newLevel != currLevel:
                currLevel = newLevel
                if LSTLEVELS[currLevel]==0: ### End of blind
                  while running:
                    running = endAction(surface, textPause, fontPause, rectPauseline, rectNextLevel, pauseBox, rectPause, shutCenter, shutRadius, screenScale)
                try:
                  cntBreak = updateTextAfterTimeSkip(LSTBLINDS, currLevel, textCurrLevel, textBlind, textBBAnte, fontBlind, fontNextLevelnum, fontTitleTournament, textNextBBAntenum, textNextBlindnum, cntBreak)
                except:
                  print("No levels left2")
              strTimer = makeTimerString(min, sec, total)
              textMainTimer.changeContent(content = strTimer, font = fontMainTimer)
              strBreakTimer = makeTimerString(min_break,sec_break,total)
              textTimeBreaknum.changeContent(font = fontSideNum, content = strBreakTimer)
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
              if mouseInRect(rectPrizeBox, position):
                prizeInput(screenScale)
                lstTextPrize = []
                for i in range(len(TK_LST)):
                  temp = TextObj(font = fontPrize, content=TK_LST[i], relative="topleft", color=WHITE, position=(round(1590/screenScale), round((210+PRIZEINTERVAL*i)/screenScale)))
                  lstTextPrize.append(temp)
              doubleClickTimer = 0
            if not flagSettings:
              temp_input = 0
              if clickedNum!=-1:
                dictClicked[clickedNum].changeColor(WHITE)
                dictClicked[clickedNum].changeContent(font = fontSideNum, content = format(dictNum[clickedNum], ","))
                clickedNum=-1
              elif mouseInRect(textPlayernum.getRect(), position):
                clickedNum=0
              elif mouseInRect(textAveragenum.getRect(), position):
                clickedNum=1
              elif mouseInRect(textChipsinplaynum.getRect(), position):
                clickedNum=2
              elif mouseInRect(textEntriesnum.getRect(), position):
                clickedNum=3
              elif mouseInRect(textStartingstacknum.getRect(), position):
                clickedNum=4
              elif (((position[0] - shutCenter[0]) ** 2 + (position[1] - shutCenter[1]) ** 2) ** 0.5 <= shutRadius):
                confirmQuit()
              if mouseInRect(rectSettings, position):
                flagSettings = True
                rectBar.centerx = midpoint[0] - round(400/screenScale) + round(volume * 1000)
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
            dictClicked[clickedNum].changeContent(font = fontSideNum, content = format(temp_input, ","))
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
            dictClicked[clickedNum].changeContent(font = fontSideNum, content = format(dictNum[clickedNum], ","))
            if (clickedNum==0 or clickedNum==2) and dictNum[0] > 0:
              dictNum[1] = dictNum[2] // dictNum[0]
              textAveragenum.changeColor(WHITE)
              textAveragenum.changeContent(font = fontSideNum, content = format(dictNum[1], ","))
          temp_input = 0
          clickedNum = -1
        if event.key == K_RIGHT or event.key == K_LEFT: ### 1분 뒤로
          factor = 60 if event.key == K_RIGHT else -60
          min, sec, total, newLevel, min_break, sec_break = timeupdate(min, sec, total, factor, currLevel, soundLevelup,lstBreakIdx)
          if newLevel != currLevel:
            currLevel = newLevel
            if LSTLEVELS[currLevel]==0: ### End of blind
              while running:
                running = endAction(surface, textPause, fontPause, rectPauseline, rectNextLevel, pauseBox, rectPause, shutCenter, shutRadius, screenScale)
            try:
              cntBreak = updateTextAfterTimeSkip(LSTBLINDS, currLevel, textCurrLevel, textBlind, textBBAnte, fontBlind, fontNextLevelnum, fontTitleTournament, textNextBBAntenum, textNextBlindnum, cntBreak)

            except:
              print("No levels left")
          strTimer = makeTimerString(min, sec, total)
          textMainTimer.changeContent(content = strTimer, font = fontMainTimer)
          strBreakTimer = makeTimerString(min_break,sec_break,total)
          textTimeBreaknum.changeContent(font = fontSideNum, content = strBreakTimer)
        
      elif event.type == MOUSEBUTTONDOWN:
          if event.button == 1:
            position = pygame.mouse.get_pos()
            temp_input = 0
            if doubleClickTimer == 0:
              doubleClickTimer = 0.001
            elif doubleClickTimer < 0.5:
              if mouseInRect(rectPrizeBox, position):
                prizeInput(screenScale)
                lstTextPrize = []
                for i in range(len(TK_LST)):
                  temp = TextObj(font = fontPrize, content=TK_LST[i], relative="topleft", color=WHITE, position=(round(1590/screenScale), round((210+PRIZEINTERVAL*i)/screenScale)))
                  lstTextPrize.append(temp)
              doubleClickTimer = 0
            if clickedNum!=-1:
              dictClicked[clickedNum].changeColor(WHITE)
              dictClicked[clickedNum].changeContent(font = fontSideNum, content = format(dictNum[clickedNum], ","))
              clickedNum=-1
            elif mouseInRect(textPlayernum.getRect(), position):
              clickedNum=0
            elif mouseInRect(textAveragenum.getRect(), position):
              clickedNum=1
            elif mouseInRect(textChipsinplaynum.getRect(), position):
              clickedNum=2
            elif mouseInRect(textEntriesnum.getRect(), position):
              clickedNum=3
            elif mouseInRect(textStartingstacknum.getRect(), position):
              clickedNum=4
            if (((position[0] - shutCenter[0]) ** 2 + (position[1] - shutCenter[1]) ** 2) ** 0.5 <= shutRadius):
              confirmQuit()
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
            textPause.changeContent(font = fontPause, content = "No more blinds")
            pygame.draw.rect(surface, RED, rectPauseline, width=round(5/screenScale))
            pygame.draw.rect(surface, PALEGRAY, rectNextLevel, width = round(5/screenScale))
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
            time.sleep(0.1)
        try:
          cntBreak = updateTextAfterTimeSkip(LSTBLINDS, currLevel, textCurrLevel, textBlind, textBBAnte, fontBlind, fontNextLevelnum, fontTitleTournament, textNextBBAntenum, textNextBlindnum, cntBreak)
        except:
          print("No levels left")
      strTimer = makeTimerString(min, sec, total)
      textMainTimer.changeContent(content = strTimer, font = fontMainTimer)
      strBreakTimer = makeTimerString(min_break,sec_break,total)
      textTimeBreaknum.changeContent(font = fontSideNum, content = strBreakTimer)
    surface.blit(imgBackground,(0,0))
    if clickedNum != -1:
      pygame.draw.rect(surface, PALEGRAY, dictClicked[clickedNum].getRect())
    blitText(surface, textMainTimer, textTitleTournament,textCurrLevel,textBlind,textTEXTBlind,textTEXTBBAnte,textBBAnte,textTEXTPlayer,textPlayernum,textAverage,textAveragenum,textChipsinplay,textChipsinplaynum,textEntries,textEntriesnum,textStartingstack,textTimeBreak,textTimeBreaknum,textStartingstacknum,textNextLevel,textNextBlind,textNextBBAnte,textNextBBAntenum,textNextBlindnum)
    pygame.draw.rect(surface, WHITE, rectMainTimer, width=round(3/screenScale))
    pygame.draw.rect(surface, WHITE, rectCurrBlind, width=round(3/screenScale))
    pygame.draw.rect(surface, PALEGRAY, rectNextLevel, width = round(3/screenScale))
    pygame.draw.circle(surface, RED, shutCenter, shutRadius)
    pygame.draw.circle(surface, BLACK, shutCenter, shutRadius, width = round(2/screenScale))
    pygame.draw.rect(surface, DARKGRAY, rectPrizeBox, width=round(3/screenScale))
    for text in lstTextPrize:
      surface.blit(text.getText(), text.getRect())
    pygame.display.flip()
    dt = clock.tick(30) / 1000
  soundLevelup.stop()
  pygame.quit()
  if flagback == "load":
    return 1
  elif flagback == "save":
    return 2
  else:
    return 0
#### End of main function
