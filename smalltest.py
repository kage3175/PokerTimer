import tkinter as tk
import ctypes

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
        TK_LST.append((rank1, rank2, prize))
  window.destroy()


user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
midpoint = screensize[0] / 2, screensize[1] / 2 # 화면 중앙점
screenScale = 1152/screensize[1]

def prizeInput(screenScale):
  window = tk.Tk()
  window.title('Prize')
  screen_width = window.winfo_screenwidth()
  screen_height = window.winfo_screenheight()
  width,height = round(1000/screenScale), round(1000/screenScale)

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
      entry.place(x=round(370/screenScale), y=round(50/screenScale)*(i//3)+round(20/screenScale),width=round(580/screenScale), height=round(30/screenScale))
    entries.append(entry)
  
  window.mainloop()

prizeInput(screenScale)
print(TK_LST)