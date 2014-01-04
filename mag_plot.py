from __future__ import division, print_function
from visual import *
import wx
import sys
import serial
import re


def stop_plotting(evt) :
    cube.read_mag = False
    cube.ser.close()

def start_plotting(evt) :
    if cube.read_mag == False :
        cube.ser = serial.Serial('/dev/cu.usbserial-A2003EdY', 115200, timeout=1)
        cube.read_mag = True
    
L = 600
# Create a window. Note that w.win is the wxPython "Frame" (the window).
# window.dwidth and window.dheight are the extra width and height of the window
# compared to the display region inside the window. If there is a menu bar,
# there is an additional height taken up, of amount window.menuheight.
w = window(width=2*(L+window.dwidth), height=L+window.dheight+window.menuheight,
           menus=True, title='Widgets')

# Place a 3D display widget in the left half of the window.
d = 20
display(window=w, x=d, y=d, width=L-2*d, height=L-2*d, forward=-vector(0,1,2))
cube = box(color=color.red)
axis_len = 600
x_axis = arrow(pos=(-axis_len,0,0), axis=(2*axis_len,0,0), shaftwidth=1, color = color.red)
y_axis = arrow(pos=(0,-axis_len,0), axis=(0,2*axis_len,0), shaftwidth=1, color = color.green)
z_axis = arrow(pos=(0,0,-axis_len), axis=(0,0,2*axis_len), shaftwidth=1, color = color.yellow)
ball = sphere(pos=(0,0,0), radius=400, opacity=0.5)
# Place buttons, radio buttons, a scrolling text object, and a slider
# in the right half of the window. Positions and sizes are given in
# terms of pixels, and pos(0,0) is the upper left corner of the window.
p = w.panel # Refers to the full region of the window in which to place widgets

wx.StaticText(p, pos=(d,4), size=(L-2*d,d), label='PDH Magnetometer Plot',
              style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)

left = wx.Button(p, label='Stop Plotting', pos=(L+10,15))
left.Bind(wx.EVT_BUTTON, stop_plotting)
right = wx.Button(p, label='Start Plotting', pos=(1.5*L+10,15))
right.Bind(wx.EVT_BUTTON, start_plotting)

# A VPython program that uses these wxPython capabilities should always end
# with an infinite loop containing a rate statement, as future developments
# may require this to keep a display active.


cube.read_mag = True
cube.ser = serial.Serial('/dev/cu.usbserial-A2003EdY', 115200, timeout=1)
mag_point = [0,0,0]
mag_points = []

while True:
    rate(100)
    if ( cube.read_mag == True )  :
        line = cube.ser.readline()
        print(line)
        match = re.match(".*MagRaw: ([-0-9]*)\t([-0-9]*)\t([-0-9]*)",line) 
        if match :
            print("Match:",match.group(1),match.group(2),match.group(3))
            x = int(match.group(1))
            y = int(match.group(2))
            z = int(match.group(3))
            
            mag_point = (x,y,z)
            mag_points.append(mag_point)
            points(pos=mag_points, size=5, color=color.green)                   
        else:
            print("No Match")

    
    
