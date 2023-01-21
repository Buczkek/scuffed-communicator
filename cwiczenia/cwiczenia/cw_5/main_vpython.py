from vpython import *

scene.center = vector(2, 2, 0)
scene.forward = vector(1, 1, -1) 
scene.up = vector(1, 1, 1)
scene.width = 1800
scene.height = 850


lamp = local_light(pos=vector(10, 10, 10), color=color.red)

w1 = box(pos=vector(0, 0, 0),
         size=vector(4, 4, 0.1),
         color=color.red)

w2 = box(pos=vector(0, 2, 2),
         size=vector(4, 0.1, 4),
         color=color.blue)
w3 = box(pos=vector(2, 0, 2),
         size=vector(0.1, 4, 4),
         texture=textures.flower)


"""rod = cylinder(pos=vector(0, 2, 1),
               axis=vector(5, 0, 0),
               radius=1)

rod.color = vector(0.5, 0.5, 0)
"""
