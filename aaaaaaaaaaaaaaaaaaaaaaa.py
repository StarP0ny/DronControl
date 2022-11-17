from djitellopy import Tello
import time

tello =Tello()
tello.connect()

commands={1:'forward ', -1:'back', 2:'up', -2:'down', 3:'right',-3:'left', 4:'tello.rotate_clockwise(90)'}

tello.takeoff()
time.sleep(5)
tello.move(commands[-1], 50)
time.sleep(5)
exec(commands[4])
tello.land()