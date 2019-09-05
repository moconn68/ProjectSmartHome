import onionGpio 
import sys

gpio1 = onionGpio.OnionGpio(1)
gpio1.setOutputDirection()

val = sys.argv[1]
print(val)
gpio1.setValue(val)
