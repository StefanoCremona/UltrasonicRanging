#!/usr/bin/env python3
########################################################################
# Filename    : UltrasonicRanging.py
# Description : Get distance from UltrasonicRanging.
# Author      : freenove
# modification: 2018/08/03
########################################################################
import RPi.GPIO as GPIO
import time
import sys

trigPin = 16
#trigPin = 36
echoPin = 18
#echoPin = 38
ledPin = 11

MAX_DISTANCE = 220          #define the maximum measured distance
pingFreq = 0.5              #define the freq in seconds of the signal check
executionTime = 3           #Second after that the registration terminates.
executions = 5              #Recording events
timeOut = MAX_DISTANCE*60   #calculate timeout according to the maximum measured distance

f = open("walkingStef.txt", "a")

def setup():
    print ('Program is starting...')
    GPIO.setmode(GPIO.BOARD)        #numbers GPIOs by physical location
    GPIO.setup(trigPin, GPIO.OUT)   #
    GPIO.setup(echoPin, GPIO.IN)    #
    GPIO.setup(ledPin, GPIO.OUT)    # Set ledPin's mode is output
    GPIO.output(ledPin, GPIO.LOW)   # Set ledPin low to off led
    
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

def loop():
    GPIO.output(ledPin, GPIO.HIGH)  # led on
    execution = 0
    startTime = time.time()
    iterations = executionTime / pingFreq
    print("Expected iterations " + str(iterations))
    i = 0
    
    while(True):
        i += 1
        distance = getSonar()
        currentTime = time.time()
        print ("The distance at : %.3f is : %.2f cm"%(currentTime, distance))
        f.write(str(round(distance, 2)))
        if(i > iterations):
            f.write("\n")
            print("End event registration " + str(execution))
            execution += 1
            if(execution >= executions):
                GPIO.cleanup()
                print("End program.")
                sys.exit()
            else:
                GPIO.output(ledPin, GPIO.LOW)  # led on
                time.sleep(1)
                GPIO.output(ledPin, GPIO.HIGH)  # led on
                i = 0
        else:
            f.write(",")
        time.sleep(pingFreq)
        
if __name__ == '__main__':     #program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  #when 'Ctrl+C' is pressed, the program will exit
        GPIO.cleanup()         #release resource


    
