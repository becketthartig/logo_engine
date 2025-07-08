import numpy as np
import math
from PIL import Image

from geo_objects import Vector, v_init, Ray

class Engine():

    """
    
    Ray tracing engine for very simple renders
    Currently does not save images, only displays them however easy to change

    o:  Vector          camera origin
    d:  Vector          camera direction
    a:  float           apeture
    w:  int             image width
    h:  int             image height
    etc...

    """

    def __init__(self, o, d, a=math.pi / 2, w=100, h=75, background_color=np.array([2, 2, 3])):
        self.o = o
        self.d = d.normalize()
        self.a = a
        self.w = w
        self.h = h
        self.background_color = background_color
        self.framebuffer = np.zeros((h, w, 3), dtype=np.uint8)
        self.scene = []

    def cast(self, ray, reflections=0, diffuse=False, energy_loss=1):
        ray.o = Vector(ray.o.v + ray.d.v * 0.0001)
        best_t = float("inf")
        best_r = None
        best_color = None
        best_is_light = False
        for s in self.scene:
            t, r = s.intersect(ray, diffuse)
            if r and t < best_t:
                best_t = t
                best_r = r
                best_color = s.color
                best_is_light = s.is_light
        if not best_r:
            return self.background_color / 255
        if reflections == 10 and best_is_light:
            return best_color / 255 / 8
        if reflections <= 0 or best_is_light:
            return best_color / 255
        return best_color / 255 * self.cast(best_r, reflections - 1) * energy_loss

    def cast_rays(self, samples, reflections=0, diffuse=False, energy_loss=1):
        aspect = self.w / self.h
        x_max = math.tan(self.a / 2)
        y_max = x_max / aspect

        r = self.d.cross(v_init(0, 1, 0)).normalize()
        u = r.cross(self.d).normalize()

        count = 0
        for j in range(self.h):
            for i in range(self.w):
                count += 1
                if count % 1000 == 0:
                    print("Pixel", count)

                starting_col = np.array([0.0, 0.0, 0.0])
                
                for _ in range(samples):

                    u_scalar = (i + 0.5) / self.w
                    v_scalar = (j + 0.5) / self.h

                    x = (2 * u_scalar - 1) * x_max
                    y = (1 - 2 * v_scalar) * y_max
                    pixel_dir = Vector(self.d.v + r.v * x + u.v * y).normalize()

                    color = np.power(np.clip(self.cast(Ray(self.o, pixel_dir), reflections, diffuse, energy_loss), 0.0, 1.0), 0.45454545)
                    starting_col = starting_col + (color * 255).astype(np.uint8)



                self.framebuffer[j, i] = starting_col / samples

    def render(self, path="output.png"):
        image = Image.fromarray(self.framebuffer, "RGB")
        # image.save(path)
        image.show()