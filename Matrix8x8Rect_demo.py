"""
Created by Kshitij Goel

Demo code to use Rasperry Pi Pico to display information
on 8x8x16 display using MAX7219 module with daisy chain
configuration

"""
from machine import Pin, SPI
import utime
import framebuf
from Matrix8x8Rect import Matrix8x8Rect

HNUM = 8	# HNUM = No of 8x8 matrix block present horizontally
VNUM = 1	# VNUM = No of 8x8 matrix block present vertically

pMOSI = machine.Pin(3)
pCLK = machine.Pin(2)
pCS = machine.Pin(5,Pin.OUT)

display = Matrix8x8Rect(SPI(0,sck=pCLK,mosi=pMOSI), pCS, HNUM, VNUM)
display.brightness(2)

mess01 = "1234ABCD"
max_h_scroll = (len(mess01)) * 8
max_v_scroll = display.MH * VNUM + 1

while True:
    # Horizontal Scrolling for text
    for x in range(HNUM*display.MW, -max_h_scroll, -1):
        display.fill(0)
        display.text(mess01,x + 8,display.MH * 0,1)
        display.show()
        utime.sleep(0.1)

    # Vertical Scrolling for text
    for y in range(VNUM*display.MH, -max_v_scroll, -1):
        display.fill(0)
        display.text("1234",0,display.MH*0 + y,1)
        display.text("ABCD",display.MW*4,display.MH*1 +y,1)
        display.show()
        utime.sleep(0.1)
