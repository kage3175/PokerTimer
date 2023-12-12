import time

start_time = time.time()
timer = 0
minute_counter = 1
second_counter = 0
total_counter_sec = minute_counter*60 + second_counter
pause_time = 0
cnt = 1
print(str(minute_counter).zfill(2) + ":" + str(second_counter).zfill(2))
while total_counter_sec > 0:
  timer = time.time() - start_time + pause_time
  if(timer > cnt):
    if(second_counter == 0):
      minute_counter-=1
      second_counter = 59
      total_counter_sec-=1
    else:
      second_counter-=1
      total_counter_sec-=1
    print(str(minute_counter).zfill(2) + ":" + str(second_counter).zfill(2))
    cnt+=1
  time.sleep(0.05)