from blocks import object_type
from scenes.stages.map import Map_Structure
import utils


class FirstMap(Map_Structure):
    def __init__(self, scene):
        print("FirstMap: Initializing FirstMap")
        self.scene = scene
        super().__init__(scene)
        self.ball_start_pos = utils.pos_by_one_block(2, 3)

        for x in range(1,10):
            block_pos_rept = utils.pos_by_one_block(x,1)
            block_obj = utils.make_static_object(block_pos_rept,'floor.png',object_type.PLATFORM)
            super().add_map_object(block_obj)

        for x in range(20,30):
            block_pos_rept = utils.pos_by_one_block(x,18)
            block_obj = utils.make_static_object(block_pos_rept,'floor.png',object_type.PLATFORM)
            super().add_map_object(block_obj)

        for x in range(15,20):
            block_pos_rept = utils.pos_by_one_block(x,12)
            block_obj = utils.make_static_object(block_pos_rept,'floor.png',object_type.PLATFORM)
            super().add_map_object(block_obj)

        for x in range(5,17,3):
            block_pos_rept = utils.pos_by_one_block(x,18)
            block_obj = utils.make_static_object(block_pos_rept,'floor.png',object_type.PLATFORM)
            super().add_map_object(block_obj)

        for x in range(2,10):
            block_pos_rept = utils.pos_by_one_block(x,9)
            block_obj = utils.make_static_object(block_pos_rept,'floor.png',object_type.PLATFORM)
            super().add_map_object(block_obj)

        for x in range(4,10,3):
            block_pos_rept = utils.pos_by_one_block(x,10)
            block_obj = utils.make_static_object(block_pos_rept,'spike.png',object_type.SPIKE_BLOCK)
            super().add_map_object(block_obj)

        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(12,1),'jump.png',object_type.JUMP_BLOCK))
        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(16,1),'jump.png',object_type.JUMP_BLOCK))
        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(20,1),'jump.png',object_type.JUMP_BLOCK))

        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(24,1),'elevator.png',object_type.ELEVATOR_BLOCK))

        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(29,1),'gravity.png',object_type.GRAVITY_BLOCK))
        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(19,18),'gravity.png',object_type.GRAVITY_BLOCK))
        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(14,12),'gravity.png',object_type.GRAVITY_BLOCK))
        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(2,18),'gravity.png',object_type.GRAVITY_BLOCK))

        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(14,4),'spike.png',object_type.SPIKE_BLOCK))
        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(18,4),'spike.png',object_type.SPIKE_BLOCK))
        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(22,4),'spike.png',object_type.SPIKE_BLOCK))
        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(15,13),'spike.png',object_type.SPIKE_BLOCK))

        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(13,13),'floor.png',object_type.PLATFORM))
        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(13,14),'floor.png',object_type.PLATFORM))

        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(9,10),'complete.png',object_type.COMPLETE_BLOCK))