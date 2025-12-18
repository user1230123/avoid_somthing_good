import pymunk
from blocks import object_type

def collisionTrigger(arbiter, space, data):
    current_scene = data
    shape_a, shape_b = arbiter.shapes
    shape_a: pymunk.Shape
    shape_b: pymunk.Shape

    if shape_a.collision_type == object_type.BALL:
        treatFunc = object_type.collisionTriggerFuncs.get(shape_b.collision_type,lambda a,b,c:True)
        treatFunc:callable
        treatFunc(shape_a,shape_b, space, current_scene)
    elif shape_b.collision_type == object_type.BALL:
        treatFunc = object_type.collisionTriggerFuncs.get(shape_a.collision_type,lambda a,b,c:True)
        treatFunc:callable
        treatFunc(shape_b, shape_a, space, current_scene)
