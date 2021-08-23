import time

def timetest(func):
  def wrapper(*args, **kwarg):
    start_time = time.time()
    func(*args, **kwarg)
    end_time = time.time()
    print(f'함수 {func.__name__}이 {end_time - start_time}만에 실행됨')
  return wrapper