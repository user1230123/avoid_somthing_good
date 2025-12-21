from pyclbr import Class
import pygame
import pymunk
from blocks import object_trigger, object_type
import colors
import pymunk.pygame_util
from typing import Type

import scene
from scenes.physics_scene import PhysicsScene
from object import GameObject
from components.munk_physics import PhysicsComponent
from scenes.stages.map import Map_Structure
import settings
import utils

class GameStage(PhysicsScene):
    def __init__(self, screen: pygame.Surface, objects: list[GameObject] | None = None, map_class: Type[Map_Structure] | None = None):
        if objects is None:
            objects = []
        super().__init__(screen, objects,self)

        print("GameStage: Initializing GameStage")
        
        self.map_class = map_class

        print(f"GameStage: map_class is {map_class}")
        if map_class is not None:
            print(f"GameStage: Loading map {map_class.__name__}")
            self.map_instance = map_class(self)
            self.map_instance:Map_Structure
            for obj in self.map_instance.map_objs:
                super().add_object(obj)

        self.fonts = []
        self.fonts:list[pygame.Surface]

        self._create_ball()
        
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

    def update(self, dt: float):
        physics = self.ball_obj.get_component(PhysicsComponent)

        #플레이 타임 표기용 폰트 서피스
        self.fonts.append(utils.make_font_surface(60,None,"Time: "+str(round(self.manager.play_time,2)),colors.PINK))

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
        #플레이 타임을 화면에 그림(위치는 하드코딩)
        for font in self.fonts:
            self.fonts.remove(font)
            font_pos = utils.pos_by_one_block(1,1)
            font_pos = (font_pos[0],font_pos[1]-20)
            self.screen.blit(font,font_pos)

    def handle_event(self, event: pygame.event.Event):
        pass

    
    def _create_ball(self):
        # Dynamic Ball 생성
        ball_pos = self.map_instance.ball_start_pos
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