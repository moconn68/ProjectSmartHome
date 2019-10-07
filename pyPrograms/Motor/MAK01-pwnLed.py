from motors import OmegaPwm
import math
import time

# define constants
PWM_FREQUENCY = 1000
sleepTime = 0.005

# apply sine to the input radian value
#    ensure that it
def calcDutyCycle(rad):
    result = 50.0*(math.sin(rad)) + 50.0
    if(result > 100.0):
        result = 100.0
    if(result < 0.0):
        result = 0.0
    return result

# main function
def main():
    # construct an array of OmegaPwm objects
    ledObjectArray = []     # create an empty array
    for i in range(16):
        # instantiate an object tied to the i channel on the PWM Expansion
        obj = OmegaPwm(i, PWM_FREQUENCY)
        # add the object into our array of objects
        ledObjectArray.append(obj)

    # define the phase difference (in radians) between each channel
    channelIncrement = (2 * math.pi)/16
    # define the phase difference (in radians) for each
    phaseIncrement = (2 * math.pi)/160
    
    # counters for frames and duty cycles in the LED animation
    loopCount = 0
    duty = 0
    
    # infinite loop
    while(True):
        # loop through each of the LED PWM Channels
        for index,element in enumerate(ledObjectArray):
            # calculate the duty cycle for the channel using a sine function
            #   the input to the duty cycle calculation consists of the sum of two numbers, one fixed and one changing:
            #   - multiplying channelIncrement by the PWM channel index - fixed for each channel
            #   - multiplying phaseIncrement by the loop count - changing
            duty = calcDutyCycle(( (index) * channelIncrement ) + (loopCount * phaseIncrement))
            element.setDutyCycle(duty)
        # increment the loop count and ensure it doesn't go over 160
        loopCount += 1
        loopCount = loopCount % 160
        # add a small delay for the visual effect
        time.sleep(sleepTime)

if __name__ == '__main__':
    main()
