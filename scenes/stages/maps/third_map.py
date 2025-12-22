from blocks import object_type
from scenes.stages.map import Map_Structure
import utils

class ThirdMap(Map_Structure):
    def __init__(self, scene):
            print("ThirdMap: Initializing ThirdMap")
            self.scene = scene
            super().__init__(scene)
            self.ball_start_pos = utils.pos_by_one_block(2, 3)

            for x in range(1,23):
                block_pos_rept = utils.pos_by_one_block(x,11)
                self.add_block(block_pos_rept,'floor.png',object_type.PLATFORM)

            for x in range(3,23):
                block_pos_rept = utils.pos_by_one_block(x,7)
                self.add_block(block_pos_rept,'floor.png',object_type.PLATFORM)

            for x in range(1,33):
                block_pos_rept = utils.pos_by_one_block(x,1)
                self.add_block(block_pos_rept,'floor.png',object_type.PLATFORM)
            
            for x in range(2,19):
                block_pos_rept = utils.pos_by_one_block(32,x)
                self.add_block(block_pos_rept,'floor.png',object_type.PLATFORM)
            
            self.add_block(utils.pos_by_one_block(31,2),'complete.png',object_type.COMPLETE_BLOCK)
            self.add_block(utils.pos_by_one_block(4,2),'complete.png',object_type.COMPLETE_BLOCK)

            self.add_block(utils.pos_by_one_block(3,3),'floor.png',object_type.PLATFORM)
            self.add_block(utils.pos_by_one_block(1,5),'floor.png',object_type.PLATFORM)
            self.add_block(utils.pos_by_one_block(1,9),'floor.png',object_type.PLATFORM)
            
            self.add_block(utils.pos_by_one_block(25,7),'floor.png',object_type.PLATFORM)

            self.add_block(utils.pos_by_one_block(28,7),'floor.png',object_type.PLATFORM)
            self.add_block(utils.pos_by_one_block(29,7),'floor.png',object_type.PLATFORM)
            self.add_block(utils.pos_by_one_block(30,7),'floor.png',object_type.PLATFORM)

            self.add_block(utils.pos_by_one_block(24,2),'floor.png',object_type.PLATFORM)
            self.add_block(utils.pos_by_one_block(24,3),'floor.png',object_type.PLATFORM)
            self.add_block(utils.pos_by_one_block(24,4),'floor.png',object_type.PLATFORM)
            
            self.add_block(utils.pos_by_one_block(23,4),'elevator.png',object_type.ELEVATOR_BLOCK)


            self.add_block(utils.pos_by_one_block(31,7),'gravity.png',object_type.GRAVITY_BLOCK)
            self.add_block(utils.pos_by_one_block(24,7),'gravity.png',object_type.GRAVITY_BLOCK)
            
            self.add_block(utils.pos_by_one_block(28,6),'spike_under.png',object_type.SPIKE_BLOCK)
            self.add_block(utils.pos_by_one_block(28,3),'spike.png',object_type.SPIKE_BLOCK)
            self.add_block(utils.pos_by_one_block(29,3),'spike.png',object_type.SPIKE_BLOCK)
            self.add_block(utils.pos_by_one_block(30,3),'spike.png',object_type.SPIKE_BLOCK)
            
            self.add_block(utils.pos_by_one_block(26,3),'elevator.png',object_type.ELEVATOR_BLOCK)

            self.add_block(utils.pos_by_one_block(28,2),'floor.png',object_type.PLATFORM)
            self.add_block(utils.pos_by_one_block(29,2),'floor.png',object_type.PLATFORM)
            self.add_block(utils.pos_by_one_block(30,2),'floor.png',object_type.PLATFORM)
                
    
    def add_block(self, block_pos: tuple, block_png: str, type: int):
        super().add_map_object(utils.make_static_object(block_pos, block_png, type))
         
            
