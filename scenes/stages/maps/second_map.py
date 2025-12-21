import utils

from blocks import object_type
from scenes.stages.map import Map_Structure


class SecondMap(Map_Structure):
    def __init__(self, scene):
        print("SecondMap: Initializing SecondMap")
        self.scene = scene
        super().__init__(scene)
        self.ball_start_pos = utils.pos_by_one_block(3,3)

        for x in range(3,10,3):
            block_pos_rept = utils.pos_by_one_block(x,1)
            block_obj = utils.make_static_object(block_pos_rept,'floor.png',object_type.PLATFORM)
            super().add_map_object(block_obj)

        for x in range(11,20):
            block_pos_rept = utils.pos_by_one_block(x,1)
            block_obj = utils.make_static_object(block_pos_rept,'floor.png',object_type.PLATFORM)
            super().add_map_object(block_obj)

        for x in range(24,30):
            block_pos_rept = utils.pos_by_one_block(x,13)
            block_obj = utils.make_static_object(block_pos_rept,'floor.png',object_type.PLATFORM)
            super().add_map_object(block_obj)

        for x in range(9,32,3):
            block_pos_rept = utils.pos_by_one_block(x,18)
            block_obj = utils.make_static_object(block_pos_rept,'floor.png',object_type.PLATFORM)
            super().add_map_object(block_obj)

        for x in range(3,10):
            block_pos_rept = utils.pos_by_one_block(x,9)
            block_obj = utils.make_static_object(block_pos_rept,'floor.png',object_type.PLATFORM)
            super().add_map_object(block_obj)

        for x in range(1,10):
            block_pos_rept = utils.pos_by_one_block(x,5)
            block_obj = utils.make_static_object(block_pos_rept,'floor.png',object_type.PLATFORM)
            super().add_map_object(block_obj)

        for x in range(1,5):
            block_pos_rept = utils.pos_by_one_block(9,x+9)
            block_obj = utils.make_static_object(block_pos_rept,'floor.png',object_type.PLATFORM)
            super().add_map_object(block_obj)

        for x in range(12,16,3):
            block_pos_rept = utils.pos_by_one_block(x,14)
            block_obj = utils.make_static_object(block_pos_rept,'floor.png',object_type.PLATFORM)
            super().add_map_object(block_obj)

        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(13,2),'spike.png',object_type.SPIKE_BLOCK))
        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(15,2),'spike.png',object_type.SPIKE_BLOCK))
        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(5,10),'spike.png',object_type.SPIKE_BLOCK))
        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(5,6),'spike.png',object_type.SPIKE_BLOCK))

        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(21,1),'jump.png',object_type.JUMP_BLOCK))
        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(22,5),'jump.png',object_type.JUMP_BLOCK))

        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(23,9),'elevator.png',object_type.ELEVATOR_BLOCK))
        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(10,5),'elevator.png',object_type.ELEVATOR_BLOCK))
        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(11,10),'elevator.png',object_type.ELEVATOR_BLOCK))


        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(30,13),'gravity.png',object_type.GRAVITY_BLOCK))
        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(6,18),'gravity.png',object_type.GRAVITY_BLOCK))

        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(1,9),'floor.png',object_type.PLATFORM))
        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(16,8),'floor.png',object_type.PLATFORM))

        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(16,9),'complete.png',object_type.COMPLETE_BLOCK))
        super().add_map_object(utils.make_static_object(utils.pos_by_one_block(4,3),'complete.png',object_type.COMPLETE_BLOCK))