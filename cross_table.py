######################
# micropython script
# Initialisation script for a transmission from a frame buffer to WS2812 strips
# running diagonally back and forth.
# The strip starts at the top left in an upward direction and ends at the bottom right.
# The program logic is mapped via a 8bit frame buffer.
# The dimensions of the rectangular frame can be freely defined.
#######################
# Author:  Weja HoFaLab
# License: CC-BY-NC

import time
from machine import Pin
import array
import framebuf
import neopixel

neopixel_output_pin = 26
####################### frame buffer dimensions ################
width,height = 7,7
########################### number of led's ####################
led_num = width*height
################################################################
screen = framebuf.FrameBuffer(bytearray(led_num),width,height,framebuf.GS8)
stripe = neopixel.NeoPixel(Pin(neopixel_output_pin),led_num)
cross_table = [0]*led_num

## make 240 rainbow RGB colors & 16 grayscale colors
colors = [(0,0,0)]*256 
def make_color_palette():
    colidx=0
    for i in range(80):
        v=i*3
        colors[colidx]=(240-v,0+v,0)
        colidx+=1
    for i in range(80):
        v=i*3
        colors[colidx]=(0,240-v,0+v,)
        colidx+=1
    for i in range(80):
        v=i*3
        colors[colidx]=(0+v,0,240-v)
        colidx+=1
    for i in range(16):
        colidx=240+i
        light=int(225-240/16*i)
        colors[colidx]=(light,light,light)
make_color_palette()

def make_cross_table():
    global cross_table
    dir = 1   #bottom-left to top-right
    xpos,ypos = -1,1
    changedir = False
    for pos in range(led_num):
        xpos = xpos+dir
        ypos = ypos-dir
        if dir == 1:
            if xpos == width:
                changedir = True
                ypos=ypos+2
                xpos = xpos-1
            if ypos == -1:
                changedir = True
                ypos=ypos+1
        else:
            if xpos == -1:
                changedir = True
                xpos = xpos+1
            if ypos == height:
                changedir = True
                ypos=ypos-1
                xpos=xpos+2
        if changedir:
            dir*=-1     # reverse direction
            changedir = False   
        cross_table[(ypos*width)+xpos] = pos       
make_cross_table()
    
def show_screen():
    for y in range(height):
        for x in range(width):
            stripe[cross_table[y*width+x]] = colors[screen.pixel(x,y)]
            #print(screen.pixel(x,y),end=" ") # for debug mode
        #print()                              #     -*-
    stripe.write()

########################## start your program from here #######################

# example
screen.line(0,0,6,6,80) # diagonal green line 
show_screen()
time.sleep(3)
screen.fill(0)          # black
show_screen()
