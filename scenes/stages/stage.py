import pygame
import pymunk
from blocks import object_type
import colors
import pymunk.pygame_util

from scenes.physics_scene import PhysicsScene
from object import GameObject
from components.munk_physics import PhysicsComponent
import settings
import utils 


class GameStage(PhysicsScene):
    def __init__(self, screen: pygame.Surface, objects: list[GameObject] | None = None):
        if objects is None:
            objects = []
        super().__init__(screen, objects,self)

        block_size = settings.BLOCK_SIZE

        block_pos = (20, block_size[1]*18-20)
        
        for x in range(0,42):
            block_pos_rept = (block_pos[0] + block_size[0]*x, block_pos[1])
            block_obj = utils.makeStaticObject(block_pos_rept,"floor.png",block_size,object_type.PLATFORM)
            super().add_object(block_obj)

        for x in range(0,42):
            block_pos_rept = (block_pos[0] + block_size[0]*x - 20, block_pos[1] - block_size[1]*9)
            block_obj = utils.makeStaticObject(block_pos_rept,"floor.png",block_size,object_type.PLATFORM)
            super().add_object(block_obj)

        super().add_object(utils.makeStaticObject((block_size[0]*2-20,block_size[0]*17-20),"floor.png",block_size,object_type.PLATFORM))
        super().add_object(utils.makeStaticObject((block_size[0]*2-20,block_size[1]*16-20),"floor.png",block_size,object_type.PLATFORM))
        super().add_object(utils.makeStaticObject((block_size[0]*2-20,block_size[1]*15-20),"floor.png",block_size,object_type.PLATFORM))
        super().add_object(utils.makeStaticObject((block_size[0]*2-20,block_size[1]*14-20),"floor.png",block_size,object_type.PLATFORM))

        super().add_object(utils.makeStaticObject((block_size[0]*4-20,block_size[1]*11-20),"gravity.png",block_size,object_type.GRAVITY_BLOCK))
        super().add_object(utils.makeStaticObject((block_size[0]*4-20,block_size[1]*16-20),"gravity.png",block_size,object_type.GRAVITY_BLOCK))

        super().add_object(utils.makeStaticObject((block_size[0]*9-20,block_size[1]*17-20),"spike.png",block_size,object_type.SPIKE_BLOCK))
        super().add_object(utils.makeStaticObject((block_size[0]*10-20,block_size[1]*17-20),"complete.png",block_size,object_type.COMPLETE_BLOCK))

        test_obj = utils.makeStaticObject((block_size[0]*3-20,block_size[1]*16-20),"elevator.png",block_size,object_type.ELEVATOR_BLOCK)
        super().add_object(test_obj)

        self._create_ball()
        
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

        ball_pos = self.ball_obj.get_pos()

        if ball_pos.x < 0 or ball_pos.y < 0:
            self.manager.remove_scene_to_render(self.__class__.__name__)
            self.manager.add_scene_to_render('GameOverScene')
        if ball_pos.y > self.screen.get_height() or ball_pos.x > self.screen.get_width():
            self.manager.remove_scene_to_render(self.__class__.__name__)
            self.manager.add_scene_to_render('GameOverScene')
        


    def draw(self):
        pass

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            print(pymunk.version)

    def _create_ball(self):
        # Dynamic Ball 생성
        ball_pos = (200, 600)
        ball_radius = settings.BALL_RADIUS
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
        ball_shape.collision_type = object_type.BALL
        
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