import os
import pygame
import pymunk

from components.munk_physics import PhysicsComponent
from object import GameObject
import settings

def make_surface(size, color):
    """
    size, color로 surface를 생성합니다.
    """
    surf = pygame.Surface(size)
    surf.fill(color)
    return surf

def seconds_to_frames(seconds: float, fps: int = 60) -> int:
    return int(seconds * int(os.getenv("FPS", fps)))

def image_load(*path:str):
    return pygame.image.load(os.path.join("assets",*path))

#정적물체 생성(플랫폼)
#생성할 위치와 이미지이름(예:"example.png"같은)
def make_static_object(pos: tuple, imageName: str, collisionType = 2, size: tuple = settings.BLOCK_SIZE): # (object_type.PLATFORM = 2)

    static_Object_texture = image_load("block_textures", imageName)

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

    static_object = GameObject(pos,static_Object_size,static_Object_texture)

    static_shape.user_data = static_object
    
    static_object.add_component(PhysicsComponent(static_body,static_shape))
    return static_object

def pos_by_one_block(pos_for_one_block_x, pos_for_one_block_y):
    """
    실제 오브젝트 위치를 블록 인덱스로 변환합니다.
    """
    x_index = int((pos_for_one_block_x - 0.5) * settings.BLOCK_SIZE[0])
    y_index = int((settings.SCREEN_BLOCK_SIZE[1] - pos_for_one_block_y + 0.5) * settings.BLOCK_SIZE[1])
    return (x_index, y_index)