import tkinter as tk

def close_window(window, truefalse):
  print('ok')
  window.destroy()

def printEntry(entry):
  print(entry.get())

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
entry = tk.Entry(window)
entry.place(x=100, y=20)
yesB = tk.Button(window, width=15, height= 2, relief="raised", overrelief="solid", borderwidth=4, font = ("Arial", 15), text= "Yes", command = lambda: close_window(window, True))
yesB.place(x = 40, y = 80)
noB = tk.Button(window, width=15, height= 2, relief="raised", overrelief="solid", borderwidth=4, font = ("Arial", 15), text= "No", command = lambda: printEntry(entry))
noB.place(x = 280, y = 80)
window.mainloop()
