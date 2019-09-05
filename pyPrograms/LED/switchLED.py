import onionGpio

gpio0 = onionGpio.OnionGpio(18)
val = int(gpio0.getValue())
print(val)
