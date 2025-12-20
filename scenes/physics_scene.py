import logging
from abc import abstractmethod

import pymunk
from blocks.object_func import collision_trigger
from components.munk_physics import PhysicsComponent
from object import GameObject
import pygame

from scene import Scene

class PhysicsScene(Scene):
    def __init__(self, screen: pygame.Surface, objects: list[GameObject],childClassInstance_Scene:"PhysicsScene"):
        super().__init__(screen, objects)
        
        self.space = pymunk.Space()
        self.space.gravity = (0, 900)

        #충돌 핸들러 등록
        self.space.on_collision(begin=collision_trigger,data=childClassInstance_Scene)

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


    #space에 중복으로 body와 shape가 등록되는 것을 막습니다.
    def remove_physics(self, objects: GameObject):
        if isinstance(objects,list):
            for object in objects:
                physics_comp = object.get_component(PhysicsComponent)
                if physics_comp:
                    physics_comp.remove_from_space(self.space)
                else:
                    logging.warning(f"PhysicsScene Object {id(object)} has no PhysicsComponent. Ignored.")

    def _update(self, dt: float):
        self.space.step(dt)

        self.update(dt)
        for obj in self.objects:
            obj._update(dt)

        #블록들에 설정된 리스폰 타이머 처리
        for obj in list(self.objects):
            timer = getattr(obj, "respawning", 0)
            if timer:
                obj.respawning = timer - 1
                print(timer)
                if obj.respawning <= 0:
                    physics_comp = obj.get_component(PhysicsComponent)
                    if physics_comp:
                        physics_comp.add_to_space(self.space)
                    else:
                        logging.warning(f"PhysicsScene Object {id(obj)} has no PhysicsComponent. Ignored.")

                    # 타이머 제거
                    if hasattr(obj, "respawning"):
                        delattr(obj, "respawning")

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        pass