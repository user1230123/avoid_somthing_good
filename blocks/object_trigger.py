import pygame
import pymunk
from components.munk_physics import PhysicsComponent
from object import GameObject
import settings
import utils

def ball_jump_func(ball_shape:pymunk.Shape, block_shape:pymunk.Shape, space:pymunk.space, scene, forCheckOnly=False):
    ball_pos = ball_shape.body.position
    blockVertices = [v.x for v in block_shape.get_vertices()]
    blockMaxX = max(blockVertices) + block_shape.body.position.x
    blockMinX = min(blockVertices) + block_shape.body.position.x

    if blockMaxX > ball_pos.x-settings.BALL_RADIUS+settings.BALL_JUMP_CORRECTION and blockMaxX < ball_pos.x+settings.BALL_RADIUS+settings.BALL_JUMP_CORRECTION:
        print("IN BLOCK X RANGE")
        if ball_jump_func_sub(ball_shape, block_shape, space, forCheckOnly):
            return True

    if blockMaxX < ball_pos.x-settings.BALL_RADIUS+settings.BALL_JUMP_CORRECTION and blockMaxX > ball_pos.x+settings.BALL_RADIUS+settings.BALL_JUMP_CORRECTION:
        print("IN BLOCK X RANGE")
        if ball_jump_func_sub(ball_shape, block_shape, space, forCheckOnly):
            return True

    if blockMinX < ball_pos.x < blockMaxX:
        print("IN BLOCK X RANGE")
        if ball_jump_func_sub(ball_shape, block_shape, space, forCheckOnly):
            return True
        
    return False

def ball_jump_func_sub(ball_shape:pymunk.Shape, block_shape:pymunk.Shape, space:pymunk.space, forCheckOnly=False):
    ball_pos = ball_shape.body.position
    block_pos = block_shape.body.position
    dotY = [v.y for v in block_shape.get_vertices()]
    blockMaxY = max(dotY) + block_pos.y
    blockMinY = min(dotY) + block_pos.y

    if space.gravity.y > 0:
        print("UP")
        if ball_pos.y < blockMaxY:
            if forCheckOnly:
                return True
            ball_shape.body.velocity = (ball_shape.body.velocity.x, -settings.BALL_JUMP_POWER)
            return True
    else:
        print("DOWN")
        if ball_pos.y > blockMinY:
            if forCheckOnly:
                return True
            ball_shape.body.velocity = (ball_shape.body.velocity.x, settings.BALL_JUMP_POWER)
            return True
    return False

def platform_block_func(ball_shape:pymunk.Shape, block_shape:pymunk.Shape, space:pymunk.space, scene):
    ball_jump_func(ball_shape, block_shape, space, scene)

def spike_block_func(ball_shape:pymunk.Shape, block_shape:pymunk.Shape, space:pymunk.space, scene):
    scene.manager.remove_scene_to_render(scene.__class__.__name__)
    scene.manager.add_scene_to_render('GameOverScene')

def elevator_block_func(ball_shape:pymunk.Shape, block_shape:pymunk.Shape, space:pymunk.space, scene):
    #이미 리스폰 중이면 무시
    obj = getattr(block_shape, "user_data", None)
    obj:GameObject
    if obj is None:
        return

    if getattr(obj, "respawning", 0):
        return
    
    print("ELEVATOR BLOCK TRIGGERED")

    if ball_jump_func(ball_shape, block_shape, space, scene):
        if not hasattr(obj, "_max_uses"):
            obj._max_uses = getattr(obj, "max_uses", 5)
        if not hasattr(obj, "_remaining_uses"):
            obj._remaining_uses = obj._max_uses

        obj._remaining_uses -= 1

        if obj._remaining_uses >= 0:

            new_pos = (block_shape.body.position.x, block_shape.body.position.y - settings.BLOCK_SIZE[1])
            total_frames = utils.seconds_to_frames(0.2)
            obj.respawning = total_frames

            # 위치 변경 콜백
            def teleport(space, data):
                body, pos, shape = data
                body.position = pos

                space.reindex_shape(shape)
            
            space.add_post_step_callback(teleport, (block_shape.body, new_pos, block_shape))

            physics_comp = obj.get_component(PhysicsComponent)
            if physics_comp:
                physics_comp.remove_from_space(space)

def gravity_block_func(ball_shape:pymunk.Shape, block_shape:pymunk.Shape, space:pymunk.space, scene):
    if ball_jump_func(ball_shape, block_shape, space, scene, forCheckOnly=True):
        objects = scene.objects

        for obj in objects:
            obj:GameObject
            physics_comp = obj.get_component(PhysicsComponent)
            physics_comp:PhysicsComponent
            
            if physics_comp:
                if physics_comp.shape.collision_type == 5: # object_type.GRAVITY_BLOCK
                    if space.gravity.y > 0:
                        obj.texture = pygame.transform.scale(utils.image_load(*settings.GRAVITY_BLOCK_TEXTURE_TUPLE[1]), obj.size)
                    else:
                        obj.texture = pygame.transform.scale(utils.image_load(*settings.GRAVITY_BLOCK_TEXTURE_TUPLE[0]), obj.size)

        if space.gravity.y > 0:
            space.gravity = (0, -900)
        else:
            space.gravity = (0, 900)

def complete_block_func(ball_shape:pymunk.Shape, block_shape:pymunk.Shape, space:pymunk.space, scene):
    scene.manager.remove_scene_to_render(scene.__class__.__name__)
    scene.manager.add_scene_to_render('GameStage',None,utils.get_next_map_sequence(scene.map_class))

def jump_block_func(ball_shape:pymunk.Shape, block_shape:pymunk.Shape, space:pymunk.space, scene):
    if ball_jump_func(ball_shape, block_shape, space, scene, forCheckOnly=True):
        ball_shape.body.velocity = (ball_shape.body.velocity.x, -settings.BALL_JUMP_POWER * 1.5)
