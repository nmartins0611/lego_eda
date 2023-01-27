from buildhat import Motor
from time import sleep

motor_left = Motor('A')
motor_right = Motor('B')

#motor_left.run_for_seconds(seconds=10, speed=50)
#motor_right.run_for_seconds(seconds=10, speed=-50)
def stop():
  motor_left.stop()
  motor_right.stop()


def forward():
  motor_left.start(-30)
  motor_right.start(30)


for i in range(2):
  forward()
  sleep(1)
  stop()
  sleep(1)
