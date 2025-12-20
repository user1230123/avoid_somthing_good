from typing import Type
from scene import Scene
import pygame

from scenes.physics_scene import PhysicsScene

class SceneManager:
    # SceneManager는 FIFO (First In First Out) 에 따라 Draw하므로, 마지막 Scene이 위에 그려집니다.

    # 기본적으로 Scene은 Class 형태로 입력되어야 하며,
    # 게임에 사용될 모든 Scene은 Manager 초기화 시 입력되어야 합니다.
    # Render로 체크된 Scene은 내부에서 Instance화 되어 Render됩니다.
    def __init__(self, screen: pygame.Surface, scenes: list[Type[Scene]] | Type[Scene]):
        if not isinstance(scenes, list):
            self.scenes = [scenes]
        else:
            self.scenes = scenes

        self.screen = screen

        # Scenes dict 초기화
        self.scenes_dict = {scene.__name__: scene for scene in self.scenes}

        self.scenes_to_render: list[Scene] = []
        self.render_names_set: set[str] = set()  # 중복 렌더링 체크용

        self.scenes_to_remove_render: set[Scene] = set()
        self.scenes_to_remove: set[Type[Scene]] = set()

    def set_manager(self, scenes: list[Scene]):
        for s in scenes:
            s.set_manager(self)

    def add_scene_to_render(self, scene_name: str, *args, **kwargs) -> bool:
        """
        Scene 리스트에서 렌더링될 Scene을 지정합니다.
        scene_name은 Manager 초기화 시 파라미터로 주어진 scenes 리스트에 포함되어 있어야 합니다.
        파라미터를 추가하여 kwargs를 전달할 수 있습니다.
        """
        if scene_name in self.scenes_dict and scene_name not in self.render_names_set:
            scenes_instance = self.scenes_dict[scene_name](self.screen, *args, **kwargs)
            self.scenes_to_render.append(scenes_instance)
            self.render_names_set.add(scene_name)
            self.set_manager([scenes_instance])
            return True
        return False
    
    def remove_scene_to_render(self, scene_name: str) -> bool:
        """
        Scene 리스트에서 렌더링될 Scene을 제거합니다.
        scene_name은 렌더링될 Scene을 가리켜야 합니다.
        """
        if scene_name in self.scenes_dict:
            for scene_to_render in self.scenes_to_render:
                if scene_to_render.__class__.__name__ == scene_name:
                    self.scenes_to_remove_render.add(scene_to_render)
                    self.render_names_set.discard(scene_name)
                    return True
        return False

    def add_scene(self, scene: list[Type[Scene]] | Type[Scene]):
        """
        Scene 리스트에 Scene을 추가합니다.
        렌더링될 Scene을 추가한다면, add_scene_to_render를 참조하십시오.
        """
        if isinstance(scene, list):
            self.scenes.extend(scene)
            for s in scene:
                self.scenes_dict[s.__name__] = s
        else:
            self.scenes.append(scene)
            self.scenes_dict[scene.__name__] = scene

    def remove_scene(self, scene: list[Type[Scene]] | Type[Scene]) -> bool:
        """
        Scene 리스트에서 Scene을 제거합니다.
        렌더링될 Scene을 제거할 경우에는, remove_scene_to_render를 참조하십시오. 
        """
        if scene in self.scenes:
            if isinstance(scene, list):
                self.scenes_to_remove.update(scene)
            else:
                self.scenes_to_remove.add(scene)
            return True
        return False

    def set_scene(self, scene: list[Type[Scene]] | Type[Scene]):
        """
        Scene 리스트를 다시 지정합니다.
        """
        if isinstance(scene, list):
            self.scenes = scene
        else:
            self.scenes = [scene]

        self.scenes_dict.clear()
        for s in self.scenes:
            self.scenes_dict[s.__name__] = s

    def _on_event(self, event: pygame.event.Event):
        for scene in self.scenes_to_render:
            scene.handle_event(event)

    def _update(self, dt: float):
        for scene in self.scenes_to_render: # Render로 지정된 Scene update
            scene._update(dt)

        for scene in self.scenes_to_remove_render: # Remove 플래그된 Render Scene Remove
            if scene in self.scenes_to_render:
                if isinstance(scene,PhysicsScene):
                    scene.remove_physics(scene.objects)
                self.scenes_to_render.remove(scene)
                self.render_names_set.discard(scene.__class__.__name__)
        self.scenes_to_remove_render.clear()
        
        for scene_class in self.scenes_to_remove: # Remove 플래그된 Scene Remove
            if scene_class in self.scenes:
                self.scenes.remove(scene_class)
            if scene_class.__name__ in self.scenes_dict: # scenes_dict 갱신
                del self.scenes_dict[scene_class.__name__]
        self.scenes_to_remove.clear()

    def _draw(self):
        for scene in self.scenes_to_render:
            scene._draw()
