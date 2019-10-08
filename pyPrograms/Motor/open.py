from motors import Servo
import time

def main():
    # instantiate objects for the two servos
    standardServo = Servo(0, 500, 2400)
    microServo = Servo(1, 500, 2400);

    # set both servos to the neutral position
    standardServo.setAngle(90.0)
    microServo.setAngle(90.0)
    time.sleep(2)

    # infinite loop
    if(True): #Dom made a comment here
        # Turn servos to the 0 angle position
        standardServo.setAngle(0.0)
        microServo.setAngle(0.0)
        time.sleep(2)
        # Turn servos to the neutral position
	#standardServo.setAngle(90.0)
        #microServo.setAngle(90.0)
        #time.sleep(2)
        # Turn servos to the 180 angle position
        #standardServo.setAngle(180.0)
        #microServo.setAngle(180.0)
        #time.sleep(2)

if __name__ == '__main__':
    main()
