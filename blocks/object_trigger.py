import pymunk
from components.munk_physics import PhysicsComponent
from object import GameObject
import utils

def platformBlockFunc(ball_shape:pymunk.Shape, block_shape:pymunk.Shape, space:pymunk.space, scene):
    ball_pos = ball_shape.body.position
    dotY = [v.y for v in block_shape.get_vertices()]
    blockMaxY = max(dotY)

    if ball_pos.y > blockMaxY - 5 :
        ball_shape.body.velocity = (ball_shape.body.velocity.x, -400)

def spikeBlockFunc(ball_shape:pymunk.Shape, block_shape:pymunk.Shape, space:pymunk.space, scene):
    scene.manager.remove_scene_to_render(scene.__class__.__name__)
    scene.manager.add_scene_to_render('MainMenuScene')

def elevatorBlockFunc(ball_shape:pymunk.Shape, block_shape:pymunk.Shape, space:pymunk.space, scene):
    ball_pos = ball_shape.body.position
    dotY = [v.y for v in block_shape.get_vertices()]
    blockMaxY = max(dotY)

    #이미 리스폰 중이면 무시
    obj = getattr(block_shape, "user_data", None)
    obj:GameObject
    if obj is None:
        return

    if getattr(obj, "respawning", 0):
        return

    if ball_pos.y > blockMaxY - 5 :
            
        if not hasattr(obj, "_max_uses"):
            obj._max_uses = getattr(obj, "max_uses", 5)
        if not hasattr(obj, "_remaining_uses"):
            obj._remaining_uses = obj._max_uses
        
        ball_shape.body.velocity = (ball_shape.body.velocity.x, -400)

        obj._remaining_uses -= 1

        if obj._remaining_uses >= 0:

            new_pos = (block_shape.body.position.x, block_shape.body.position.y - 30)
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
