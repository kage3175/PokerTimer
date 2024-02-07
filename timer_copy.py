import pygame
from pygame.locals import *
import time
import random
import ctypes
import os
from TextObj import TextObj

FONTPATH = {'NGothicR' : './font/NanumGothic.ttf', 'NSquareR' : './font/NanumSquareR.ttf'}
TESTMIN, TESTSEC, TESTTOTAL = 10,0,600
LSTLEVELS = []
LSTBLINDS = []

BLACK = (0,0,0)
WHITE = (240,240,240)
RED = (210,0,0)
BRIGHTRED = (255,10,10)
BACKGROUND = (20,20,90)
PALEGRAY = (180,180,180)
YELLOW = (220,220,90)
K_NUM = [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]


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
  soundlvlup.play()
  level = currLevel+updown
  if updown > 0:
    min, sec, tot = minute + LSTLEVELS[level], second, total + LSTLEVELS[level] * 60
    min -= 1
    sec = second + 60 - amount
    tot -= amount
  else:
    min, sec = minute + LSTLEVELS[level] + updown, second
    tot = min*60+sec
  return min, sec,tot,level
#### End of levelupdate function

def blitText(surface, *textobjs):
  for text in textobjs:
    surface.blit(text.getText(), text.getRect())
  pass
#### End of blitText function

