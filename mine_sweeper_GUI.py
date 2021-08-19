from mine_sweeper_embedded import *
from tkinter import *
from functools import partial
import time

# 레벨 선택
# level = input('난이도를 선택하세요: ')
level = '고급'
root = Tk()
root.title('Minesweeper')
root.geometry(level_dict_dict[level]['size']) # 가로 * 세로


# 다시하기 버튼(표정 있음)이 들어있는 프레임
TopFrame = Frame(root)
TopFrame.pack(side='top', fill='x')

# 게임 판이 들어있는 프레임
MineFrame = Frame(root)
MineFrame.pack(side='top')

start_time = time.time()
Minesweeper = mineland(MineFrame, level, 30)
end_time = time.time()
print(Minesweeper.minemap)
print(end_time - start_time)

# 다시하기 버튼은 mineland 클래스 안에 넣어둔다.
Minesweeper.restart_btn = Button(TopFrame, image=Minesweeper.photo_dict['neutral'], command=Minesweeper.again)
Minesweeper.restart_btn.pack()
root.resizable(True, True) # x(너비), y(높이) 값 변경 불가
root.mainloop()