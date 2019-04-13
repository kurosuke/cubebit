# for 4tronix Cube:Bit 

from rpi_ws281x import *
import time

class Cube:
    def __init__(self, nside, npanel, brightness=30):
        self.nside = nside
        self.npanel = npanel

        self.ndot = self.nside * self.nside
        self.ndot_all = self.ndot * self.npanel
        self.cube = Adafruit_NeoPixel(self.ndot_all, 18, 800000, 5, False, brightness)
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

    def dot(self, x, y, panel, color):

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

        #print("dot {:2d},{:2d},{:2d} = {:2d}".format(x, y, panel, p))
        self.cube.setPixelColor(p + panel*self.ndot, color)

    def clear(self):
        for p in range(self.ndot_all):
            self.cube.setPixelColor(p, 0)
        self.cube.show()


if __name__ == "__main__":

    try:
        cube = Cube(5, 7)

        # set top panel
        color = cube.rgb(0, 9, 10)
        cube.panel(6, color)

        color = cube.rgb(10, 0, 10)
        cube.panel(5, color)

        cube.show()
        time.sleep(3)

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
        time.sleep(10)

    except Exception as ex:
        print (ex)
        print
    finally:
        cube.clear()
