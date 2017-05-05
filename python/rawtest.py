import RPi.GPIO as GPIO
import time
GPIO.VERSION
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.IN)

while True:
    try:
        if(GPIO.input(3)==1):
            print("Touched3")
            time.sleep(.5)
    except IOError:
        GPIO.cleanup()
        print "Error"
