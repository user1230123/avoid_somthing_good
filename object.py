from pygame.math import Vector2
from abc import abstractmethod
from typing import Type, TypeVar, cast
from component import Component
import pygame

C = TypeVar('C', bound=Component)

class GameObject:
    def __init__(self, pos: Vector2 | tuple[float, float], size: tuple[int, int],
                 texture: pygame.Surface,
                 is_visible = True, rotation: float = 0,

                 components: dict[Type[Component], Component] | None = None):
        self.pos = Vector2(pos)
        self.size = size
        self.rotation = rotation

        
        self.original_texture = pygame.transform.scale(texture, size)
        self.texture = self.original_texture

        self.rect = self.texture.get_rect(center=self.pos)

        self.is_visible = is_visible

        if components is None:
            self.components = {}
        else:
            self.components = components
            for component in self.components.values():
                component.set_owner(self)

    def add_component(self, component: Component):
        component.set_owner(self)
        self.components[type(component)] = component

    def get_component(self, component_type: Type[C]) -> C | None:
        component = self.components.get(component_type)
        if component is not None:
            return cast(C, component)
        return None

    def get_pos(self) -> Vector2:
        return self.pos
    
    def get_rect(self) -> pygame.Rect:
        return self.rect
    
    def set_size(self, size: tuple[int, int]):
        self.size = size

        self.original_texture = pygame.transform.scale(self.original_texture, size)
        self._update_texture_rotation()

        # 나머지 Rect 처리는 texture rotation에서 처리됨
    
    def set_pos(self, pos: Vector2 | tuple[float, float]):
        self.pos = Vector2(pos)
        self.rect.center = (int(pos[0]), int(pos[1]))

    def set_rotation(self, angle: float):
        """회전 각도를 설정합니다."""
        if angle != self.rotation:
            self.rotation = angle
            self._update_texture_rotation()
            
    def _update_texture_rotation(self):
        """텍스처를 회전합니다."""
        
        # 텍스처 회전
        self.texture = pygame.transform.rotate(self.original_texture, self.rotation)
        
        # Rect 갱신
        current_center = self.rect.center
        self.rect = self.texture.get_rect(center=current_center)

    def _update(self, dt: float):
        for component in self.components.values():
            component.update(dt)

    def _draw(self, screen: pygame.Surface):
        if self.is_visible:
            screen.blit(self.texture, self.rect.topleft)