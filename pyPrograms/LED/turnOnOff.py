import onionGpio 
import sys

gpio1 = onionGpio.OnionGpio(11)
gpio1.setOutputDirection()

val = int(sys.argv[1])

if (val == 1):
	print(2)
	gpio1.setValue(1)
else:
	print(3)
	gpio1.setValue(0)
#gpio1.setValue(val)
