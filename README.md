지뢰 찾기 게임 (Minesweeper)를 파이썬으로 구현

0. 목차
- 1. 사용 모듈
- 2. 구현 방식
- 3. 클래스 속성과 주요 상수들 도입 이유와 구조 설명
- 4. 함수들 설명
- 5. 게임 흐름 설명
- 6. 흐름에 따른 함수와 속성의 사용

1. 사용 모듈
1) 기초적인 그래픽: tkinter
- 윈도우 xp에서 사용했던 지뢰찾기와 비슷한 모습을 보여줄 수 있을 것 같아서 선택함.
2) 랜덤적 요소: random
- 설명이 필요없다.
3) 버튼 커맨드에 추가적 요소: functools
- 이것이 없다면 버튼에 함수를 연결할 때 self를 제외한 인수를 투입할 수 없다.
4) 양쪽 마우스 버튼 클릭을 위한 time
- 두 독립적인 클릭이 '동시'와 비슷한 시간 내에 일어났다는 것을 표현하기 위하여 사용되었다.

2. 구현 방식
tkinter를 이용하여 화면 생성
mineland 객체 자체가 여러 개의 버튼과 그 버튼에 연결된 함수를 가진 기계와 같은 객체가 된다.
객체 내에 모든 임베디드 시스템을 갖춘 하나의 전자제품과 같은 형태
사용자는 그 버튼들을 조작하며 객체를 변경해 나가고, 객체를 재생성하는 동작이 게임의 재시작이 된다.

3. mineland 클래스 설명