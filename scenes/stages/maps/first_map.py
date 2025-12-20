from blocks import object_type
from scenes.stages.map import Map_Structure
import utils


class FirstMap(Map_Structure):
    def __init__(self, scene):
        print("FirstMap: Initializing FirstMap")
        self.scene = scene
        super().__init__(scene)
        self.ball_start_pos = utils.pos_by_one_block(5, 15)

        # 바닥 플랫폼 생성
        for i in range(1, 33):
            platform = utils.make_static_object(utils.pos_by_one_block(i, 1), "floor.png")
            super().add_map_object(platform)

        # 중간 플랫폼 생성
        for i in range(10, 15):
            platform = utils.make_static_object(utils.pos_by_one_block(i, 4), "floor.png")
            super().add_map_object(platform)

        for i in range(15, 20):
            platform = utils.make_static_object(utils.pos_by_one_block(i, 3), "floor.png")
            super().add_map_object(platform)
        # 중력 반전 블록 생성
        gravity_block = utils.make_static_object(utils.pos_by_one_block(25, 14), "gravity.png",object_type.GRAVITY_BLOCK)
        super().add_map_object(gravity_block)
        # 점프 블록 생성
        jump_block = utils.make_static_object(utils.pos_by_one_block(5, 10), "jump.png", object_type.JUMP_BLOCK)
        super().add_map_object(jump_block)
        