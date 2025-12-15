# test_scene.py

import pygame
import pymunk
import colors
import pymunk.pygame_util

from scenes.physics_scene import PhysicsScene
from object import GameObject
from components.munk_physics import PhysicsComponent 

class TestPhysicsScene(PhysicsScene):
    def __init__(self, screen: pygame.Surface, objects: list[GameObject] = []):
        super().__init__(screen, objects)

        floor_height = 550
        
        # Static Body 생성
        floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        # 두께 5의 선분
        floor_shape = pymunk.Segment(floor_body, (0, floor_height), (600, floor_height), 5)
        floor_shape.elasticity = 0.5  # 탄성
        floor_shape.friction = 0.8   # 마찰력
        
        # Pymunk Space에 추가
        self.space.add(floor_body, floor_shape)
        
        # self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

    def update(self, dt: float):
        pass

    def draw(self):
        pass

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._create_ball()

    def _create_ball(self):
        # Dynamic Ball 생성
        ball_pos = (200, 50)
        ball_radius = 20
        ball_size = (ball_radius * 2, ball_radius * 2)
        
        # 텍스처 생성
        ball_texture = pygame.Surface(ball_size, pygame.SRCALPHA)
        pygame.draw.circle(ball_texture, colors.BLUE, (ball_radius, ball_radius), ball_radius)
        
        # Body, Shape 생성
        mass = 10
        inertia = pymunk.moment_for_circle(mass, 0, ball_radius)
        ball_body = pymunk.Body(mass, inertia)
        ball_shape = pymunk.Circle(ball_body, ball_radius)
        ball_shape.elasticity = 0.95
        ball_shape.friction = 0.5
        
        # 초기 위치, 속도 설정
        ball_body.position = ball_pos
        ball_body.angular_velocity = 1.0 # 회전속도
        
        # PhysicsComponent 생성
        physics_comp = PhysicsComponent(ball_body, ball_shape)

        # GameObject 생성, Component 추가
        self.ball_obj = GameObject(
            pos=ball_pos, 
            size=ball_size, 
            texture=ball_texture,
        )
        self.ball_obj.add_component(physics_comp)
        
        # 씬에 GameObject 추가
        self.add_object(self.ball_obj)