# for 4tronix Cube:Bit 

from cube import *
import time

if __name__ == "__main__":

    try:
        cube = Cube(5, 7)
        cube.clear()

        while True:
            for n in range(220):
                for z in range(7):
                    color1 = cube.rgb(0, 9, 255-n)
                    color2 = cube.rgb((n*2+20)%255, n+9, 0)
                    color3 = cube.rgb(50, (n*2+20)%100, 50)
                    cube.dot(1, 1, z, color1)
                    cube.dot(2, 1, z, color1)
                    cube.dot(3, 1, z, color1)
                    cube.dot(1, 3, z, color1)
                    cube.dot(2, 3, z, color1)
                    cube.dot(3, 3, z, color1)
                    cube.dot(2, 2, z, color2)

                    cube.dot(0, 0, z, color3)
                    cube.dot(0, 4, z, color3)
                    cube.dot(4, 0, z, color3)
                    cube.dot(4, 4, z, color3)

                time.sleep(0.01)
                cube.show()
            time.sleep(1)


    except Exception as ex:
        print (ex)
        print
    finally:
        cube.clear()
