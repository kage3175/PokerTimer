import pygame
from pygame.locals import *
import time
import random
import ctypes
import os

FONTPATH = {'NGothicR' : './font/NanumGothic.ttf', 'NSquareR' : './font/NanumSquareR.ttf'}
TESTMIN, TESTSEC, TESTTOTAL = 10,0,600
TESTLEVELS = [0,1,1,1,-1]
TESTBLINDS = [0,(100,200,200),(1000,2000,2000),0]

BLACK = (0,0,0)
WHITE = (240,240,240)
RED = (220,0,0)
BACKGROUND = (20,20,90)
PALEGRAY = (180,180,180)
K_NUM = [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]

def timeupdate(minute, second, total, amount):
  if total < amount:
    minute, second, total = 0,0,-1
  elif amount >= 0:
    if second < amount:
      minute -= (amount // 60 + 1)
      second = second + 60 - amount % 60
      total -= amount
    else:
      second -= amount
      total -= amount
  else: #### amount가 음수일 때, 즉 시간을 증가시킬 때
    pass
  return minute, second, total

def makeTimerString(min, sec, total):
  return str(min).zfill(2) + ':' + str(sec).zfill(2)

def levelupdate(amount):
  pass 

def main():
  running = True
  pygame.init()
  
  user32 = ctypes.windll.user32
  screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
  midpoint = screensize[0] / 2, screensize[1] / 2 # 화면 중앙점
  print(screensize)
  screenScale = 1152/screensize[1]
  surface = pygame.display.set_mode(screensize, FULLSCREEN)
  soundLevelup = pygame.mixer.Sound("./sound/levelup.mp3")

  start_time = time.time()
  timer = 0
  pause_time = 0
  currLevel = 1
  cntBreak = 0
  min, sec, total = TESTLEVELS[currLevel], 0, TESTLEVELS[currLevel]*60
  strTimer = makeTimerString(min, sec, total)
  
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


  ### location, loc 모음집
  locMainTimer = (midpoint[0], midpoint[1] - round(200 / screenScale))
  locTitleTournament = (midpoint[0], midpoint[1] - round(440 /screenScale))
  locTextCurrLevel = (midpoint[0], midpoint[1] + round(25 /screenScale))
  locCurrBlind = (midpoint[0], midpoint[1] + round(150/screenScale))
  #locTextBlind = (midpoint[0] + round(150/screenScale), midpoint[1] + round(115/screenScale))
  #locTextTEXTBlind = (midpoint[0] - round(200/screenScale), midpoint[1] + round(115/screenScale))

  #region texts

  #### text 모음집
  textMainTimer = fontMainTimer.render(strTimer, True, WHITE)
  objTextMainTimer = textMainTimer.get_rect()
  objTextMainTimer.center = locMainTimer
  textTitleTournament = fontTitleTournament.render('Test', True, PALEGRAY)
  objTextTitleTournament = textTitleTournament.get_rect()
  objTextTitleTournament.center = locTitleTournament
  textCurrLevel = fontTitleTournament.render('Level ' + str(currLevel), True, WHITE)
  objTextCurrLevel = textCurrLevel.get_rect()
  objTextCurrLevel.center = locTextCurrLevel
  textBlind = fontBlind.render("- / -", True, WHITE)
  objTextBlind = textBlind.get_rect()
  objTextBlind.centery = midpoint[1] + round(115/screenScale)
  objTextBlind.right = midpoint[0] + round(350/screenScale)
  textTEXTBlind = fontBlind.render("Blinds", True, WHITE)
  objTextTEXTBlind = textTEXTBlind.get_rect()
  objTextTEXTBlind.centery = midpoint[1] + round(115/screenScale)
  objTextTEXTBlind.left = midpoint[0] - round(300/screenScale)
  textTEXTBBAnte = fontBlind.render("BB Ante", True, WHITE)
  objTextTEXTBBAnte = textTEXTBBAnte.get_rect()
  objTextTEXTBBAnte.centery = midpoint[1] + round(175/screenScale)
  objTextTEXTBBAnte.left = midpoint[0] - round(300/screenScale)
  textBBAnte = fontBlind.render("-", True, WHITE)
  objTextBBAnte = textBBAnte.get_rect()
  objTextBBAnte.centery = midpoint[1] + round(175/screenScale)
  objTextBBAnte.right = midpoint[0] + round(350/screenScale)
  textTEXTPlayer = fontSide.render("Players", True, WHITE)
  objTextTEXTPlayer = textTEXTPlayer.get_rect()
  objTextTEXTPlayer.topleft = (round(115/screenScale),round(150/screenScale))
  textPlayernum = fontSideNum.render("0", True, WHITE)
  objTextPlayernum = textPlayernum.get_rect()
  objTextPlayernum.topleft = (round(115/screenScale),round(205/screenScale))
  textAverage = fontSide.render("Average Chips", True, WHITE)
  objTextAverage = textAverage.get_rect()
  objTextAverage.topleft = (round(115/screenScale),round(325/screenScale))
  textAveragenum = fontSideNum.render("0", True, WHITE)
  objTextAveragenum = textAveragenum.get_rect()
  objTextAveragenum.topleft = (round(115/screenScale),round(380/screenScale))
  textChipsinplay = fontSide.render("Chips in Play", True, WHITE)
  objTextChipsinplay = textChipsinplay.get_rect()
  objTextChipsinplay.topleft = (round(115/screenScale),round(500/screenScale))
  textChipsinplaynum = fontSideNum.render("0", True, WHITE)
  objTextChipsinplaynum = textChipsinplaynum.get_rect()
  objTextChipsinplaynum.topleft = (round(115/screenScale),round(555/screenScale))
  textEntries = fontSide.render("Entries", True, WHITE)
  objTextEntries = textEntries.get_rect()
  objTextEntries.topleft = (round(115/screenScale),round(675/screenScale))
  textEntriesnum = fontSideNum.render("0", True, WHITE)
  objTextEntriesnum = textEntriesnum.get_rect()
  objTextEntriesnum.topleft = (round(115/screenScale),round(730/screenScale))
  textStartingstack = fontSide.render("Starting Stacks", True, WHITE)
  objTextStartingstack = textStartingstack.get_rect()
  objTextStartingstack.topleft = (round(115/screenScale),round(850/screenScale))
  textStartingstacknum = fontSideNum.render("0", True, WHITE)
  objTextStartingstacknum = textStartingstacknum.get_rect()
  objTextStartingstacknum.topleft = (round(115/screenScale),round(905/screenScale))
  textPause = fontPause.render("Game Paused", True, BLACK)
  objTextPause = textPause.get_rect()
  objTextPause.center = locMainTimer

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

  pauseEvent = True
  pause_start = time.time()
  pause_time = 0

  while running:
    if pauseEvent:
      flag = True
      surface.blit(imgBackground,(0,0))
      surface.blit(textMainTimer, objTextMainTimer)
      surface.blit(textTitleTournament, objTextTitleTournament)
      surface.blit(textCurrLevel, objTextCurrLevel)
      surface.blit(textBlind, objTextBlind)
      surface.blit(textTEXTBlind, objTextTEXTBlind)
      surface.blit(textTEXTBBAnte, objTextTEXTBBAnte)
      surface.blit(textBBAnte, objTextBBAnte)
      surface.blit(textTEXTPlayer, objTextTEXTPlayer)
      if flagPlayer:
        pygame.draw.rect(surface, PALEGRAY, objTextPlayernum)
      surface.blit(textPlayernum, objTextPlayernum)
      surface.blit(textAverage, objTextAverage)
      if flagAverage:
        pygame.draw.rect(surface, PALEGRAY, objTextAveragenum)
      surface.blit(textAveragenum, objTextAveragenum)
      surface.blit(textChipsinplay, objTextChipsinplay)
      if flagChips:
        pygame.draw.rect(surface, PALEGRAY, objTextChipsinplaynum)
      surface.blit(textChipsinplaynum, objTextChipsinplaynum)
      surface.blit(textEntries, objTextEntries)
      if flagEntries:
        pygame.draw.rect(surface, PALEGRAY, objTextEntriesnum)
      surface.blit(textEntriesnum, objTextEntriesnum)
      surface.blit(textStartingstack, objTextStartingstack)
      if flagStarting:
        pygame.draw.rect(surface, PALEGRAY, objTextStartingstacknum)
      surface.blit(textStartingstacknum, objTextStartingstacknum)
      pygame.draw.rect(surface, WHITE, rectMainTimer, width=3)
      pygame.draw.rect(surface, RED, rectMidPoint)
      pygame.draw.rect(surface, WHITE, rectCurrBlind, width=3)
      pygame.draw.rect(surface, WHITE, rectPause)
      pygame.draw.rect(surface, RED, rectPauseline, width=5)
      surface.blit(textPause, objTextPause)
      pygame.display.flip()
      pause_time = pause_start - time.time()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        elif event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            surface = pygame.display.set_mode((500,500))
          if event.key == K_SPACE:
            print(11)
            soundLevelup.play()
            pauseEvent = False
            flag = False
            textBlind = fontBlind.render(format(TESTBLINDS[currLevel][0], ",")+" / "+format(TESTBLINDS[currLevel][1], ","), True, WHITE)
            objTextBlind = textBlind.get_rect()
            objTextBlind.centery = midpoint[1] + round(115/screenScale)
            objTextBlind.right = midpoint[0] + round(350/screenScale)
            if TESTBLINDS[currLevel][2] != 0:
              textBBAnte = fontBlind.render(format(TESTBLINDS[currLevel][2], ","), True, WHITE)
              objTextBBAnte = textBBAnte.get_rect()
              objTextBBAnte.centery = midpoint[1] + round(175/screenScale)
              objTextBBAnte.right = midpoint[0] + round(350/screenScale)
          if event.key == ord('q'):
            running=False
          if event.key in K_NUM:
            if flagPlayer or flagEntries or flagAverage or flagChips or flagStarting:
              temp_input = temp_input*10 + int(event.key) - 48
              if flagPlayer:
                textPlayernum = fontSideNum.render(format(temp_input, ","), True, BLACK)
                objTextPlayernum = textPlayernum.get_rect()
                objTextPlayernum.topleft = (round(115/screenScale),round(205/screenScale))
              elif flagAverage:
                textAveragenum = fontSideNum.render(format(temp_input, ","), True, BLACK)
                objTextAveragenum = textAveragenum.get_rect()
                objTextAveragenum.topleft = (round(115/screenScale),round(380/screenScale))
              elif flagChips:
                textChipsinplaynum = fontSideNum.render(format(temp_input, ","), True, BLACK)
                objTextChipsinplaynum = textChipsinplaynum.get_rect()
                objTextChipsinplaynum.topleft = (round(115/screenScale),round(555/screenScale))
              elif flagEntries:
                textEntriesnum = fontSideNum.render(format(temp_input, ","), True, BLACK)
                objTextEntriesnum = textEntriesnum.get_rect()
                objTextEntriesnum.topleft = (round(115/screenScale),round(730/screenScale))
              elif flagStarting:
                textStartingstacknum = fontSideNum.render(format(temp_input, ","), True, BLACK)
                objTextStartingstacknum = textStartingstacknum.get_rect()
                objTextStartingstacknum.topleft = (round(115/screenScale),round(905/screenScale))
          if event.key == K_RETURN:
            if flagPlayer:
              numPlayer = temp_input
              textPlayernum = fontSideNum.render(format(numPlayer, ","), True, WHITE)
              objTextPlayernum = textPlayernum.get_rect()
              objTextPlayernum.topleft = (round(115/screenScale),round(205/screenScale))
            elif flagAverage:
              numAverage = temp_input
              textAveragenum = fontSideNum.render(format(numAverage, ","), True, WHITE)
              objTextAveragenum = textAveragenum.get_rect()
              objTextAveragenum.topleft = (round(115/screenScale),round(380/screenScale))
            elif flagChips:
              numChips = temp_input
              textChipsinplaynum = fontSideNum.render(format(numChips, ","), True, WHITE)
              objTextChipsinplaynum = textChipsinplaynum.get_rect()
              objTextChipsinplaynum.topleft = (round(115/screenScale),round(555/screenScale))
              if numPlayer > 0:
                numAverage = numChips // numPlayer
                textAveragenum = fontSideNum.render(format(numAverage, ","), True, WHITE)
                objTextAveragenum = textAveragenum.get_rect()
                objTextAveragenum.topleft = (round(115/screenScale),round(380/screenScale))
            elif flagEntries:
              numEntries = temp_input
              textEntriesnum = fontSideNum.render(format(numEntries, ","), True, WHITE)
              objTextEntriesnum = textEntriesnum.get_rect()
              objTextEntriesnum.topleft = (round(115/screenScale),round(730/screenScale))
            elif flagStarting:
              numStarting = temp_input
              textStartingstacknum = fontSideNum.render(format(numStarting, ","), True, WHITE)
              objTextStartingstacknum = textStartingstacknum.get_rect()
              objTextStartingstacknum.topleft = (round(115/screenScale),round(905/screenScale))
            temp_input = 0
            flagPlayer, flagAverage, flagChips, flagEntries, flagStarting = False, False,False,False,False
        elif event.type == MOUSEBUTTONDOWN:
          position = pygame.mouse.get_pos()
          temp_input = 0
          if flagPlayer:
            textPlayernum = fontSideNum.render(format(numPlayer, ","), True, WHITE)
            objTextPlayernum = textPlayernum.get_rect()
            objTextPlayernum.topleft = (round(115/screenScale),round(205/screenScale))
            flagPlayer = False
          if flagAverage:
            textAveragenum = fontSideNum.render(format(numAverage, ","), True, WHITE)
            objTextAveragenum = textAveragenum.get_rect()
            objTextAveragenum.topleft = (round(115/screenScale),round(380/screenScale))
            flagAverage = False
          if flagChips:
            textChipsinplaynum = fontSideNum.render(format(numChips, ","), True, WHITE)
            objTextChipsinplaynum = textChipsinplaynum.get_rect()
            objTextChipsinplaynum.topleft = (round(115/screenScale),round(555/screenScale))
            flagChips = False
          if flagEntries:
            textEntriesnum = fontSideNum.render(format(numEntries, ","), True, WHITE)
            objTextEntriesnum = textEntriesnum.get_rect()
            objTextEntriesnum.topleft = (round(115/screenScale),round(730/screenScale))
            flagEntries = False
          if flagStarting:
            textStartingstacknum = fontSideNum.render(format(numStarting, ","), True, WHITE)
            objTextStartingstacknum = textStartingstacknum.get_rect()
            objTextStartingstacknum.topleft = (round(115/screenScale),round(905/screenScale))
            flagStarting = False
          elif ((position[0] > objTextPlayernum.left and position[0] < objTextPlayernum.right) and (position[1] > objTextPlayernum.top and position[1] < objTextPlayernum.bottom)):
            flagPlayer = True
          elif ((position[0] > objTextAveragenum.left and position[0] < objTextAveragenum.right) and (position[1] > objTextAveragenum.top and position[1] < objTextAveragenum.bottom)):
            flagAverage = True
          elif ((position[0] > objTextChipsinplaynum.left and position[0] < objTextChipsinplaynum.right) and (position[1] > objTextChipsinplaynum.top and position[1] < objTextChipsinplaynum.bottom)):
            flagChips = True
          elif ((position[0] > objTextEntriesnum.left and position[0] < objTextEntriesnum.right) and (position[1] > objTextEntriesnum.top and position[1] < objTextEntriesnum.bottom)):
            flagEntries = True
          elif ((position[0] > objTextStartingstacknum.left and position[0] < objTextStartingstacknum.right) and (position[1] > objTextStartingstacknum.top and position[1] < objTextStartingstacknum.bottom)):
            flagStarting = True
      time.sleep(0.05)
      pause_time+=pause_start-time.time()
      if flag:
        continue
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
        if event.key in K_NUM:
          if flagPlayer or flagEntries or flagAverage or flagChips or flagStarting:
            temp_input = temp_input*10 + int(event.key) - 48
            if flagPlayer:
              textPlayernum = fontSideNum.render(format(temp_input, ","), True, BLACK)
              objTextPlayernum = textPlayernum.get_rect()
              objTextPlayernum.topleft = (round(115/screenScale),round(205/screenScale))
            elif flagAverage:
              textAveragenum = fontSideNum.render(format(temp_input, ","), True, BLACK)
              objTextAveragenum = textAveragenum.get_rect()
              objTextAveragenum.topleft = (round(115/screenScale),round(380/screenScale))
            elif flagChips:
              textChipsinplaynum = fontSideNum.render(format(temp_input, ","), True, BLACK)
              objTextChipsinplaynum = textChipsinplaynum.get_rect()
              objTextChipsinplaynum.topleft = (round(115/screenScale),round(555/screenScale))
            elif flagEntries:
              textEntriesnum = fontSideNum.render(format(temp_input, ","), True, BLACK)
              objTextEntriesnum = textEntriesnum.get_rect()
              objTextEntriesnum.topleft = (round(115/screenScale),round(730/screenScale))
            elif flagStarting:
              textStartingstacknum = fontSideNum.render(format(temp_input, ","), True, BLACK)
              objTextStartingstacknum = textStartingstacknum.get_rect()
              objTextStartingstacknum.topleft = (round(115/screenScale),round(905/screenScale))
        if event.key == K_RETURN:
          if flagPlayer:
            numPlayer = temp_input
            textPlayernum = fontSideNum.render(format(numPlayer, ","), True, WHITE)
            objTextPlayernum = textPlayernum.get_rect()
            objTextPlayernum.topleft = (round(115/screenScale),round(205/screenScale))
          elif flagAverage:
            numAverage = temp_input
            textAveragenum = fontSideNum.render(format(numAverage, ","), True, WHITE)
            objTextAveragenum = textAveragenum.get_rect()
            objTextAveragenum.topleft = (round(115/screenScale),round(380/screenScale))
          elif flagChips:
            numChips = temp_input
            textChipsinplaynum = fontSideNum.render(format(numChips, ","), True, WHITE)
            objTextChipsinplaynum = textChipsinplaynum.get_rect()
            objTextChipsinplaynum.topleft = (round(115/screenScale),round(555/screenScale))
            if numPlayer > 0:
              numAverage = numChips // numPlayer
              textAveragenum = fontSideNum.render(format(numAverage, ","), True, WHITE)
              objTextAveragenum = textAveragenum.get_rect()
              objTextAveragenum.topleft = (round(115/screenScale),round(380/screenScale))
          elif flagEntries:
            numEntries = temp_input
            textEntriesnum = fontSideNum.render(format(numEntries, ","), True, WHITE)
            objTextEntriesnum = textEntriesnum.get_rect()
            objTextEntriesnum.topleft = (round(115/screenScale),round(730/screenScale))
          elif flagStarting:
            numStarting = temp_input
            textStartingstacknum = fontSideNum.render(format(numStarting, ","), True, WHITE)
            objTextStartingstacknum = textStartingstacknum.get_rect()
            objTextStartingstacknum.topleft = (round(115/screenScale),round(905/screenScale))
          temp_input = 0
          flagPlayer, flagAverage, flagChips, flagEntries, flagStarting = False, False,False,False,False
      elif event.type == MOUSEBUTTONDOWN:
          position = pygame.mouse.get_pos()
          temp_input = 0
          if flagPlayer:
            textPlayernum = fontSideNum.render(format(numPlayer, ","), True, WHITE)
            objTextPlayernum = textPlayernum.get_rect()
            objTextPlayernum.topleft = (round(115/screenScale),round(205/screenScale))
            flagPlayer = False
          if flagAverage:
            textAveragenum = fontSideNum.render(format(numAverage, ","), True, WHITE)
            objTextAveragenum = textAveragenum.get_rect()
            objTextAveragenum.topleft = (round(115/screenScale),round(380/screenScale))
            flagAverage = False
          if flagChips:
            textChipsinplaynum = fontSideNum.render(format(numChips, ","), True, WHITE)
            objTextChipsinplaynum = textChipsinplaynum.get_rect()
            objTextChipsinplaynum.topleft = (round(115/screenScale),round(555/screenScale))
            flagChips = False
          if flagEntries:
            textEntriesnum = fontSideNum.render(format(numEntries, ","), True, WHITE)
            objTextEntriesnum = textEntriesnum.get_rect()
            objTextEntriesnum.topleft = (round(115/screenScale),round(730/screenScale))
            flagEntries = False
          if flagStarting:
            textStartingstacknum = fontSideNum.render(format(numStarting, ","), True, WHITE)
            objTextStartingstacknum = textStartingstacknum.get_rect()
            objTextStartingstacknum.topleft = (round(115/screenScale),round(905/screenScale))
            flagStarting = False
          elif ((position[0] > objTextPlayernum.left and position[0] < objTextPlayernum.right) and (position[1] > objTextPlayernum.top and position[1] < objTextPlayernum.bottom)):
            flagPlayer = True
          elif ((position[0] > objTextAveragenum.left and position[0] < objTextAveragenum.right) and (position[1] > objTextAveragenum.top and position[1] < objTextAveragenum.bottom)):
            flagAverage = True
          elif ((position[0] > objTextChipsinplaynum.left and position[0] < objTextChipsinplaynum.right) and (position[1] > objTextChipsinplaynum.top and position[1] < objTextChipsinplaynum.bottom)):
            flagChips = True
          elif ((position[0] > objTextEntriesnum.left and position[0] < objTextEntriesnum.right) and (position[1] > objTextEntriesnum.top and position[1] < objTextEntriesnum.bottom)):
            flagEntries = True
          elif ((position[0] > objTextStartingstacknum.left and position[0] < objTextStartingstacknum.right) and (position[1] > objTextStartingstacknum.top and position[1] < objTextStartingstacknum.bottom)):
            flagStarting = True
    #####
    if(time.time() - start_time + pause_time > timer): ### 매 1초마다
      timer+=1
      min, sec, total = timeupdate(min, sec, total, 1)
      if total < 0: ### Level up 해야함
        currLevel+=1
        soundLevelup.play()
        try:
          if TESTLEVELS[currLevel] < 0: ### Break
            cntBreak +=1
            textCurrLevel = fontTitleTournament.render("BREAK", True, WHITE)
            min, sec, total = -TESTLEVELS[currLevel]-1, 59, -TESTLEVELS[currLevel]*60-1
          else:
            min, sec, total = TESTLEVELS[currLevel]-1, 59, TESTLEVELS[currLevel]*60-1
            textCurrLevel = fontTitleTournament.render('Level '+str(currLevel-cntBreak), True, WHITE)
            textBlind = fontBlind.render(format(TESTBLINDS[currLevel][0], ",")+" / "+format(TESTBLINDS[currLevel][1], ","), True, WHITE)
            objTextBlind = textBlind.get_rect()
            objTextBlind.centery = midpoint[1] + round(115/screenScale)
            objTextBlind.right = midpoint[0] + round(350/screenScale)
            if TESTBLINDS[currLevel][2] != 0:
              textBBAnte = fontBlind.render(format(TESTBLINDS[currLevel][2], ","), True, WHITE)
              objTextBBAnte = textBBAnte.get_rect()
              objTextBBAnte.centery = midpoint[1] + round(175/screenScale)
              objTextBBAnte.right = midpoint[0] + round(350/screenScale)
        except:
          print("No levels left")
        pass
      strTimer = makeTimerString(min, sec, total)
      textMainTimer = fontMainTimer.render(strTimer, True, WHITE)
      objTextMainTimer = textMainTimer.get_rect()
      objTextMainTimer.center = locMainTimer
    #surface.fill(BACKGROUND)
    surface.blit(imgBackground,(0,0))
    surface.blit(textMainTimer, objTextMainTimer)
    surface.blit(textTitleTournament, objTextTitleTournament)
    surface.blit(textCurrLevel, objTextCurrLevel)
    surface.blit(textBlind, objTextBlind)
    surface.blit(textTEXTBlind, objTextTEXTBlind)
    surface.blit(textTEXTBBAnte, objTextTEXTBBAnte)
    surface.blit(textBBAnte, objTextBBAnte)
    surface.blit(textTEXTPlayer, objTextTEXTPlayer)
    if flagPlayer:
      pygame.draw.rect(surface, PALEGRAY, objTextPlayernum)
    surface.blit(textPlayernum, objTextPlayernum)
    surface.blit(textAverage, objTextAverage)
    if flagAverage:
      pygame.draw.rect(surface, PALEGRAY, objTextAveragenum)
    surface.blit(textAveragenum, objTextAveragenum)
    surface.blit(textChipsinplay, objTextChipsinplay)
    if flagChips:
      pygame.draw.rect(surface, PALEGRAY, objTextChipsinplaynum)
    surface.blit(textChipsinplaynum, objTextChipsinplaynum)
    surface.blit(textEntries, objTextEntries)
    if flagEntries:
      pygame.draw.rect(surface, PALEGRAY, objTextEntriesnum)
    surface.blit(textEntriesnum, objTextEntriesnum)
    surface.blit(textStartingstack, objTextStartingstack)
    if flagStarting:
      pygame.draw.rect(surface, PALEGRAY, objTextStartingstacknum)
    surface.blit(textStartingstacknum, objTextStartingstacknum)
    pygame.draw.rect(surface, WHITE, rectMainTimer, width=3)
    pygame.draw.rect(surface, RED, rectMidPoint)
    pygame.draw.rect(surface, WHITE, rectCurrBlind, width=3)
    pygame.display.flip()
    time.sleep(0.05)
  soundLevelup.stop()
  pygame.quit()
main()
