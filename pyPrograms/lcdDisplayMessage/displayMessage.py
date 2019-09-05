import lcdDriver
import sys

#set default address
lcdAddress = 0x3f
def display(inp):
    #setup LCD
    lcd = lcdDriver.Lcd(lcdAddress)
    lcd.backlightOn()
    lcd.lcdDisplayStringList(["Your message is:  ",inp])
def __main__():
    output = ""
    for x in range(1,len(sys.argv)):
        output += sys.argv[x] + " "
    display(output)
    print(output)
if __name__ == "__main__":
    __main__()

    
