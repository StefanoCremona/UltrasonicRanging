#!/usr/bin/env python3
########################################################################
# Filename    : UltrasonicRanging.py
# Description : Get distance from UltrasonicRanging.
# Author      : freenove - Stefano Cremona
# modification: 2019/10/04
########################################################################
import RPi.GPIO as GPIO
import time

trigPin = 16
trigPinA = 16
trigPinB = 36

echoPin = 18
echoPinA = 18
echoPinB = 38

rotation = 0

MAX_DISTANCE = 220          #define the maximum measured distance
pingFreq = 0.5              #define the freq of the signal check in seconds
timeOut = MAX_DISTANCE*60   #calculate timeout according to the maximum measured distance

def pulseIn(pin,level,timeOut): # function pulseIn: obtain pulse time of a pin
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    pulseTime = (time.time() - t0)*1000000
    return pulseTime

def getSonar():     #get the measurement results of ultrasonic module,with unit: cm
    GPIO.output(trigPin,GPIO.HIGH)      #make trigPin send 10us high level
    time.sleep(0.00001)     #10us
    GPIO.output(trigPin,GPIO.LOW)
    pingTime = pulseIn(echoPin,GPIO.HIGH,timeOut)   #read plus time of echoPin
    distance = pingTime * 340.0 / 2.0 / 10000.0     # the sound speed is 340m/s, and calculate distance
    return distance

def setup():
    print ('Program is starting...')
    GPIO.setmode(GPIO.BOARD)       #numbers GPIOs by physical location
    GPIO.setup(trigPinA, GPIO.OUT)   #
    GPIO.setup(trigPinB, GPIO.OUT)   #
    GPIO.setup(echoPinA, GPIO.IN)    #
    GPIO.setup(echoPinB, GPIO.IN)    #

def loop():
    while(True):
        distance = getSonar()
        print ("The distance of ", rotation % 2, " is : %.2f cm"%(distance))
    global rotation
    global echoPin
    global trigPin
    rotation += 1
    if rotation % 2 == 0:
        echoPin = echoPinA
        trigPin = trigPinA
    else:
        echoPin = echoPinB
        trigPin = trigPinB
        
        time.sleep(pingFreq)

if __name__ == '__main__':     #program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  #when 'Ctrl+C' is pressed, the program will exit
        GPIO.cleanup()         #release resource


    