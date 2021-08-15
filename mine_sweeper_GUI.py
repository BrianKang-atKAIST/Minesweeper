from mine_sweeper_embedded import *
from tkinter import *
from functools import partial

level = '초급'

root = Tk()
root.title('Minesweeper')
root.geometry('300x300') # 가로 * 세로
#root.geometry('640x480+500+200') # 가로 * 세로 + x좌표 + y좌표

TopFrame = Frame(root)
TopFrame.pack(side='top', fill='x')

MineFrame = Frame(root)
MineFrame.pack(side='top')

Minesweeper = mineland(MineFrame, level)
print(Minesweeper.minemap)

root.resizable(True, True) # x(너비), y(높이) 값 변경 불가
root.mainloop()