def main(lstBLINDS, lstLevels,title):
  global LSTLEVELS, LSTBLINDS
  LSTLEVELS = lstLevels
  LSTLEVELS.append(100)

  LSTBLINDS = lstBLINDS
  LSTBLINDS.append((0,0,0))

  lstBreakIdx = [0 for _ in range(len(LSTLEVELS))]
  running = True
  pygame.init()
  
  user32 = ctypes.windll.user32
  screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
  midpoint = screensize[0] / 2, screensize[1] / 2 # 화면 중앙점
  screenScale = 1152/screensize[1]
  surface = pygame.display.set_mode(screensize, FULLSCREEN)
  soundLevelup = pygame.mixer.Sound("./sound/levelup.mp3")
  pauseBox = pygame.Surface((round(800/screenScale),round(100/screenScale)))
  pauseBox.set_alpha(128)
  pauseBox.fill(YELLOW)

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
  #print(lstBreakIdx)

  imgBackground = pygame.image.load("./img/background.jpg")
  imgBackground = pygame.transform.scale(imgBackground, screensize)
  surface.blit(imgBackground,(0,0))

  #### font, font 모음집
  fontMainTimer = pygame.font.Font('./font/NanumSquareB.ttf', round(270 / screenScale))
  fontTitleTournament = pygame.font.Font('./font/NanumGothic.ttf', round(60 / screenScale))
  fontBlind = pygame.font.Font('./font/NanumGothic.ttf', round(45 / screenScale))
  fontSide = pygame.font.Font('./font/NanumGothicExtraBold.ttf', round(40/screenScale))
  fontSideNum = pygame.font.Font('./font/NanumGothic.ttf', round(40/screenScale))
  fontPause = pygame.font.Font('./font/NanumGothicBold.ttf', round(80/screenScale))
  fontNextLevel = pygame.font.Font("./font/NanumGothic.ttf", round(40/screenScale))
  fontNextLevelnum = pygame.font.Font('./font/NanumGothic.ttf', round(35/screenScale))


  ### location, loc 모음집
  locMainTimer = (midpoint[0], midpoint[1] - round(200 / screenScale))
  locTitleTournament = (midpoint[0], midpoint[1] - round(440 /screenScale))
  locTextCurrLevel = (midpoint[0], midpoint[1] + round(25 /screenScale))
  locCurrBlind = (midpoint[0], midpoint[1] + round(150/screenScale))
  locNextLevel = (midpoint[0], midpoint[1] + round(280/screenScale))
  #locTextBlind = (midpoint[0] + round(150/screenScale), midpoint[1] + round(115/screenScale))
  #locTextTEXTBlind = (midpoint[0] - round(200/screenScale), midpoint[1] + round(115/screenScale))

  #region texts

  #### text 모음집
  textMainTimer = TextObj(font=fontMainTimer, content= strTimer, position=locMainTimer, relative="center", color=WHITE)
  textTitleTournament = TextObj(content=title, position = locTitleTournament, relative="center", color=PALEGRAY, font=fontTitleTournament)
  textCurrLevel = TextObj(font = fontTitleTournament, content='Level '+ str(currLevel), relative="center", color=WHITE, position=locTextCurrLevel)
  textBlind = TextObj(font = fontBlind, content=format(LSTBLINDS[currLevel][0], ",") + " / " + format(LSTBLINDS[currLevel][1], ","), relative="rcenter", position = (midpoint[1] + round(115/screenScale), midpoint[0] + round(350/screenScale)), color=WHITE)
  textTEXTBlind = TextObj(font = fontBlind, content="BLINDS", position=(midpoint[1] + round(115/screenScale), midpoint[0] - round(300/screenScale)), relative="lcenter", color=WHITE)
  textTEXTBBAnte = TextObj(font = fontBlind, content="BB Ante", position=(midpoint[1] + round(175/screenScale), midpoint[0] - round(300/screenScale)), relative="lcenter", color=WHITE)
  temp = "-" if LSTBLINDS[currLevel][2] == 0 else format(LSTBLINDS[currLevel][2], ",")
  textBBAnte = TextObj(font=fontBlind, content=temp, position=(midpoint[1] + round(175/screenScale), midpoint[0] + round(350/screenScale)), relative="rcenter", color=WHITE)
  textTEXTPlayer = TextObj(font=fontSide, content="Players", position=(round(115/screenScale),round(110/screenScale)), relative="topleft", color=WHITE)
  textPlayernum = TextObj(font = fontSideNum, content="0", position= (round(115/screenScale),round(165/screenScale)), relative="topleft", color=WHITE)
  textAverage = TextObj(font = fontSide, content="Average Chips", position=(round(115/screenScale),round(265/screenScale)), relative="topleft", color=WHITE)
  textAveragenum = TextObj(font = fontSideNum, content="0", position=(round(115/screenScale),round(320/screenScale)), relative="topleft", color=WHITE)
  textChipsinplay = TextObj(font = fontSide, content="Chips in Play", position=(round(115/screenScale),round(420/screenScale)), relative="topleft", color=WHITE)
  textChipsinplaynum = TextObj(font=fontSideNum, content="0", position=(round(115/screenScale),round(475/screenScale)), relative="topleft", color=WHITE)
  textEntries = TextObj(font = fontSide, content="Entries", position=(round(115/screenScale),round(575/screenScale)), relative="topleft", color=WHITE)
  textEntriesnum = TextObj(font = fontSideNum, content="0", color=WHITE, position=(round(115/screenScale),round(630/screenScale)), relative="topleft")
  textStartingstack = TextObj(font=fontSide, content="Starting Stacks", color=WHITE, relative="topleft", position=(round(115/screenScale),round(730/screenScale)))
  textStartingstacknum = TextObj(font = fontSideNum, color=WHITE, content="0", relative="topleft", position=(round(115/screenScale),round(785/screenScale)))
  textTimeBreak = TextObj(font=fontSide, content="Time to Break", color=WHITE, position= (round(115/screenScale),round(885/screenScale)), relative="topleft")
  textTimeBreaknum = TextObj(font=fontSideNum, content=strBreakTimer, color=WHITE, relative="topleft", position=(round(115/screenScale),round(940/screenScale)))
  textPause = TextObj(font = fontPause, content="Game Paused", color=BLACK, position=locMainTimer, relative="center")
  textNextLevel = TextObj(font = fontNextLevel, content="Next Level", color=PALEGRAY, position=locNextLevel, relative="center")
  textNextBlind = TextObj(font = fontNextLevelnum, content="Blinds", color=PALEGRAY, position=(midpoint[0]-round(240/screenScale),midpoint[1] + round(340/screenScale)), relative="topleft")
  textNextBBAnte = TextObj(font = fontNextLevelnum, content="BB Ante", color=PALEGRAY, position=(midpoint[0]-round(240/screenScale),midpoint[1] + round(395/screenScale)), relative="topleft")
  textNextBlindnum = TextObj(font = fontNextLevelnum, color=PALEGRAY, content=format(LSTBLINDS[currLevel+1][0], ",") + " / " + format(LSTBLINDS[currLevel+1][1], ","), position= (midpoint[0]+round(240/screenScale),midpoint[1] + round(340/screenScale)), relative="topright")
  temp = "-" if LSTBLINDS[currLevel+1][2] == 0 else format(LSTBLINDS[currLevel+1][2], ",")
  textNextBBAntenum = TextObj(font=fontNextLevelnum, content=temp, color=PALEGRAY, position=(midpoint[0]+round(240/screenScale),midpoint[1] + round(395/screenScale)), relative="topright")

  #endregion

  flagPlayer, flagAverage, flagChips, flagEntries, flagStarting = False, False,False,False,False
  numPlayer, numChips, numAverage, numEntries, numStarting = 0,0,0,0,0
  temp_input = 0

  #### rect 모음집
  rectMainTimer = pygame.Rect(0,0,round(1050/screenScale),round(350/screenScale))
  rectMainTimer.center = locMainTimer
  rectMidPoint = pygame.Rect(0,0,20,20)
  rectMidPoint.center = midpoint
  rectCurrBlind = pygame.Rect(0,0,round(800/screenScale), round(165/screenScale))
  rectCurrBlind.center = locCurrBlind
  rectPause = pygame.Rect(0,0,round(800/screenScale),round(100/screenScale))
  rectPause.center = locMainTimer
  rectPauseline = pygame.Rect(0,0,round(800/screenScale),round(100/screenScale))
  rectPauseline.center = locMainTimer
  rectNextLevel = pygame.Rect(0,0,round(600/screenScale),round(140/screenScale))
  rectNextLevel.center = (midpoint[0], midpoint[1] + round(390/screenScale))

  pauseEvent = True
  pause_start = time.time()
  pause_time = 0

  while running:
    if pauseEvent:
      flag = True
      surface.blit(imgBackground,(0,0))
      if flagPlayer:
        pygame.draw.rect(surface, PALEGRAY, textPlayernum.getRect())
      if flagAverage:
        pygame.draw.rect(surface, PALEGRAY, textAveragenum.getRect())
      if flagChips:
        pygame.draw.rect(surface, PALEGRAY, textChipsinplaynum.getRect())
      if flagEntries:
        pygame.draw.rect(surface, PALEGRAY, textEntriesnum.getRect())
      if flagStarting:
        pygame.draw.rect(surface, PALEGRAY, textStartingstacknum.getRect())
      blitText(surface, textMainTimer, textTitleTournament, textCurrLevel, textBlind, textTEXTBlind, textTEXTBBAnte, textBBAnte, textTEXTPlayer, textPlayernum, textAverage, textAveragenum, textChipsinplay, textChipsinplaynum, textEntries, textEntriesnum, textStartingstack, textStartingstacknum, textTimeBreak, textTimeBreaknum, textNextLevel, textNextBlind, textNextBBAnte, textNextBlindnum, textNextBBAntenum)
      pygame.draw.rect(surface, WHITE, rectMainTimer, width=3)
      pygame.draw.rect(surface, WHITE, rectCurrBlind, width=3)
      pygame.draw.rect(surface, RED, rectPauseline, width=5)
      pygame.draw.rect(surface, PALEGRAY, rectNextLevel, width = 3)
      surface.blit(pauseBox, rectPause)
      surface.blit(textPause.getText(), textPause.getRect())
      pygame.display.flip()
      pause_time_to_add = pause_start - time.time()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        elif event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            surface = pygame.display.set_mode((500,500))
          if event.key == K_SPACE:
            soundLevelup.play()
            pauseEvent = False
            flag = False
            textBlind.changeContent(font = fontBlind, content = format(LSTBLINDS[currLevel][0], ",")+" / "+format(LSTBLINDS[currLevel][1], ","))
            if LSTBLINDS[currLevel][2] != 0:
              textBBAnte.changeContent(font = fontBlind, content = format(LSTBLINDS[currLevel][2], ","))
          if event.key == ord('q'):
            running=False
          if event.key in K_NUM or event.key == K_BACKSPACE:
            if flagPlayer or flagEntries or flagAverage or flagChips or flagStarting:
              temp_input = (temp_input*10 + int(event.key) - 48) if (event.key in K_NUM) else (temp_input//10)
              if flagPlayer:
                textPlayernum.changeColor(BLACK)
                textPlayernum.changeContent(font = fontSideNum, content = format(temp_input, ","))
              elif flagAverage:
                textAveragenum.changeColor(BLACK)
                textAveragenum.changeContent(font = fontSideNum, content = format(temp_input, ","))
              elif flagChips:
                textChipsinplaynum.changeColor(BLACK)
                textChipsinplaynum.changeContent(font = fontSideNum, content = format(temp_input, ","))
              elif flagEntries:
                textEntriesnum.changeColor(BLACK)
                textEntriesnum.changeContent(font = fontSideNum, content = format(temp_input, ","))
              elif flagStarting:
                textStartingstacknum.changeColor(BLACK)
                textStartingstacknum.changeContent(font = fontSideNum, content = format(temp_input, ","))
          if event.key == K_RETURN:
            if flagPlayer:
              numPlayer = temp_input
              textPlayernum.changeColor(WHITE)
              textPlayernum.changeContent(font = fontSideNum, content = format(numPlayer, ","))
              numAverage = numChips // numPlayer
              textAveragenum.changeColor(WHITE)
              textAveragenum.changeContent(font = fontSideNum, content = format(numAverage, ","))
            elif flagAverage:
              numAverage = temp_input
              textAveragenum.changeColor(WHITE)
              textAveragenum.changeContent(font = fontSideNum, content = format(numAverage, ","))
            elif flagChips:
              numChips = temp_input
              textChipsinplaynum.changeColor(WHITE)
              textChipsinplaynum.changeContent(font = fontSideNum, content = format(numChips, ","))
              if numPlayer > 0:
                numAverage = numChips // numPlayer
                textAveragenum.changeColor(WHITE)
                textAveragenum.changeContent(font = fontSideNum, content = format(numAverage, ","))
            elif flagEntries:
              numEntries = temp_input
              textEntriesnum.changeColor(WHITE)
              textEntriesnum.changeContent(font = fontSideNum, content = format(numEntries, ","))
            elif flagStarting:
              numStarting = temp_input
              textStartingstacknum.changeColor(WHITE)
              textStartingstacknum.changeContent(font = fontSideNum, content = format(numStarting, ","))
            temp_input = 0
            flagPlayer, flagAverage, flagChips, flagEntries, flagStarting = False, False,False,False,False
          if event.key == K_RIGHT: ### 1분 뒤로
            #print(currLevel)
            min, sec, total, newLevel, min_break, sec_break = timeupdate(min, sec, total, 60, currLevel, soundLevelup,lstBreakIdx)
            if newLevel != currLevel:
              currLevel = newLevel
              if LSTLEVELS[currLevel]==0: ### End of blind
                while running:
                  textPause.changeContent(font = fontPause, content = "No more blinds")
                  pygame.draw.rect(surface, RED, rectPauseline, width=5)
                  pygame.draw.rect(surface, PALEGRAY, rectNextLevel, width = 3)
                  surface.blit(pauseBox, rectPause)
                  surface.blit(textPause.getText(), textPause.getRect())
                  pygame.display.flip()
                  for event in pygame.event.get():
                    if event.type == KEYDOWN:
                      if event.key == ord('q'):
                        running = False
                  time.sleep(0.1)
                  
              try:
                if LSTBLINDS[currLevel][0] == 0:
                  cntBreak+=1
                  textCurrLevel.changeColor(BRIGHTRED)
                  textCurrLevel.changeContent(font = fontTitleTournament, content = "Break")
                  textBlind.changeContent(font = fontBlind, content="- / -")
                  textBBAnte.changeContent(font = fontBlind, content = "-")
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
                else:
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
              except:
                print("No levels left2")
            strTimer = makeTimerString(min, sec, total)
            textMainTimer.changeContent(content = strTimer, font = fontMainTimer)
            strBreakTimer = makeTimerString(min_break,sec_break,total)
            textTimeBreaknum.changeContent(font = fontSideNum, content = strBreakTimer)
        elif event.type == MOUSEBUTTONDOWN:
          position = pygame.mouse.get_pos()
          temp_input = 0
          if flagPlayer:
            textPlayernum.changeColor(BLACK)
            textPlayernum.changeContent(font = fontSideNum, content = format(numPlayer, ","))
            flagPlayer = False
          if flagAverage:
            textAveragenum.changeColor(BLACK)
            textAveragenum.changeContent(font = fontSideNum, content = format(numAverage, ","))
            flagAverage = False
          if flagChips:
            textChipsinplaynum.changeColor(BLACK)
            textChipsinplaynum.changeContent(font = fontSideNum, content = format(numChips, ","))
            flagChips = False
          if flagEntries:
            textEntriesnum.changeColor(BLACK)
            textEntriesnum.changeConten(font = fontSideNum, content = format(numEntries, ","))
            flagEntries = False
          if flagStarting:
            textStartingstacknum.changeColor(BLACK)
            textStartingstacknum.changeContent(font = fontSideNum, content = format(numStarting, ","))
            flagStarting = False
          elif ((position[0] > textPlayernum.getRect().left and position[0] < textPlayernum.getRect().right) and (position[1] > textPlayernum.getRect().top and position[1] < textPlayernum.getRect().bottom)):
            flagPlayer = True
          elif ((position[0] > textAveragenum.getRect().left and position[0] < textAveragenum.getRect().right) and (position[1] > textAveragenum.getRect().top and position[1] < textAveragenum.getRect().bottom)):
            flagAverage = True
          elif ((position[0] > textChipsinplaynum.getRect().left and position[0] < textChipsinplaynum.getRect().right) and (position[1] > textChipsinplaynum.getRect().top and position[1] < textChipsinplaynum.getRect().bottom)):
            flagChips = True
          elif ((position[0] > textEntriesnum.getRect().left and position[0] < textEntriesnum.getRect().right) and (position[1] > textEntriesnum.getRect().top and position[1] < textEntriesnum.getRect().bottom)):
            flagEntries = True
          elif ((position[0] > textStartingstacknum.getRect().left and position[0] < textStartingstacknum.getRect().right) and (position[1] > textStartingstacknum.getRect().top and position[1] < textStartingstacknum.getRect().bottom)):
            flagStarting = True
      time.sleep(0.05)
      #pause_time+=pause_start-time.time()
      #print(pause_time)
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
          running = False
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
          if flagPlayer or flagEntries or flagAverage or flagChips or flagStarting:
            temp_input = (temp_input*10 + int(event.key) - 48) if (event.key in K_NUM) else (temp_input//10)
            if flagPlayer:
              textPlayernum.changeColor(BLACK)
              textPlayernum.changeContent(font = fontSideNum, content = format(temp_input, ","))
            elif flagAverage:
              textAveragenum.changeColor(BLACK)
              textAveragenum.changeContent(font = fontSideNum, content = format(temp_input, ","))
            elif flagChips:
              textChipsinplaynum.changeColor(BLACK)
              textChipsinplaynum.changeContent(font = fontSideNum, content = format(temp_input, ","))
            elif flagEntries:
              textEntriesnum.changeColor(BLACK)
              textEntriesnum.changeContent(font = fontSideNum, content = format(temp_input, ","))
            elif flagStarting:
              textStartingstacknum.changeColor(BLACK)
              textStartingstacknum.changeContent(font = fontSideNum, content = format(temp_input, ","))
        if event.key == K_RETURN:
          if flagPlayer:
            numPlayer = temp_input
            textPlayernum.changeColor(WHITE)
            textPlayernum.changeContent(font = fontSideNum, content = format(numPlayer, ","))
            numAverage = numChips // numPlayer
            textAveragenum.changeColor(WHITE)
            textAveragenum.changeContent(font = fontSideNum, content = format(numAverage, ","))
          elif flagAverage:
            numAverage = temp_input
            textAveragenum.changeColor(WHITE)
            textAveragenum.changeContent(font = fontSideNum, content = format(numAverage, ","))
          elif flagChips:
            numChips = temp_input
            textChipsinplaynum.changeColor(WHITE)
            textChipsinplaynum.changeContent(font = fontSideNum, content = format(numChips, ","))
            if numPlayer > 0:
              numAverage = numChips // numPlayer
              textAveragenum.changeColor(WHITE)
              textAveragenum.changeContent(font = fontSideNum, content = format(numAverage, ","))
          elif flagEntries:
            numEntries = temp_input
            textEntriesnum.changeColor(WHITE)
            textEntriesnum.changeContent(font = fontSideNum, content = format(numEntries, ","))
          elif flagStarting:
            numStarting = temp_input
            textStartingstacknum.changeColor(WHITE)
            textStartingstacknum.changeContent(font = fontSideNum, content = format(numStarting, ","))
          temp_input = 0
          flagPlayer, flagAverage, flagChips, flagEntries, flagStarting = False, False,False,False,False
        if event.key == K_RIGHT: ### 1분 뒤로
          #print(currLevel)
          min, sec, total, newLevel, min_break, sec_break = timeupdate(min, sec, total, 60, currLevel, soundLevelup,lstBreakIdx)
          if newLevel != currLevel:
            currLevel = newLevel
            if LSTLEVELS[currLevel]==0: ### End of blind
                while running:
                  textPause.changeContent(font = fontPause, content = "No more blinds")
                  pygame.draw.rect(surface, RED, rectPauseline, width=5)
                  pygame.draw.rect(surface, PALEGRAY, rectNextLevel, width = 3)
                  surface.blit(pauseBox, rectPause)
                  surface.blit(textPause.getText(), textPause.getRect())
                  pygame.display.flip()
                  for event in pygame.event.get():
                    if event.type == KEYDOWN:
                      if event.key == ord('q'):
                        currLevel-=1
                        running = False
                  time.sleep(0.1)
            try:
              if LSTBLINDS[currLevel][0] == 0:
                cntBreak+=1
                textCurrLevel.changeColor(BRIGHTRED)
                textCurrLevel.changeContent(font = fontTitleTournament, content = "Break")
                textBlind.changeContent(font = fontBlind, content = "- / -")
                textBBAnte.changeContent(font = fontBlind, content = "-")
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
              else:
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
            except:
              print("No levels left")
          strTimer = makeTimerString(min, sec, total)
          textMainTimer.changeContent(content = strTimer, font = fontMainTimer)
          strBreakTimer = makeTimerString(min_break,sec_break,total)
          textTimeBreaknum.changeContent(font = fontSideNum, content = strBreakTimer)
        if event.key == K_LEFT: # 1분 당기기
          pass
      elif event.type == MOUSEBUTTONDOWN:
          position = pygame.mouse.get_pos()
          temp_input = 0
          if flagPlayer:
            textPlayernum.changeColor(WHITE)
            textPlayernum.changeContent(font = fontSideNum, content = format(numPlayer, ","))
            flagPlayer = False
          if flagAverage:
            textAveragenum.changeColor(WHITE)
            textAveragenum.changeContent(font = fontSideNum, content = format(numAverage, ","))
            flagAverage = False
          if flagChips:
            textChipsinplaynum.changeColor(WHITE)
            textChipsinplaynum.changeContent(font = fontSideNum, content = format(numChips, ","))
            flagChips = False
          if flagEntries:
            textEntriesnum.changeColor(WHITE)
            textEntriesnum.changeContent(font = fontSideNum, content = format(numEntries, ","))
            flagEntries = False
          if flagStarting:
            textStartingstacknum.changeColor(WHITE)
            textStartingstacknum.changeContent(font = fontSideNum, content = format(numStarting, ","))
            flagStarting = False
          elif ((position[0] > textPlayernum.getRect().left and position[0] < textPlayernum.getRect().right) and (position[1] > textPlayernum.getRect().top and position[1] < textPlayernum.getRect().bottom)):
            flagPlayer = True
          elif ((position[0] > textAveragenum.getRect().left and position[0] < textAveragenum.getRect().right) and (position[1] > textAveragenum.getRect().top and position[1] < textAveragenum.getRect().bottom)):
            flagAverage = True
          elif ((position[0] > textChipsinplaynum.getRect().left and position[0] < textChipsinplaynum.getRect().right) and (position[1] > textChipsinplaynum.getRect().top and position[1] < textChipsinplaynum.getRect().bottom)):
            flagChips = True
          elif ((position[0] > textEntriesnum.getRect().left and position[0] < textEntriesnum.getRect().right) and (position[1] > textEntriesnum.getRect().top and position[1] < textEntriesnum.getRect().bottom)):
            flagEntries = True
          elif ((position[0] > textStartingstacknum.getRect().left and position[0] < textStartingstacknum.getRect().right) and (position[1] > textStartingstacknum.getRect().top and position[1] < textStartingstacknum.getRect().bottom)):
            flagStarting = True
    #####
    if(time.time() - start_time + pause_time > timer): ### 매 1초마다
      timer+=1
      min, sec, total, newLevel, min_break, sec_break = timeupdate(min, sec, total, 1, currLevel, soundLevelup,lstBreakIdx)
      if newLevel != currLevel:
        currLevel = newLevel
        try:
          if LSTLEVELS[currLevel]==0: ### End of blind
            while running:
              textPause.changeContent(font = fontPause, content = "No more blinds")
              pygame.draw.rect(surface, RED, rectPauseline, width=5)
              pygame.draw.rect(surface, PALEGRAY, rectNextLevel, width = 3)
              surface.blit(pauseBox, rectPause)
              surface.blit(textPause.getText(), textPause.getRect())
              pygame.display.flip()
              time.sleep(0.1)
              for event in pygame.event.get():
                if event.type == KEYDOWN:
                  if event.key == ord('q'):
                    running = False
          if LSTBLINDS[currLevel][0] == 0: #Break
            cntBreak+=1
            textCurrLevel.changeColor(BRIGHTRED)
            textCurrLevel.changeContent(font = fontTitleTournament, content = "Break")
            textBlind.changeContent(font = fontBlind, content = "- / -")
            textBBAnte.changeContent(font = fontBlind, content = "-")
            if LSTBLINDS[currLevel+1][0] == 0:
              temp_str1 = "- / -"
              temp_str = "-"
            else:
              tmp_str1 = format(LSTBLINDS[currLevel+1][0], ",") + " / " + format(LSTBLINDS[currLevel+1][1], ",")
              if LSTBLINDS[currLevel+1][2] != 0:
                temp_str = format(LSTBLINDS[currLevel+1][2], ",")
              else:
                temp_str = "-"
            textNextBlindnum.changeContent(font = fontNextLevelnum, content = tmp_str1)
            textNextBBAntenum.changeContent(font = fontNextLevelnum, content = temp_str)
          else:
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
        except:
          print("No levels left")
      strTimer = makeTimerString(min, sec, total)
      textMainTimer.changeContent(content = strTimer, font = fontMainTimer)
      strBreakTimer = makeTimerString(min_break,sec_break,total)
      textTimeBreaknum.changeContent(font = fontSideNum, content = strBreakTimer)
    surface.blit(imgBackground,(0,0))
    if flagPlayer:
      pygame.draw.rect(surface, PALEGRAY, textPlayernum.getRect())
    if flagStarting:
      pygame.draw.rect(surface, PALEGRAY, textStartingstacknum.getRect())
    if flagEntries:
      pygame.draw.rect(surface, PALEGRAY, textEntriesnum.getRect())
    if flagChips:
      pygame.draw.rect(surface, PALEGRAY, textChipsinplaynum.getRect())
    if flagAverage:
      pygame.draw.rect(surface, PALEGRAY, textAveragenum.getRect())
    blitText(surface, textMainTimer, textTitleTournament,textCurrLevel,textBlind,textTEXTBlind,textTEXTBBAnte,textBBAnte,textTEXTPlayer,textPlayernum,textAverage,textAveragenum,textChipsinplay,textChipsinplaynum,textEntries,textEntriesnum,textStartingstack,textTimeBreak,textTimeBreaknum,textStartingstacknum,textNextLevel,textNextBlind,textNextBBAnte,textNextBBAntenum,textNextBlindnum)
    pygame.draw.rect(surface, WHITE, rectMainTimer, width=3)
    pygame.draw.rect(surface, WHITE, rectCurrBlind, width=3)
    pygame.draw.rect(surface, PALEGRAY, rectNextLevel, width = 3)
    pygame.display.flip()
    time.sleep(0.05)
  soundLevelup.stop()
  pygame.quit()
#### End of main function
