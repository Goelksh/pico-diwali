"""
Created by Kshitij Goel 
I have used some base code from

https://github.com/mcauser/micropython-max7219/blob/master/max7219.py
MicroPython max7219 cascadable 8x8 LED matrix driver
"""

from micropython import const
import framebuf

_NOOP = const(0)
_DIGIT0 = const(1)
_DECODEMODE = const(9)
_INTENSITY = const(10)
_SCANLIMIT = const(11)
_SHUTDOWN = const(12)
_DISPLAYTEST = const(15)

# Subclassing FrameBuffer provides support for graphics primitives
# Class to support daisy chain of 8x8 matrix connected on MAX7219

class Matrix8x8Rect(framebuf.FrameBuffer):
    # hnum represents number of 8x8 matrix block present horizontally
    # Vnum represents number of 8x8 matrix block present vertically (you can think them as pages)
    # Assuming all 8x8 pixel blocks are connected in a single daisey chain
    
    def __init__(self, spi, cs, hnum = 1,vnum = 1):

        self.spi = spi
        self.cs = cs
        self.cs.init(cs.OUT, True)
        self.hnum = hnum
        self.vnum = vnum
        self.num = hnum * vnum
        self.MH = 8										# matrix height
        self.MW = 8										# matrix Width
        self.buffer = bytearray(self.MH * self.num)
        
        super().__init__(self.buffer, self.MW * hnum, self.MH * vnum, framebuf.MONO_HLSB)
        self.init()

    def _write(self, command, data):
        self.cs(0)
        for m in range(self.num):
            self.spi.write(bytearray([command, data]))
        self.cs(1)

    def init(self):
        for command, data in (
            (_SHUTDOWN, 0),
            (_DISPLAYTEST, 0),
            (_SCANLIMIT, 7),
            (_DECODEMODE, 0),
            (_SHUTDOWN, 1),
        ):
            self._write(command, data)

    def brightness(self, value):
        if not 0 <= value <= 15:
            raise ValueError("Brightness out of range")
        self._write(_INTENSITY, value)

    # customised the show function for the daisy chain of 8x8x4 blocks for dot matrix on MAX7219
    def show(self):
        # loop for each line in matrix height
        for y in range(self.MH):
            self.cs(0)
            
            # loop for each vertical block (or pages)
            for v in range(self.vnum):

                # loop for each horizontal block
                for h in range(self.hnum):
                    p = (v * self.hnum * self.MH) + h + (y * self.hnum)
                    self.spi.write(bytearray([_DIGIT0 + y, self.buffer[p]])) 
            self.cs(1)
            

# ##########################################################
# # How to use this class
# ###########################################################
# HNUM = 4
# VNUM = 1
# 
# pMOSI = machine.Pin(3)
# pCLK = machine.Pin(2)
# pCS = machine.Pin(5,Pin.OUT)
# 
# display = Matrix8x8(SPI(0,sck=pCLK,mosi=pMOSI), pCS, HNUM, VNUM)
# display.brightness(2)
# display.text("Happy Diwali")
# display.show()
# utime.sleep(5)
# # display a diya on 8x8 grid at position 0,0
# display.blit(framebuf.FrameBuffer(bytearray([0x10,0x08,0x10,0x08,0x91,0x81,0x42,0x3c]), 8, 8, framebuf.MONO_HLSB),0,0)
# display.show()
############################################################
