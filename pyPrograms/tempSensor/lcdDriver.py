from OmegaExpansion import onionI2C
import time

# sleep durations
writeSleep = 0.0001 # 1 millisecond
initSleep = 0.2

## LCD Display commands
# commands
lcdClearDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

En = 0b00000100 # Enable bit
Rw = 0b00000010 # Read/Write bit
Rs = 0b00000001 # Register select bit

class Lcd:
    #initialzies objects and lcd
    def __init__(self,address,port=0):
        self.address = address
        self.i2c = onionI2C.OnionI2C(port)

        # lcd defaults


        self.lcdbacklight = LCD_BACKLIGHT #default status
        self.line1= "";
        self.line2= "";
        self.line3= "";
        self.line4= "";

        self.lcdWrite(0x03)
        self.lcdWrite(0x03)
        self.lcdWrite(0x03)
        self.lcdWrite(0x02)

        self.lcdWrite(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
        self.lcdWrite(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
        self.lcdWrite(lcdClearDISPLAY)
        self.lcdWrite(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
        time.sleep(initSleep)

    #function to write byte to the screen via I2C
    def writeBytesToLcd(self, cmd):
        self.i2c.write(self.address, [cmd])
        time.sleep(writeSleep)

    # creates an EN pulse (using I2C) to latch previously sent command
    def lcdStrobe(self, data):
        self.writeBytesToLcd(data | En | self.lcdbacklight)
        time.sleep(.0005)
        self.writeBytesToLcd(((data & ~ En) | self.lcdbacklight))
        time.sleep(.0001)
    def lcdWriteFourBits(self, data):
        # write four data bits along with backlight state to the screen
        self.writeBytesToLcd(data | self.lcdbacklight)
        # perform strobe to latch the data we just sent
        self.lcdStrobe(data)

    # function to write an 8-bit command to lcd
    def lcdWrite(self, cmd, mode=0):
        # due to how the I2C backpack expects data, we need to send the top four and bottom four bits of the command separately
        self.lcdWriteFourBits(mode | (cmd & 0xF0))
        self.lcdWriteFourBits(mode | ((cmd << 4) & 0xF0))
    
    def lcdDisplayString(self, string, line):
        if line == 1:
            self.line1 = string;
            self.lcdWrite(0x80)
        if line == 2:
            self.line2 = string;
            self.lcdWrite(0xC0)
        if line == 3:
            self.line3 = string;
            self.lcdWrite(0x94)
        if line == 4:
            self.line4 = string;
            self.lcdWrite(0xD4)
        for char in string:
            self.lcdWrite(ord(char), Rs)
    def lcdDisplayStringList(self, strings):
        for x in range(0, min(len(strings), 4)):
            self.lcdDisplayString(strings[x], x+1)
    #clear lcd and set to home
    def lcdClear(self):
        self.lcdWrite(lcdClearDISPLAY)
        self.lcdWrite(LCD_RETURNHOME)
    #write the current lines to the screen
    def refresh(self):
        self.lcdDisplayString(self.line1,1)
        self.lcdDisplayString(self.line2,2)
        self.lcdDisplayString(self.line3,3)
        self.lcdDisplayString(self.line4,4)

    #turn on the backlight
    def backlightOn(self):
        self.lcdbacklight = LCD_BACKLIGHT
        self.refresh()
    def backlightOff(self):
        self.lcdbacklight = LCD_NOBACKLIGHT
        self.refresh()

