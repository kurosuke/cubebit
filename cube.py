# for 4tronix Cube:Bit

import sys
import traceback
from rpi_ws281x import *
import time

class Cube:
    def __init__(self, nside, npanel, brightness=30):
        self.nside = nside
        self.npanel = npanel

        self.ndot = self.nside * self.nside
        self.ndot_all = self.ndot * self.npanel
        pinout = 18
        #pinout = 12
        self.cube = Adafruit_NeoPixel(self.ndot_all, pinout, 800000, 5, False, brightness)
        self.cube.begin()
        self.clear()
        self.cube.show()

    def show(self):
        self.cube.show()

    def rgb(self, red, green, blue):
        return ((int(red)<<16) + (int(green)<<8) + blue)

    def panel(self, panel, color):
        for p in range(self.ndot):
            self.cube.setPixelColor(panel*self.ndot+p, color)

    def get_map(self, x, y, panel):

        if panel % 2 == 0:
            #
            # Side-A
            #
            # 20 21 22 23 24
            # 19 18 17 16 15
            # 10 11 12 13 14
            # 09 08 07 06 05
            # 00 01 02 03 04
            if y % 2 == 0:
                p = x + y*self.nside
            else:
                p = (self.nside-x) + (y*self.nside-1)

        else:
            #
            # Side-B
            #
            # 20 19 10 09 00
            # 21 18 11 08 01
            # 22 17 12 07 02
            # 23 16 13 06 03
            # 24 15 11 05 04
            if x % 2 == 0:
                p = 24 - x*self.nside - y
            else:
                p = 24 - (x*self.nside-1) - (self.nside-y)

        return panel*self.ndot + p

    def dot(self, x, y, panel, color):
        p = self.get_map(x, y, panel)

        self.cube.setPixelColor(p, color)

    def clear(self):
        for p in range(self.ndot_all):
            self.cube.setPixelColor(p, 0)
        self.cube.show()

    def darker(self, offset):
        maps = self.cube.getPixels();
        for p in range(self.ndot_all):
            color = maps[p]
            red = color >> 16 & 0xff
            green = color >> 8 & 0xff
            blue = color & 0xff
            if red - offset > 0:
                red -= offset
            if green - offset > 0:
                green -= offset
            if blue - offset > 0:
                blue -= offset
            maps[p] = Color(red, green, blue)
        self.cube.show()

    def rotate(self, dx, dy, dz):
        maps = self.cube.getPixels();

        if dx == 0 and dy == 0 and dz == 0:
            pre = 0
            for z in range(self.npanel):
                for y in range(self.nside):
                    for x in range(self.nside):
                        p = self.get_map(x, y, z)
                        cur = maps[p]
                        maps[p] = pre
                        pre = cur
        elif dx == 1:
            for z in range(self.npanel):
                for y in range(self.nside):
                    pre_color = maps[self.get_map(self.nside-1, y, z)]
                    for x in range(self.nside):
                        cur_p = self.get_map(x, y, z)
                        cur_color = maps[cur_p]
                        maps[cur_p] = pre_color
                        pre_color = cur_color
        elif dy == 1:
            for z in range(self.npanel):
                for x in range(self.nside):
                    pre_color = maps[self.get_map(x, self.nside-1, z)]
                    for y in range(self.nside):
                        cur_p = self.get_map(x, y, z)
                        cur_color = maps[cur_p]
                        maps[cur_p] = pre_color
                        pre_color = cur_color
        elif dz == 1:
            for x in range(self.nside):
                for y in range(self.nside):
                    pre_color = maps[self.get_map(x, y, self.npanel-1)]
                    for z in range(self.npanel):
                        cur_p = self.get_map(x, y, z)
                        cur_color = maps[cur_p]
                        maps[cur_p] = pre_color
                        pre_color = cur_color

if __name__ == "__main__":

    try:
        cube = Cube(5, 7)

        # set top panel
        color = cube.rgb(0, 19, 120)
        cube.panel(6, color)

        color = cube.rgb(10, 100, 10)
        cube.panel(5, color)
        cube.show()
        time.sleep(1)

        for n in range(2):
            cube.darker(1)
            cube.show()
            time.sleep(0.1)

        npanel = cube.npanel
        for z in range(npanel):
            color = cube.rgb(10, 0, 0)
            cube.dot(0, 0, z, color)

        for z in range(npanel):
            color = cube.rgb(0, 20, 0)
            cube.dot(1, 0, z, color)

        for z in range(npanel):
            color = cube.rgb(0, 30, 0)
            cube.dot(2, 0, z, color)

        for z in range(npanel):
            color = cube.rgb(20, 20, 0)
            cube.dot(0, 1, z, color)

        for z in range(npanel):
            color = cube.rgb(20, 0, 0)
            cube.dot(4, 4, z, color)

        cube.show()

        for y in range(10):
            cube.darker(1)
            if y % 2 == 0:
                cube.rotate(1, 0, 0)
            else:
                cube.rotate(0, 1, 0)
            for z in range(7):
                cube.rotate(0, 0, 1)
                cube.show()
                time.sleep(0.1)

    except Exception as e:
        t, v, tb = sys.exc_info()
        print (traceback.format_exception(t, v, tb))
    finally:
        cube.clear()
