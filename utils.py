import os
import pygame
import pymunk

from components.munk_physics import PhysicsComponent
from object import GameObject

def make_surface(size, color):
    """
    size, color로 surface를 생성합니다.
    """
    surf = pygame.Surface(size)
    surf.fill(color)
    return surf

def seconds_to_frames(seconds: float, fps: int = 60) -> int:
    return int(seconds * int(os.getenv("FPS", fps)))

def imageLoad(*path:str):
    return pygame.image.load(os.path.join("assets",*path))

#정적물체 생성(플랫폼)
#생성할 위치와 이미지이름(예:"example.png"같은)
def makeStaticObject(pos: tuple,imageName: str,size: tuple = None, collisionType = 2):

    static_Object_texture = imageLoad("block_textures", imageName)

    if size is None:
        static_Object_height = static_Object_texture.get_height()
        static_Object_width = static_Object_texture.get_width()
        static_Object_size = (static_Object_width, static_Object_height)
    else:
        static_Object_size = size

    static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    static_body.position = pos
    static_shape = pymunk.Poly.create_box(static_body, static_Object_size)
    static_shape.collision_type = collisionType

    staticObject = GameObject(pos,static_Object_size,static_Object_texture)

    static_shape.user_data = staticObject
    
    staticObject.add_component(PhysicsComponent(static_body,static_shape))
    return staticObject