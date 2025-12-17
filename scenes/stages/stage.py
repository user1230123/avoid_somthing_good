import pygame
import pymunk
import colors
import pymunk.pygame_util

from scenes.physics_scene import PhysicsScene
from object import GameObject
from components.munk_physics import PhysicsComponent
import utils 


class GameStage(PhysicsScene):
    def __init__(self, screen: pygame.Surface, objects: list[GameObject] = []):
        super().__init__(screen, objects)

        self.COLLISION_BALL = 1
        self.COLLISION_PLATFORM = 2

        floor_pos = (640, 710) 

        floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        floor_body.position = floor_pos

        floor_shape = pymunk.Segment(floor_body, (-640, 0), (640, 0), 10)

        floor_shape.elasticity = 1.0
        floor_shape.collision_type = self.COLLISION_PLATFORM
        floor_shape.friction = 0.8

        physics_comp = PhysicsComponent(floor_body, floor_shape)

        floor_obj = GameObject(
            pos=floor_pos, 
            size=(1280, 20),
            texture=utils.make_surface((1280, 20), colors.WHITE),
        )
        floor_obj.add_component(physics_comp)
        floor_shape.user_data = floor_obj

        super().add_object(floor_obj)
        
        self._create_ball()

        self.space.on_collision(
            self.COLLISION_BALL,
            self.COLLISION_PLATFORM,
            begin=self._on_ball_hit_platform
        )
        
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

    def update(self, dt: float):
        physics = self.ball_obj.get_component(PhysicsComponent)
        vx, vy = physics.body.velocity

        acceleration = 500  # px/s^2, 얼마나 빨리 가속할지
        max_speed = 150       # px/s, 최대 좌우 속도
        friction = 800       # px/s^2, 키를 떼면 속도 감소

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            vx -= acceleration * dt
        elif keys[pygame.K_RIGHT]:
            vx += acceleration * dt
        else:
            # 키를 누르지 않으면 속도 줄이기
            if vx > 0:
                vx -= friction * dt
                if vx < 0: vx = 0
            elif vx < 0:
                vx += friction * dt
                if vx > 0: vx = 0

        # 속도 제한
        vx = max(-max_speed, min(max_speed, vx))

        # 적용
        physics.body.velocity = (vx, vy)

    def _on_ball_hit_platform(self, arbiter, space, data):
        ball_shape, floor_shape = arbiter.shapes
        body = ball_shape.body
        floor = floor_shape.user_data

        body.velocity = (body.velocity.x, -400)


    def draw(self):
        pass

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            print("!!")

    def _create_ball(self):
        # Dynamic Ball 생성
        ball_pos = (200, 50)
        ball_radius = 10
        ball_size = (ball_radius * 2, ball_radius * 2)
        
        # 텍스처 생성
        ball_texture = pygame.Surface(ball_size, pygame.SRCALPHA)
        pygame.draw.circle(ball_texture, colors.WHITE, (ball_radius, ball_radius), ball_radius)
        
        # Body, Shape 생성
        mass = 10
        inertia = pymunk.moment_for_circle(mass, 0, ball_radius)
        ball_body = pymunk.Body(mass, inertia)
        ball_shape = pymunk.Circle(ball_body, ball_radius)
        ball_shape.elasticity = 1
        ball_shape.friction = 0.5
        ball_shape.collision_type = self.COLLISION_BALL
        
        # 초기 위치, 속도 설정
        ball_body.position = ball_pos
        
        # PhysicsComponent 생성
        physics_comp = PhysicsComponent(ball_body, ball_shape)

        # GameObject 생성, Component 추가
        self.ball_obj = GameObject(
            pos=ball_pos, 
            size=ball_size, 
            texture=ball_texture,
        )
        ball_shape.user_data = self.ball_obj
        self.ball_obj.add_component(physics_comp)
        
        # 씬에 GameObject 추가
        self.add_object(self.ball_obj)