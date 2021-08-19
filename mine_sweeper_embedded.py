# 모듈 임포트
from os import terminal_size
from random import shuffle
from functools import partial
import random
from tkinter import *
import time

# 클래스 정의
class mineland:
  def __init__(self, root, level, blockpixel, photo_dict, newgame=True):
    '''mineland 클래스 객체 init'''
    # 주요 인수들을 클래스 속성으로 저장
    self.root = root
    self.level = level
    self.blockpixel = blockpixel
    self.photo_dict = photo_dict
    self.level_dict = level_dict_dict[level]
    # 아래의 식에서 self.minemap, self.mineset, self.buttonmap_dict이 정의됨
    self.init_minemap_and_mineset(refresh=newgame)
    self.init_buttons(refresh=newgame)
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
    if self.minemap[coord] % 10 == 9:
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
    self.minemap[coord] += 10
    if (self.minemap[coord]//10) % 3 == 0: # 맵의 앞자리수가 0, 3, 6이면 아무것도 표시 안함
      self.buttonmap_dict[coord]['image'] = self.photo_dict['block']
      self.buttonmap_dict[coord]['state'] = 'active'      
    # 맵의 앞자리수가 1, 4, 7이면 깃발 표시, self.detected_mineset에 그 칸 넣음
    elif (self.minemap[coord]//10) % 3 == 1:
      self.buttonmap_dict[coord]['image'] = self.photo_dict['flag']
      self.buttonmap_dict[coord]['state'] = 'disabled'
      if coord in self.mineset:
        self.detected_mineset.add(coord)
    # 맵의 앞자리수가 2, 5, 8이면 물음표 표시, self.detected_mineset에서 그 칸 제거
    else: 
      self.buttonmap_dict[coord]['image'] = self.photo_dict['unknown']
      if coord in self.mineset:
        self.detected_mineset.remove(coord)
    # print(self.detected_mineset)
    # print(self.mineset)
    # 모든 지뢰 칸에만 깃발을 꽂았다면
    if self.mineset == self.detected_mineset:
      self.alldetected = True
      if self.allopened: # allopened도 True라면? 끝
        self.end()

  def init_buttons(self, refresh):
    '''buttonmap을 생성하는 함수'''
    try:
      if refresh:
        for button in self.buttonmap_dict.values():
          button.destroy()
    except AttributeError:
      refresh = False # 이것은 그냥 아무 의미가 없다.
    temp_buttonmap_dict = {(i, j): 0 for i in range(self.level_dict['col']) for j in range(self.level_dict['row'])}
    for coord in temp_buttonmap_dict.keys():
      x = coord[0]
      y = coord[1]
      temp_buttonmap_dict[coord] = Button(self.root, image=self.photo_dict['block'], command=partial(self.left_minecmd, coord), padx=0, pady=0, borderwidth=0)
      temp_buttonmap_dict[coord].grid(row=y, column=x)
      temp_buttonmap_dict[coord].bind('<Button-3>', partial(self.right_minecmd, coord))
    self.buttonmap_dict = temp_buttonmap_dict

  def lay_label(self, coord):
    x = coord[0]
    y = coord[1]
    if self.minemap[coord]%10 == 0:
      self.buttonmap_dict[coord] = Label(self.root, image=self.photo_dict['0'], padx=0, pady=0, borderwidth=0)
      self.buttonmap_dict[coord].grid(row=y, column=x)
    elif self.minemap[coord]%10 == 9:
      self.buttonmap_dict[coord] = Label(self.root, image=self.photo_dict['mine'], padx=0, pady=0, borderwidth=0)
      self.buttonmap_dict[coord].grid(row=y, column=x)
    else:
      self.buttonmap_dict[coord] = Label(self.root, image=self.photo_dict[f'{self.minemap[coord]%10}'], padx=0, pady=0, borderwidth=0)
      self.buttonmap_dict[coord].bind('<Button-1>', partial(self.label_leftclick, coord))
      self.buttonmap_dict[coord].bind('<Button-3>', partial(self.label_rightclick, coord))
      self.buttonmap_dict[coord].grid(row=y, column=x)

  def openblock(self, coord):
    col = self.level_dict['col']
    row = self.level_dict['row']
    # print(coord)
    coordset = {coord}
    majorset = {coord}
    minorset = {coord}
    checkorgo = 'go'
    if self.minemap[coord] % 10 == 0:
      checkorgo = 'check'

    while checkorgo == 'check':
      majorset = set(minorset)
      for coordinate in majorset:
        i = coordinate[0]
        j = coordinate[1]
        if self.minemap[coordinate] % 10 == 0:
          for m in range(max(0, i-1), min(i+2, col)):
            for n in range(max(0, j-1), min(j+2, row)):
              minorset.add((m, n))
          minorset = minorset - coordset
      coordset = minorset | coordset
      checkorgo = 'go'
      for coordinate in minorset:
        if self.minemap[coordinate] % 10 == 0:
          checkorgo = 'check'
    
    for coordinate in coordset:
      # print((x, y))
      self.buttonmap_dict[coordinate].destroy()
      self.lay_label(coordinate)
      self.openedset.add(coordinate)
    # 만약 모든 지뢰가 아닌 칸을 열었다면
    if len(self.openedset) == self.level_dict['row']*self.level_dict['col'] - self.level_dict['mines']:
      self.allopened = True
      if self.alldetected:
        self.end()

  # 다시하기를 위한 함수들 정의
  def same_map_again(self):
    print('old game')
    self.__init__(self.root, self.level, self.blockpixel, self.photo_dict, newgame=False)
    self.restart_btn['image'] = self.photo_dict['neutral']

  def new_map_game(self, level):
    print('new game')
    self.__init__(self.root, level, self.blockpixel, self.photo_dict, newgame=True)
    self.restart_btn['image'] = self.photo_dict['neutral']

  def dead(self):
    print('dead')
    for minecoord in self.mineset:
        self.buttonmap_dict[minecoord].destroy()
        self.lay_label(minecoord)
    self.restart_btn['image'] = self.photo_dict['dead']

  def end(self):
    print('win')
    self.restart_btn['image'] = self.photo_dict['win']

  # 라벨 양쪽클릭 이벤트를 위한 함수
  def label_leftclick(self, coord, event):
    # print('labelleft')
    self.lefton = True
    self.lefttime = time.time()
    if self.righton:
      if time.time() - self.righttime < 0.05:
        self.label_bothclick(coord)
      self.righton = False
    else:
      pass

  def label_rightclick(self, coord, event):
    # print('labelright')
    self.righton = True
    self.righttime = time.time()
    if self.lefton:
      if time.time() - self.lefttime < 0.05:
        self.label_bothclick(coord)
      self.lefton = False
    else:
      pass

  def label_bothclick(self, coord):
    col = self.level_dict['col']
    row = self.level_dict['row']
    x = coord[0]
    y = coord[1]
    # print('bothclicked!')
    self.righttime = self.lefttime = False
    temp_set = set()
    for i in range(max(0, x-1), min(x+2, col)):
      for j in range(max(0, y-1), min(y+2, row)):
        temp_set.add((i, j))
    temp_set.remove(coord)
    temp_set -= self.openedset
    for coordinate in set(temp_set):
      if self.buttonmap_dict[coordinate]['state'] == 'disabled':
        temp_set.remove(coordinate)
      elif self.minemap[coordinate] % 10 == 9:
        self.dead()
    
    while temp_set:
      self.openblock(temp_set.pop())
      temp_set -= self.openedset

  def init_minemap_and_mineset(self, refresh):
    if refresh:
      temp_minemap = {(i, j): 0 for i in range(self.level_dict['col']) for j in range(self.level_dict['row'])}
      temp_mineset = set()
      shuffle(coordinates:=list(temp_minemap.keys()))
      temp_mineset = set(coordinates[:self.level_dict['mines']])
      self.minemap = dict(temp_minemap)
      self.mineset = set()
      for minecoord in temp_mineset:
        self.minemap[minecoord] = 9
      for coord in temp_minemap.keys():
        if self.minemap[coord] != 9:
          self.minemap[coord] = self.assign_label_num(coord[0], coord[1])
        else:
          self.mineset.add(coord)

  def assign_label_num(self, x, y):
    '''
    지뢰가 없는 칸에 대하여 그 칸의 라벨 넘버를 
    '''
    col = self.level_dict['col']
    row = self.level_dict['row']
    temp_set = set()
    mines = 0
    for i in range(max(x-1, 0), min(col, x+2)):
      for j in range(max(y-1, 0), min(row, y+2)):
        temp_set.add((i, j))
    for temp_coord in temp_set:
      if self.minemap[temp_coord] % 10 == 9:
        mines += 1
    return mines

# 상수 정의
level_dict_dict = {
  '테스트': {'row': 3, 'col': 3, 'mines': 2, 'time': 10, 'size': '300x300'},
  '초급': {'row': 9, 'col': 9, 'mines': 10, 'time': 3600, 'size':'330x420'},
  '중급': {'row': 16, 'col': 16, 'mines': 40, 'time': 3600, 'size': '580x670'},
  '고급': {'row': 16, 'col': 30, 'mines': 99, 'time': 3600, 'size': '1100x670'}
}
