import numpy as np
import math
import time

from rtengine import Engine
from geo_objects import v_init, Rectangle, RectPrism, Vector

if __name__ == "__main__":

    """
    Simple script which generates my github logo
    Pretty much hard coded coordinates for shape primatives
    Also runs the raytracing and displays the image
    """

    ENGINE = Engine(v_init(38, -26, -70), v_init(-1.6, -0.1, -1), math.pi * 0.6, 200, 200)

    white_wall = Rectangle(v_init(-100, -100, -100), v_init(0, 300, 0), v_init(0, 0, 200), np.array([255, 255, 255]))
    blue_wall = Rectangle(v_init(-100, -100, -100), v_init(300, 0, 0), v_init(0, 300, 0), np.array([22, 24, 138]))
    grass = Rectangle(v_init(-100, -100, -100), v_init(300, 0, 0), v_init(0, 0, 200), np.array([22, 77, 17]))

    light1 = Rectangle(v_init(200, -100, -100), v_init(0, 300, 0), v_init(0, 0, 200), np.array([235, 128, 52]), True)
    light2 = Rectangle(v_init(-100, -100, 100), v_init(300, 0, 0), v_init(0, 300, 0), np.array([51, 48, 95]), True)
    light3 = Rectangle(v_init(-100, 200, -100), v_init(300, 0, 0), v_init(0, 0, 200), np.array([51, 48, 95]), True)

    h_init = v_init(20, -35, -82)
    h1 = RectPrism(h_init, v_init(-4, 0, 0), v_init(0, 20, 0), v_init(0, 0, -4),  np.array([1880, 1024, 416]), True)
    h2 = RectPrism(Vector(h_init.v + np.array([0, 8, -4])), v_init(-4, 0, 0), v_init(0, 4, 0), v_init(0, 0, -6),  np.array([1880, 1024, 416]), True)
    h3 = RectPrism(Vector(h_init.v + np.array([0, 0, -10])), v_init(-4, 0, 0), v_init(0, 20, 0), v_init(0, 0, -4),  np.array([1880, 1024, 416]), True)

    b_init = v_init(20, -35, -64)
    b1 = RectPrism(b_init, v_init(-4, 0, 0), v_init(0, 20, 0), v_init(0, 0, -4),  np.array([1880, 1024, 416]), True)
    b2 = RectPrism(Vector(b_init.v + np.array([0, 0, -4])), v_init(-4, 0, 0), v_init(0, 3, -10), v_init(0, 3.66972, 1.10092),  np.array([1880, 1024, 416]), True)
    b3 = RectPrism(Vector(b_init.v + np.array([0, 12, -4])), v_init(-4, 0, 0), v_init(0, -4, -10), v_init(0, -3.44828, 1.37931),  np.array([1880, 1024, 416]), True)

    # np.array([235, 128, 52])
    ENGINE.scene.append(white_wall)
    ENGINE.scene.append(blue_wall)
    ENGINE.scene.append(grass)
    ENGINE.scene.append(light1)
    ENGINE.scene.append(light2)
    ENGINE.scene.append(light3)
    ENGINE.scene.append(h1)
    ENGINE.scene.append(h2)
    ENGINE.scene.append(h3)
    ENGINE.scene.append(b1)
    ENGINE.scene.append(b2)
    ENGINE.scene.append(b3)

    start = time.time()


    ENGINE.cast_rays(30, 10, True, 0.9)
    ENGINE.render()

    print(time.time() - start)