from pygame.event import Event
from scene import Scene
from object import GameObject
import colors
from scenes.stages.maps import map_sequence
import settings
import utils
import pygame

class MainMenuScene(Scene):
    def __init__(self, screen: pygame.Surface):
        self.title = GameObject((420, 170), (800, 300), utils.image_load("title.png"), colors.BLACK)
        self.playbutton = GameObject((300, 420), (500, 170), utils.image_load("playbutton.png"), colors.BLACK)
        
        self.objects = [
            GameObject(pygame.Vector2(screen.get_size()) / 2, screen.get_size(), utils.make_surface(screen.get_size(), colors.BLACK)),
            self.title, self.playbutton
        ]
        super().__init__(screen, self.objects)

    def update(self, dt: float):
        pass

    def handle_event(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.playbutton.get_rect().collidepoint(event.pos):
                print("Play!!")
                self.manager.remove_scene_to_render(self.__class__.__name__)
                self.manager.add_scene_to_render('GameStage',None,map_sequence.get_next_map_sequence(None))