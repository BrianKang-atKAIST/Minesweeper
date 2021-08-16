from mine_sweeper_embedded import *
from tkinter import *
from functools import partial

level = '초급'

root = Tk()
root.title('Minesweeper')
root.geometry('300x300') # 가로 * 세로
#root.geometry('640x480+500+200') # 가로 * 세로 + x좌표 + y좌표

images_list = [f'{i}' for i in range(0, 9)] + ['block', 'mine', 'flag', 'unknown']
photo_dict = {image : PhotoImage(file=f'C:\\Users\\82102\\Desktop\\PythonWorkspace\\mine_sweeper\\images\\{image}.png') for image in images_list}

TopFrame = Frame(root)
TopFrame.pack(side='top', fill='x')

MineFrame = Frame(root)
MineFrame.pack(side='top')

Minesweeper = mineland(MineFrame, level)
print(Minesweeper.minemap)

root.resizable(True, True) # x(너비), y(높이) 값 변경 불가
root.mainloop()