"""
Created by Kshitij Goel

I have used some base code from
https://github.com/mcauser/micropython-max7219/blob/master/max7219.py

This is MicroPython max7219 cascadable 8x8 LED matrix driver
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

# -Subclassing FrameBuffer provides support for graphics primitives
# -Class to support daisy chain of 8x8 matrix connected on MAX7219

class Matrix8x8Rect(framebuf.FrameBuffer):
    # -hnum represents number of 8x8 matrix block present horizontally
    # -vnum represents number of 8x8 matrix block present vertically (you can think them as pages)
    # Assuming all 8x8 pixel blocks are connected in a single daisey chain
    
    def __init__(self, spi, cs, hnum = 1,vnum = 1):

        self.spi = spi
        self.cs = cs
        self.cs.init(cs.OUT, True)
        self.hnum = hnum
        self.vnum = vnum
        self.num = hnum * vnum			# Total number of MAX7219 Modules 
        self.MH = 8						# matrix height
        self.MW = 8						# matrix Width
        self.buffer = bytearray(self.MH * self.num)
        
        super().__init__(self.buffer, self.MW * hnum, self.MH * vnum, framebuf.MONO_HLSB)
        self.init()

    # this _write method replays a sigle command number of times MAX7219 chip is present
    def _write(self, command, data):
        self.cs(0)
        for m in range(self.num):
            self.spi.write(bytearray([command, data]))
        self.cs(1)

    # It initialise the MAX7219 for several commands in this list
    # I have no idea from where these came
    def init(self):
        for command, data in (
            (_SHUTDOWN, 0),
            (_DISPLAYTEST, 0),
            (_SCANLIMIT, 7),
            (_DECODEMODE, 0),
            (_SHUTDOWN, 1),
        ):
            self._write(command, data)

    # it adjust the brightess of all modules in cascade
    def brightness(self, value):
        if not 0 <= value <= 15:
            raise ValueError("Brightness out of range")
        self._write(_INTENSITY, value)

    # -This method paints the pixels from the buffer attributte on the SPI device
    # -I have modified the show method for the daisy chain of 8x8x4 blocks for dot matrix on MAX7219
    def show(self):
        # loop for each line in matrix height
        for y in range(self.MH):
            self.cs(0)
            
            # -loop for each vertical block (or pages)
            for v in range(self.vnum):

                # loop for each horizontal block
                for h in range(self.hnum):
                    p = (v * self.hnum * self.MH) + h + (y * self.hnum)
                    # this line is the heart of MAX7219 driver
                    # we are writing two bytes
                    # first one tells the location
                    # second one tells the pixel map in a single byte form
                    # I think each pixel map is cascaded down to the far left chip
                    self.spi.write(bytearray([_DIGIT0 + y, self.buffer[p]])) 
            self.cs(1)