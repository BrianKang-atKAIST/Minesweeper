# 모듈 임포트
from random import shuffle
from functools import partial
from tkinter import *

# 클래스 정의
class mineland:
  def __init__(self, root, level):
    '''mineland 클래스 객체 init'''
    self.root = root
    self.level = level
    self.level_dict = level_dict_dict[level]
    self.minemap = self.init_mines()
    self.buttonmap = self.init_buttons()
    self.win = self.level_dict['win']

  def left_minecmd(self, coord):
    '''
    아직 열리지 않은 칸에 깃발 또는 물음표가 없으면 클릭이 가능\
    (self.right_minecmd 함수에서 disabled 지정으로 구현)
    클릭하여 폭탄이 있으면 사망(self.dead 호출)
    폭탄이 없으면 self.openblock을 호출하는데, 이 함수는
    1. 버튼 없애고, 
    2. lay_label 호출
      1) self.buttonmap을 라벨로 교체
      2) 라벨 pack
      3) 만약 칸이 0개의 지뢰와 맞닿아 있다면 주변 모든 칸 클릭
    '''
    print('left', coord)
    x = coord[0]
    y = coord[1]
    if self.minemap[y][x] % 10 == 9:
      self.dead()
    else:
      self.openblock(coord)
      self.win -= 1
      if self.win == 0:
        self.end()

  def right_minecmd(self, coord, event):
    '''
    **event는 bind에서 강제로 집어넣어줘서 넣음
    bind로 버튼과 연결되어 right클릭을 하면 호출됨
    right클릭을 할때마다 해당되는 self.minemap 칸에 10을 더함
    10의 자리 수가 깃발, 물음표, 아무것도 없음 이 셋을 결정
    '''
    print('right', coord)
    x = coord[0]
    y = coord[1]
    self.minemap[y][x] += 10
    if (self.minemap[y][x]//10) % 3 == 0: # 맵의 앞자리수가 0, 3, 6이면 아무것도 표시 안함
      self.buttonmap[y][x]['text'] = ''
      self.buttonmap[y][x]['state'] = 'active'      
    elif (self.minemap[y][x]//10) % 3 == 1: # 맵의 앞자리수가 1, 4, 7이면 깃발 표시
      self.buttonmap[y][x]['text'] = '깃'
      self.buttonmap[y][x]['state'] = 'disabled'      
    else: # 맵의 앞자리수가 2, 5, 8이면 물음표 표시
      self.buttonmap[y][x]['text'] = '?'

  def init_mines(self):
    temp_minemap = [[0 for i in range(self.level_dict['col'])] for i in range(self.level_dict['row'])]
    return lay_mine(temp_minemap, self.level_dict['mines'])

  def init_buttons(self):
    temp_buttonmap = [[0 for i in range(self.level_dict['col'])] for i in range(self.level_dict['row'])]
    for y, row in enumerate(temp_buttonmap):
      for x, block in enumerate(row):
        coord = (x, y)
        temp_buttonmap[y][x] = Button(self.root, text=str(coord), width=2, height=1, command=partial(self.left_minecmd, coord))
        temp_buttonmap[y][x].grid(row=y, column=x)
        temp_buttonmap[y][x].bind('<Button-3>', partial(self.right_minecmd, coord))
    return temp_buttonmap

  def lay_label(self, coord):
    x = coord[0]
    y = coord[1]
    if self.minemap[y][x]%10 == 0:
      self.buttonmap[y][x] = Label(self.root, width=2, height=1)
      self.buttonmap[y][x].grid(row=y, column=x)
    else:
      self.buttonmap[y][x] = Label(self.root, text=f'{self.minemap[y][x]%10}', width=2, height=1)
      self.buttonmap[y][x].grid(row=y, column=x)

  def openblock(self, coord):
    rightend = len(self.minemap[0])
    bottomend = len(self.minemap)
    print(coord)
    x = coord[0]
    y = coord[1]
    coordset = {coord}
    majorset = {coord}
    minorset = {coord}
    checkorgo = 'go'
    if self.minemap[y][x] % 10 == 0:
      checkorgo = 'check'

    while checkorgo == 'check':
      majorset = set(minorset)
      for coordinate in majorset:
        i = coordinate[0]
        j = coordinate[1]
        if self.minemap[j][i] % 10 == 0:
          for m in range(max(0, i-1), min(i+2, rightend)):
            for n in range(max(0, j-1), min(j+2, bottomend)):
              minorset.add((m, n))
          minorset = minorset - coordset
      coordset = minorset | coordset
      checkorgo = 'go'
      for (x, y) in minorset:
        if self.minemap[y][x] % 10 == 0:
          checkorgo = 'check'
    
    for (x, y) in coordset:
      print((x, y))
      self.buttonmap[y][x].destroy()
      self.lay_label((x, y))
    
  def dead(self):
    print('dead')
    pass

  def end(self):
    print('win')

# 함수 정의
def lay_mine(minemap, mines):
  rownum = len(minemap)
  colnum = len(minemap[0])
  temp_set = [i for i in range(rownum*colnum)]
  shuffle(temp_set)
  for mine in range(mines):
    minexy = temp_set.pop()
    # print(minexy)
    minemap[minexy//colnum][minexy%colnum] = 9
  for y, row in enumerate(minemap):
    for x, block in enumerate(row):
      if block != 9:
        minemap[y][x] = assign_label_num(minemap, x, y)
  return minemap

def assign_label_num(minemap, x, y):
  rightend = len(minemap[0])
  bottomend = len(minemap)
  temp_list = []
  mines = 0
  for i in range(max(x-1, 0), min(rightend, x+2)):
    for j in range(max(y-1, 0), min(bottomend, y+2)):
      temp_list.append((i, j))
  for xx, yy in temp_list:
    if minemap[yy][xx] % 10 == 9:
      mines += 1
  return mines

# 상수 정의
level_dict_dict = {
  '테스트': {'row': 3, 'col': 3, 'mines': 2, 'time': 10, 'win': 7},
  '초급': {'row': 9, 'col': 9, 'mines': 10, 'time': 3600, 'win': 71},
  '중급': {'row': 16, 'col': 16, 'mines': 40, 'time': 3600, 'win': 216},
  '고급': {'row': 16, 'col': 30, 'mines': 99, 'time': 3600, 'win': 381}
}