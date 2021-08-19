from mine_sweeper_embedded import *
from tkinter import *
from functools import partial
import time

# 함수 정의
def level_easy():
  global level
  level = '초급'

def level_normal():
  global level
  level = '중급'

def level_hard():
  global level
  level = '고급'

def print_help():
  print('Nothing to tell you ^^')
  print(level_var.get())

def newgamebtncmd():
  level = level_var.get()
  Minesweeper.new_map_game(level)
  root.geometry(level_dict_dict[level]['size'])

# 레벨 선택
# level = input('난이도를 선택하세요: ')
level = '중급'
root = Tk()
root.title('Minesweeper')
root.geometry(level_dict_dict[level]['size']) # 가로 * 세로

# blockpixel 값에 따라 들어가는 이미지가 달라진다.
blockpixel = 30

# 이미지를 다운로드 받는다.
images_list = [f'{i}' for i in range(0, 9)] + [f'{i}' for i in range(0, 9)] + ['block', 'mine', 'flag', 'unknown', 'neutral', 'dead', 'win']
photo_dict = {image : PhotoImage(file=f'C:\\Users\\82102\\Desktop\\PythonWorkspace\\mine_sweeper\\images{blockpixel}px\\{image}.png') for image in images_list}

# 다시하기 버튼(표정 있음)이 들어있는 프레임
TopFrame = Frame(root)
TopFrame.pack(side='top', fill='x')

# 게임 판이 들어있는 프레임
MineFrame = Frame(root)
MineFrame.pack(side='top')

start_time = time.time()
Minesweeper = mineland(MineFrame, level, blockpixel, photo_dict, newgame=True)
end_time = time.time()
print(Minesweeper.minemap)
print(end_time - start_time)

# 게임, 도움말 탭이 있는 메뉴
menu = Menu(root)
menu_game = Menu(menu, tearoff=0)
menu_game.add_command(label='새 게임', state='active', command=newgamebtncmd)
menu_game.add_command(label='현재 게임판으로 다시 게임', state='active', command=Minesweeper.same_map_again)
menu_game.add_separator()
level_var = StringVar() # 레벨?
menu_game.add_radiobutton(label='초급', value='초급', variable=level_var)
menu_game.add_radiobutton(label='중급', value='중급', variable=level_var)
menu_game.add_radiobutton(label='고급', value='고급', variable=level_var)
menu.add_cascade(label='게임(G)', menu=menu_game)

menu_help = Menu(menu, tearoff=0)
menu_help.add_command(label='도움말', state='active', command=print_help)
# menu_help.add_separator()
menu.add_cascade(label='도움말(H)', menu=menu_help)

# 다시하기 버튼은 mineland 클래스 안에 넣어둔다.
Minesweeper.restart_btn = Button(TopFrame, image=Minesweeper.photo_dict['neutral'], command=newgamebtncmd)
Minesweeper.restart_btn.pack()
root.resizable(False, False) # x(너비), y(높이) 값 변경 불가
root.config(menu=menu)
root.mainloop()