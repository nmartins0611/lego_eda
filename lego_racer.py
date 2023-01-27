from aiokafka import AIOKafkaProducer
from buildhat import ColorSensor
from os.path import exists
from buildhat import Motor
from time import sleep
import asyncio
import json
import pathlib
import os


forward = pathlib.Path("/tmp/forward")
backward = pathlib.Path("/tmp/backward")
left = pathlib.Path("/tmp/left")
right = pathlib.Path("/tmp/right")
motor_left = Motor('A')
motor_right = Motor('B')

#def drive():
#  motor_left.start("leftm")
#  motor_right.start("rightm")

def forward():
   os.remove("/tmp/forward")
   motor_left.start(-30)
   motor_right.start(30)
def backward():
   os.remove("/tmp/backward")
   motor_left.start(30)
   motor_right.start(-30)
def left():
  os.remove("/tmp/left")
  motor_left.start(30)
  motor_right.start(0)
def right():
  os.remove("/tmp/right")
  motor_left.start(0)
  motor_right.start(30)
def stop():
#  motor_left.start(0)
#  motor_right.start(0)
  print("stop")


def fileCheck():
  if exists("/tmp/forward"):
   for i in range(2):
     forward()
     sleep(1)
     stop()
     sleep(1)
  elif exists("/tmp/backward"):
   for i in range(2):
     backward()
     sleep(1)
     stop()
     sleep(1)
  elif exists("/tmp/left"):
      left()
  elif exists("/tmp/right"):
      right()
  else:
#    send_one()
    print("Nope")

async def send_one():
    producer = AIOKafkaProducer(bootstrap_servers='kafka.prometheus.io:9092')
    color = ColorSensor('C')

    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        while True:
            c = color.wait_for_new_color()
            colourData = {}
            colourData["color"] = c
            jsonData = json.dumps(colourData)

      # Produce message
 #           await producer.send_and_wait("network", bytes(c, encoding='utf-8'))
            await producer.send_and_wait("network", bytes(jsonData, encoding='utf-8'))
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()

asyncio.run(send_one())  
    
def main():
 fileCheck()


if __name__== "__main__":
   main()
