import onionGpio

gpio0 = onionGpio.OnionGpio(0)
val = int(gpio0.getValue())
print(val)
