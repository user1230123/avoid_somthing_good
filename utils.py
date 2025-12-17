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

#정적물체 생성(플랫폼)
#생성할 위치와 이미지이름(예:"example.png"같은)
def makeStaticObject(pos: tuple,size: tuple,imageName: str):

    static_Object_texture = pygame.image.load(os.path.join("assets","textures", imageName))
    static_Object_height = static_Object_texture.get_height()
    static_Object_width = static_Object_texture.get_width()
    static_Object_size = (static_Object_width, static_Object_height)
    static_Object_size = size

    static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    static_shape = pymunk.Poly.create_box(static_body, static_Object_size)
    static_shape.collision_type = 2

    staticObject = GameObject(pos,static_Object_size,static_Object_texture)

    static_shape.user_data = staticObject
    
    staticObject.add_component(PhysicsComponent(static_body,static_shape))
    return staticObject