"""
Created by Kshitij Goel

Code to use Rasperry Pi Pico to display Diwali greetings
on 8x8x16 display using MAX7219 module with daisy chain
configuration

"""
from machine import Pin, SPI
import utime
import framebuf
import Matrix8x8Rect.py
import Framebuf_Gallery.py

p25LED = machine.Pin(25,machine.Pin.OUT)

# this code indicates the pico board is working
# blink the onboard LED twice
unit_time = 0.5
for i in range(2):
    p25LED.toggle()
    utime.sleep(0.5)
    p25LED.toggle()
    utime.sleep(0.5)

# HNUM = No of 8x8 matrix block present horizontally
# VNUM = No of 8x8 matrix block present vertically

HNUM = 8
VNUM = 2

pMOSI = machine.Pin(3)
pCLK = machine.Pin(2)
pCS = machine.Pin(5,Pin.OUT)

display = Matrix8x8Rect(SPI(0,sck=pCLK,mosi=pMOSI), pCS, HNUM, VNUM)
display.brightness(2)

mess01 = "Happy Diwali"
mess02 = "Shubh Labh"

max_h_scroll = (len(mess01) + len(mess02)) * 8
max_v_scroll = display.MH * VNUM + 1

while True:
    # Horizontal Scrolling for all icons in 16x16 list 
    for x in range(HNUM*display.MW, -(len(icons16)+1)*16, -1):
         display.fill(0)
         i = 0
         for name in icons16:
             img = framebuf.FrameBuffer(bytearray(icons16[name]), 16, 16, framebuf.MONO_HLSB)
             i = i + 1
             display.blit(img,x + i*16,0)
         display.show()
         utime.sleep(0.05)
    
    # Horizontal Scrolling for all icons in 8x8 list in alternate rows
    for x in range(HNUM*display.MW, -(len(icons8)+1)*8, -1):
         display.fill(0)
         i = 0
         for name in icons8:
             img = framebuf.FrameBuffer(bytearray(icons8[name]), 8, 8, framebuf.MONO_HLSB)
             i = i + 1
             display.blit(img,x + i*9,(i%2)*8)
         display.show()
         utime.sleep(0.05)

    # Horizontal Scrolling for text
    for x in range(HNUM*display.MW, -max_h_scroll, -1):
        display.fill(0)
        display.text(mess01,x + 8,display.MH * 0,1)
        display.text(mess02,x + (len(mess01) + 1)*8, display.MH * 1,1)
        display.show()
        utime.sleep(0.05)

    # Vertical Scrolling for text
    for y in range(VNUM*display.MH, -max_v_scroll, -1):
        display.fill(0)
        display.text("Happy",0,display.MH*0 + y,1)
        display.text(" Diwali",0,display.MH*1 +y,1)
        display.text("Shubh",0,display.MH*2 +y,1)
        display.text(" Labh",0,display.MH*3 +y,1)
        display.show()
        utime.sleep(0.1)
