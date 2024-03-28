import pygame
from ClassObjs import *
import ctypes

BACKGROUND = (60, 55, 230)

def test(screen, rect, screenScale):
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
  #pygame.draw.line(screen, )

pygame.init()

clock = pygame.time.Clock()
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
print(screensize)
midpoint = screensize[0] / 2, screensize[1] / 2 # 화면 중앙점
screenScale = 1152/screensize[1]
screen = pygame.display.set_mode()

bigRect = pygame.Rect(0,0,round(1996/screenScale),round(1096/screenScale))
bigRect.topleft = (round(26/screenScale), round(28/screenScale))

img = pygame.image.load('./img/Aria_Style.png')
img = pygame.transform.scale(img, screensize)

fontTitle = pygame.font.Font('./font/NanumSquareEB.ttf', round(65/screenScale))
fontMainTimer = pygame.font.Font('./font/NanumSquareEB.ttf', round(200/screenScale))
fontLevel = pygame.font.Font('./font/NanumSquareB.ttf', round(70/screenScale))
fontLeftObjs = pygame.font.Font('./font/NanumSquareEB.ttf', round(60/screenScale))
fontRightObjs = pygame.font.Font('./font/NanumSquareB.ttf', round(42/screenScale))
fontLeftSmall = pygame.font.Font('./font/NanumGothicExtraBold.ttf', round(30/screenScale))


textTitle = TextObj(font = fontTitle, content='Title', position=(midpoint[0],round(230/screenScale)), relative='center', color=WHITE)
textMainTimer = TextObj(font = fontMainTimer, content = '19:00', position=(midpoint[0], round(483/screenScale)), relative='center', color=WHITE)
textLevel = TextObj(font = fontLevel, content='Level 6', position=(midpoint[0], round(326/screenScale)), relative='center', color=WHITE)
textSB = TextObj(font = fontLeftObjs, content='Small Blind:', position=(round(505/screenScale), round(605/screenScale)), relative='topright', color=WHITE)
textBB = TextObj(font = fontLeftObjs, content='Big Blind:', position=(round(505/screenScale), round(680/screenScale)), relative='topright', color=WHITE)
textAnte = TextObj(font = fontLeftObjs, content='Ante:', position=(round(505/screenScale), round(755/screenScale)), relative='topright', color=WHITE)
textNextSB = TextObj(font = fontRightObjs, content='Next Small Blind:', position=(round(1500/screenScale), round(605/screenScale)), relative='topright', color=WHITE)
textNextBB = TextObj(font = fontRightObjs, content='Next Big Blind:', position=(round(1500/screenScale), round(660/screenScale)), relative='topright', color=WHITE)
textNextAnte = TextObj(font = fontRightObjs, content='Next Ante:', position=(round(1500/screenScale), round(715/screenScale)), relative='topright', color=WHITE)
textAvgChips = TextObj(font = fontRightObjs, content='Average Chips:', position=(round(1500/screenScale), round(770/screenScale)), relative='topright', color=WHITE)
textTotalChips = TextObj(font = fontRightObjs, content='Total Chips:', position=(round(1500/screenScale), round(825/screenScale)), relative='topright', color=WHITE)
textStartingStack = TextObj(font = fontRightObjs, content='Starting Stack:', position=(round(1500/screenScale), round(880/screenScale)), relative='topright', color=WHITE)
textTimetoBreak = TextObj(font = fontRightObjs, content='Time to Break:', position=(round(1500/screenScale), round(935/screenScale)), relative='topright', color=WHITE)

textSBnum = TextObj(font = fontLeftObjs, content='6,000', position=(round(515/screenScale), round(605/screenScale)), relative='topleft', color=WHITE)
textBBnum = TextObj(font = fontLeftObjs, content='12,000', position=(round(515/screenScale), round(680/screenScale)), relative='topleft', color=WHITE)
textAntenum = TextObj(font = fontLeftObjs, content='12,000', position=(round(515/screenScale), round(755/screenScale)), relative='topleft', color=WHITE)

textNextSBnum = TextObj(font = fontRightObjs, content='8,000', position=(round(1510/screenScale), round(605/screenScale)), relative='topleft', color=WHITE)
textNextBBnum = TextObj(font = fontRightObjs, content='16,000', position=(round(1510/screenScale), round(660/screenScale)), relative='topleft', color=WHITE)
textNextAntenum = TextObj(font = fontRightObjs, content='16,000', position=(round(1510/screenScale), round(715/screenScale)), relative='topleft', color=WHITE)
textAvgChipsnum = TextObj(font = fontRightObjs, content='625,000', position=(round(1510/screenScale), round(770/screenScale)), relative='topleft', color=WHITE)
textTotalChipsnum = TextObj(font = fontRightObjs, content='2,500,000', position=(round(1510/screenScale), round(825/screenScale)), relative='topleft', color=WHITE)
textStartingStacknum = TextObj(font = fontRightObjs, content='100,000', position=(round(1510/screenScale), round(880/screenScale)), relative='topleft', color=WHITE)
textTimetoBreaknum = TextObj(font = fontRightObjs, content='10:00', position=(round(1510/screenScale), round(935/screenScale)), relative='topleft', color=WHITE)

textEntrants = TextObj(font = fontLeftSmall, content='Entrants', position=(round(266/screenScale), round(930/screenScale)), relative='center', color=WHITE)
textPlayersLeft = TextObj(font = fontLeftSmall, content='Players Left', position=(round(765/screenScale), round(930/screenScale)), relative='center', color=WHITE)
textEntrantsnum = TextObj(font = fontLeftObjs, content='25', position=(round(266/screenScale), round(998/screenScale)), relative='center', color=WHITE)
textPlayersLeftnum = TextObj(font = fontLeftObjs, content='4', position=(round(765/screenScale), round(998/screenScale)), relative='center', color=WHITE)

while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
    elif event.type == KEYDOWN:
      if event.key == ord('q'):
        pygame.quit()
    elif event.type == MOUSEBUTTONDOWN:
      if event.button == 1:
        position = pygame.mouse.get_pos()
        print(position)

  #screen.blit(img, (0,0))
  test(screen, bigRect, screenScale)
  screen.blit(textTitle.getText(), textTitle.getRect())
  screen.blit(textMainTimer.getText(), textMainTimer.getRect())
  screen.blit(textLevel.getText(), textLevel.getRect())
  screen.blit(textSB.getText(), textSB.getRect())
  screen.blit(textBB.getText(), textBB.getRect())
  screen.blit(textAnte.getText(), textAnte.getRect())
  screen.blit(textNextSB.getText(), textNextSB.getRect())
  screen.blit(textNextBB.getText(), textNextBB.getRect())
  blitText(screen, textNextAnte, textAvgChips, textTotalChips, textStartingStack, textTimetoBreak, textSBnum, textBBnum, textAntenum, textNextSBnum, textNextBBnum, textNextAntenum, textAvgChipsnum, textTotalChipsnum, textStartingStacknum, textTimetoBreaknum, textEntrants, textPlayersLeft, textEntrantsnum, textPlayersLeftnum)
  pygame.display.flip()
  clock.tick(FPS)
