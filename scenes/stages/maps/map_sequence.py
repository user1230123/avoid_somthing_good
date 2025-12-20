from scenes.stages.maps.first_map import FirstMap
from scenes.stages.maps.second_map import SecondMap

MAP_SEQUENCE = [FirstMap, SecondMap] # 여기에 맵 클래스를 추가하세요.

def get_next_map_sequence(current_map_class = None):
    # current_map_class가 None이면 첫 번째 맵을 반환
    if current_map_class not in MAP_SEQUENCE:
        print("Returning first map")
        return MAP_SEQUENCE[0]
    current_index = MAP_SEQUENCE.index(current_map_class)
    next_index = (current_index + 1) % len(MAP_SEQUENCE)
    print(len(MAP_SEQUENCE), next_index)
    print("Returning next map")
    return MAP_SEQUENCE[next_index]