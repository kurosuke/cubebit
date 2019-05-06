# for 4tronix Cube:Bit 

from cube import *
import time

if __name__ == "__main__":

    points = [
            [ 0, 2, 0],
            [ 0, 2, 1],
            [ 0, 2, 2],
            [ 0, 2, 3],
            [ 0, 2, 4],
            [ 0, 2, 5],
            [ 0, 2, 6],
            [ 1, 2, 6],
            [ 2, 2, 6],
            [ 3, 2, 6],
            [ 4, 2, 6],
            [ 4, 2, 5],
            [ 4, 2, 4],
            [ 4, 2, 3],
            [ 4, 2, 2],
            [ 4, 2, 1],
            [ 4, 2, 0],
            [ 3, 2, 0],
            [ 2, 2, 0],
            [ 1, 2, 0],
            [ 0, 2, 0],
        ]
    try:
        cube = Cube(5, 7)
        cube.clear()

        color = cube.rgb(0, 9, 10)
        color2 = cube.rgb(20, 9, 0)

        while True:
            pre = []
            for p in points:
                cube.dot(p[0], p[1]-2, p[2], color2)
                cube.dot(p[0], p[1]-1, p[2], color-10)
                cube.dot(p[0], p[1], p[2], color)
                cube.dot(p[0], p[1]+1, p[2], color-10)
                cube.dot(p[0], p[1]+2, p[2], color2)
                if len(pre) > 0:
                    cube.dot(pre[0], pre[1]-2, pre[2], 0)
                    cube.dot(pre[0], pre[1]-1, pre[2], 0)
                    cube.dot(pre[0], pre[1], pre[2], 0)
                    cube.dot(pre[0], pre[1]+1, pre[2], 0)
                    cube.dot(pre[0], pre[1]+2, pre[2], 0)

                cube.show()
                time.sleep(0.1)
                pre = p
            time.sleep(1)


    except Exception as ex:
        print (ex)
        print
    finally:
        cube.clear()
