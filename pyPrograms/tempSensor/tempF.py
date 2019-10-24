import oneWire
from temperatureSensor import TemperatureSensor

# default address of i2c backpack is 0x3f by default
lcdAddress = 0x3f
# setup one wire temp sensor object
oneWireGpio = 19
pollingInterval = 1 #seconds

# function to read the temp fron the one-wire temp sensore
def getTemp():
    # check if 1-Wire was setup in the kernel
    if not oneWire.setupOneWire(str(oneWireGpio)):
        print "Kernel module could not be inserted. Please reboot and try again."
        return -1
    # get the address of the temp sensor
    # it should be the only device connected to this experiment
    sensorAddress = oneWire.scanOneAddress()

    sensor = TemperatureSensor("oneWire", { "address": sensorAddress, "gpio": oneWireGpio })
    if not sensor.ready:
        print "Sensor was not set up correctly. Please make sure that your sensor is firmly connected to the GPIO specified above and try again."
        return -1

    return sensor.readValue()

def __main__():
    t = getTemp()
    #t is in Celsius, F for Fahrenheit
    F = (t * (9.0/5)) + 32
    print(F)
if __name__ == '__main__':
    __main__()
