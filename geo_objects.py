import numpy as np
import math

def v_init(x, y, z):
    return Vector(np.array([x, y, z]))

class Vector():

    """
    3D Vector implementaion required for the ray tracing engine
    """

    def __init__(self, v):
        self.v = v

    def dot(self, vec):
        return np.sum(self.v * vec.v)

    def cross(self, vec):
        return Vector(np.array([self.v[1] * vec.v[2] - self.v[2] * vec.v[1],
                                self.v[2] * vec.v[0] - self.v[0] * vec.v[2],
                                self.v[0] * vec.v[1] - self.v[1] * vec.v[0]]))
    
    def magsq(self):
        return np.sum(self.v ** 2)
    
    def normalize(self):
        return Vector(self.v / math.sqrt(self.magsq()))
    
class Ray():

    """
    'origin' and 'direction'
    """

    def __init__(self, o, d):
        self.o = o
        self.d = d.normalize()

def random_unit_vector():
    while True:
        p = Vector(np.random.uniform(-1, 1, 3))
        if p.dot(p) < 1.0:
            return p.normalize()

class Rectangle():

    """
    Rectangle in 3D space represented by a point and two direction vectors
    """
    
    def __init__(self, p, u, v, color=np.array([0, 0, 0]), is_light=False):
        self.p = p
        self.u = u
        self.v = v
        self.color = color
        self.is_light = is_light

    def get_t(self, ray):
        n = self.u.cross(self.v)
        dn = ray.d.dot(n)
        if dn == 0:
            return -1, n
        return Vector((self.p.v - ray.o.v)).dot(n) / dn, n
    
    def intersect(self, ray, diffuse=False):
        t, n = self.get_t(ray)
        if t < 0:
            return float("inf"), None
        phit = ray.o.v + ray.d.v * t
        w = Vector(phit - self.p.v)

        s = w.dot(self.u) / self.u.magsq()
        tp = w.dot(self.v) / self.v.magsq()

        if s < 0 or tp < 0 or s > 1 or tp > 1:
            return float("inf"), None
        
        nn = n.normalize()
        if nn.dot(ray.d) > 0:
            nn = Vector(nn.v * -1)
        if diffuse:
            scatter_dir = nn.v + random_unit_vector().v
            if np.linalg.norm(scatter_dir) < 1e-6:
                scatter_dir = nn
            return t, Ray(Vector(phit), Vector(scatter_dir).normalize())

        dn = ray.d.normalize()
        return t, Ray(Vector(phit), Vector(dn.v - nn.v * 2 * dn.dot(nn)))

class RectPrism():

    """
    Rectangular prism in 3D space represented by a point and 3 direction vectors
    Essentially built using 6 rectangles
    """

    def __init__(self, p, u, v, w, color=np.array([0, 0, 0]), is_light=False):
        self.p = p
        self.u = u
        self.v = v
        self.w = w
        self.color = color
        self.is_light = is_light
        self.faces = (Rectangle(p, u, v, color, is_light),
                      Rectangle(p, v, w, color, is_light),
                      Rectangle(p, u, w, color, is_light),
                      Rectangle(Vector(p.v + u.v), v, w, color, is_light),
                      Rectangle(Vector(p.v + v.v), u, w, color, is_light),
                      Rectangle(Vector(p.v + w.v), u, v, color, is_light))
        
    def intersect(self, ray, diffuse=False):
        best_t = float("inf")
        best_r = None
        for f in self.faces:
            t, r = f.intersect(ray, diffuse)
            if r and t < best_t:
                best_t = t
                best_r = r
        return best_t, best_r