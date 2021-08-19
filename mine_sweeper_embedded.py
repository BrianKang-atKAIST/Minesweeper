# 모듈 임포트
from random import shuffle
from functools import partial
from tkinter import *
import time

# 클래스 정의
class mineland:
  def __init__(self, root, level, blockpixel):
    '''mineland 클래스 객체 init'''
    # 이미지 다운로드
    self.images_list = [f'{i}' for i in range(0, 9)] + [f'{i}' for i in range(0, 9)] + ['block', 'mine', 'flag', 'unknown', 'neutral', 'dead', 'win']
    self.photo_dict = {image : PhotoImage(file=f'C:\\Users\\82102\\Desktop\\PythonWorkspace\\mine_sweeper\\images{blockpixel}px\\{image}.png') for image in self.images_list}
    # 주요 인수들을 클래스 속성으로 저장
    self.root = root
    self.level = level
    self.blockpixel = blockpixel
    self.level_dict = level_dict_dict[level]
    self.minemap, self.mineset = self.init_mines()
    self.buttonmap = self.init_buttons()
    self.openedset = set()
    # 라벨 마우스 양쪽 버튼으로 클릭 시 나오는 이펙트 구현을 위한 상수들
    self.lefton = False # 왼쪽 버튼을 눌렀나?
    self.righton = False # 오른쪽 버튼을 눌렀나?
    self.lefttime = 0 # 왼쪽 버튼을 언제 눌렀나?
    self.righttime = 0 # 오른쪽 버튼을 언제 눌렀나?
    # 게임 종료를 위한 상수들
    self.detected_mineset = set()
    self.alldetected = False
    self.allopened = False

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
    # print('left', coord)
    x = coord[0]
    y = coord[1]
    if self.minemap[y][x] % 10 == 9:
      self.dead()
    else:
      self.openblock(coord)

  def right_minecmd(self, coord, event):
    '''
    **event는 bind에서 강제로 집어넣어줘서 넣음
    bind로 버튼과 연결되어 right클릭을 하면 호출됨
    right클릭을 할때마다 해당되는 self.minemap 칸에 10을 더함
    10의 자리 수가 깃발, 물음표, 아무것도 없음 이 셋을 결정
    '''
    # print('right', coord)
    x = coord[0]
    y = coord[1]
    self.minemap[y][x] += 10
    if (self.minemap[y][x]//10) % 3 == 0: # 맵의 앞자리수가 0, 3, 6이면 아무것도 표시 안함
      self.buttonmap[y][x]['image'] = self.photo_dict['block']
      self.buttonmap[y][x]['state'] = 'active'      
    # 맵의 앞자리수가 1, 4, 7이면 깃발 표시, self.detected_mineset에 그 칸 넣음
    elif (self.minemap[y][x]//10) % 3 == 1:
      self.buttonmap[y][x]['image'] = self.photo_dict['flag']
      self.buttonmap[y][x]['state'] = 'disabled'
      if coord in self.mineset:
        self.detected_mineset.add(coord)
    # 맵의 앞자리수가 2, 5, 8이면 물음표 표시, self.detected_mineset에서 그 칸 제거
    else: 
      self.buttonmap[y][x]['image'] = self.photo_dict['unknown']
      if coord in self.mineset:
        self.detected_mineset.remove(coord)
    # print(self.detected_mineset)
    # print(self.mineset)
    # 모든 지뢰 칸에만 깃발을 꽂았다면
    if self.mineset == self.detected_mineset:
      self.alldetected = True
      if self.allopened: # allopened도 True라면? 끝
        self.end()

  def init_mines(self):
    '''minemap에 지뢰를 놓는다.'''
    temp_minemap = [[0 for i in range(self.level_dict['col'])] for i in range(self.level_dict['row'])]
    return lay_mine(temp_minemap, self.level_dict['mines'])

  def init_buttons(self):
    '''buttonmap을 생성하는 함수'''
    temp_buttonmap = [[0 for i in range(self.level_dict['col'])] for i in range(self.level_dict['row'])]
    for y, row in enumerate(temp_buttonmap):
      for x, block in enumerate(row):
        coord = (x, y)
        temp_buttonmap[y][x] = Button(self.root, image=self.photo_dict['block'], command=partial(self.left_minecmd, coord))
        temp_buttonmap[y][x].grid(row=y, column=x)
        temp_buttonmap[y][x].bind('<Button-3>', partial(self.right_minecmd, coord))
    return temp_buttonmap

  def lay_label(self, coord):
    x = coord[0]
    y = coord[1]
    if self.minemap[y][x]%10 == 0:
      self.buttonmap[y][x] = Label(self.root, image=self.photo_dict['0'])
      self.buttonmap[y][x].grid(row=y, column=x)
    elif self.minemap[y][x]%10 == 9:
      self.buttonmap[y][x] = Label(self.root, image=self.photo_dict['mine'])
      self.buttonmap[y][x].grid(row=y, column=x)
    else:
      self.buttonmap[y][x] = Label(self.root, image=self.photo_dict[f'{self.minemap[y][x]%10}'])
      self.buttonmap[y][x].bind('<Button-1>', partial(self.label_leftclick, coord))
      self.buttonmap[y][x].bind('<Button-3>', partial(self.label_rightclick, coord))
      self.buttonmap[y][x].grid(row=y, column=x)

  def openblock(self, coord):
    rightend = len(self.minemap[0])
    bottomend = len(self.minemap)
    # print(coord)
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
      # print((x, y))
      self.buttonmap[y][x].destroy()
      self.lay_label((x, y))
      self.openedset.add((x, y))
    # 만약 모든 지뢰가 아닌 칸을 열었다면
    if len(self.openedset) == self.level_dict['row']*self.level_dict['col'] - self.level_dict['mines']:
      self.allopened = True
      if self.alldetected:
        self.end()

  # 다시하기를 위한 함수들 정의
  def again(self):
    print('new game')
    self.__init__(self.root, self.level, self.blockpixel)
    self.restart_btn['image'] = self.photo_dict['neutral']

  def dead(self):
    print('dead')
    for minecoord in self.mineset:
        self.buttonmap[minecoord[1]][minecoord[0]].destroy()
        self.lay_label(minecoord)
    self.restart_btn['image'] = self.photo_dict['dead']

  def end(self):
    print('win')
    self.restart_btn['image'] = self.photo_dict['win']

  # 라벨 양쪽클릭 이벤트를 위한 함수
  def label_leftclick(self, coord, event):
    print('labelleft')
    self.lefton = True
    self.lefttime = time.time()
    if self.righton:
      if time.time() - self.righttime < 0.05:
        self.label_bothclick(coord)
      self.righton = False
    else:
      pass

  def label_rightclick(self, coord, event):
    print('labelright')
    self.righton = True
    self.righttime = time.time()
    if self.lefton:
      if time.time() - self.lefttime < 0.05:
        self.label_bothclick(coord)
      self.lefton = False
    else:
      pass

  def label_bothclick(self, coord):
    rightend = len(self.minemap[0])
    bottomend = len(self.minemap)
    x = coord[0]
    y = coord[1]
    print('bothclicked!')
    self.righttime = self.lefttime = False
    temp_set = set()
    for i in range(max(0, x-1), min(x+2, rightend)):
      for j in range(max(0, y-1), min(y+2, bottomend)):
        temp_set.add((i, j))
    temp_set.remove(coord)
    temp_set -= self.openedset
    for coordinate in set(temp_set):
      if self.buttonmap[coordinate[1]][coordinate[0]]['state'] == 'disabled':
        temp_set.remove(coordinate)
      elif self.minemap[coordinate[1]][coordinate[0]] % 10 == 9:
        self.dead()
        pass
    
    while temp_set:
      self.openblock(temp_set.pop())
      temp_set -= self.openedset

# 함수 정의
def lay_mine(minemap, mines):
  rownum = len(minemap)
  colnum = len(minemap[0])
  mineset = set()
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
      else:
        mineset.add((x, y))
  return minemap, mineset

def assign_label_num(minemap, x, y):
  '''
  지뢰가 없는 칸에 대하여 그 칸의 라벨 넘버를 
  '''
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
  '테스트': {'row': 3, 'col': 3, 'mines': 2, 'time': 10, 'size': '300x300'},
  '초급': {'row': 9, 'col': 9, 'mines': 10, 'time': 3600, 'size':'330x420'},
  '중급': {'row': 16, 'col': 16, 'mines': 40, 'time': 3600, 'size': '580x670'},
  '고급': {'row': 16, 'col': 30, 'mines': 99, 'time': 3600, 'size': '1100x670'}
}
