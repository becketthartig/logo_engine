## Custom Made Ray Tracing Engine

Simple ray tracing engine built exclusively for fun to render my github logo.
After creating an Engine object, you can append objects defined in geo_objects.py to the scene.
Simply to see a black wall:

```
from rtengine import Engine
from geo_objects import v_init, Rectangle

Engine = Engine(v_init(0, 0, 0), v_init(1, 0, 0))
Engine.scene.append(Rectangle(v_init(100, -100, -100), v_init(0, 200, 0), v_init(0, 0, 200)))
```

Then to do the raytracing and view the final image we have the following [30 samples per pixel, 10 reflections per ray, diffuse=True, minimal energy loss (0 max, 1 minimal)]:
```
Engine.cast_rays(30, 10, True, 0.9)
Engine.render()
```