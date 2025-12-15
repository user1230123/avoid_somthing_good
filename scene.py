from typing import TYPE_CHECKING
from abc import abstractmethod
from object import GameObject
import pygame

if TYPE_CHECKING: # Python 3.10 or less를 위한 Forward Reference Type Checking
    from manager import SceneManager

class Scene:
    # 모든 Scene은 ScreenManager에 등록되어 관리되어야 합니다.
    def __init__(self, screen: pygame.Surface, objects: list[GameObject]):
        self.screen = screen
        self.objects = objects

        self.objects_to_remove: set[GameObject] = set()

    def set_manager(self, manager: "SceneManager"):
        """
        Scene의 Manager를 지정합니다.
        SceneManager에 의해 자동으로 초기화되므로 직접 호출하지 마십시오.
        """
        self.manager = manager

    def add_object(self, object: GameObject):
        """
        Scene에 GameObject를 추가합니다.
        """
        self.objects.append(object)

    def remove_object(self, object: GameObject) -> bool:
        """
        Scene에서 GameObject를 제거합니다.
        Scene의 object 리스트에 제거 대상 object가 없을 경우 False를 반환합니다.
        제거는 update가 종료된 이후에 수행됩니다.
        """
        if object in self.objects:
            if isinstance(object, list):
                self.objects_to_remove.update(object)
            else:
                self.objects_to_remove.add(object)
            return True
        return False

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        pass

    def _on_event(self, event: pygame.event.Event):
        self.handle_event(event)

    def _update(self, dt: float):
        self.update(dt)
        for obj in self.objects:
            obj._update(dt)

        for object in self.objects_to_remove: # Remove 플래그된 Object Remove
            if object in self.objects:
                self.objects.remove(object)
        self.objects_to_remove.clear()

    def _draw(self):
        for obj in self.objects:
            obj._draw(self.screen)
        self.draw()