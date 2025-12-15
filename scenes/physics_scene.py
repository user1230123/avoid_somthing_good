import logging
from abc import abstractmethod

import pymunk
from components.munk_physics import PhysicsComponent
from object import GameObject
import pygame

from scene import Scene

class PhysicsScene(Scene):
    def __init__(self, screen: pygame.Surface, objects: list[GameObject]):
        super().__init__(screen, objects)
        
        self.space = pymunk.Space()
        self.space.gravity = (0, 900)

        for obj in self.objects:
            physics_comp = obj.get_component(PhysicsComponent)
            if physics_comp:
                physics_comp.add_to_space(self.space)

    def add_object(self, object: GameObject):
        super().add_object(object)

        physics_comp = object.get_component(PhysicsComponent)
        if physics_comp:
            physics_comp.add_to_space(self.space)
        else:
            logging.warning(f"PhysicsScene Object {id(object)} has no PhysicsComponent. Ignored.")

    def _update(self, dt: float):
        self.space.step(dt)

        self.update(dt)
        for obj in self.objects:
            obj._update(dt)

        for object in self.objects_to_remove:
            if object in self.objects:
                # Pymunk Space에서 제거
                physics_comp = object.get_component(PhysicsComponent)
                if physics_comp:
                    physics_comp.remove_from_space(self.space)
                
                self.objects.remove(object)
                
        self.objects_to_remove.clear()

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        pass