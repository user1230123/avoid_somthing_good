from abc import abstractmethod
from object import GameObject
import utils

class Map_Structure:
    def __init__(self, scene):
        print("Map_Structure: Initializing Map_Structure")
        self.map_objs = []
        self.map_objs: list[GameObject]
        self.scene = scene

        # 플레이어 시작 위치
        self.ball_start_pos = (0, 0)

    def add_map_object(self, obj:GameObject):
        self.map_objs.append(obj)

    # 특정 블록 인덱스에 해당하는 오브젝트를 반환합니다.
    def get_block_object_at(self, x, y): # x, y는 블록 인덱스
        targetObj_pos = utils.pos_by_one_block(x, y)
        for obj in self.map_objs:
            obj_pos = obj.get_pos()
            if obj_pos == targetObj_pos:
                return obj
        return None
    
    def get_ball_start_pos(self):
        return self.ball_start_pos