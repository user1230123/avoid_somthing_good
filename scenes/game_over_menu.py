from pygame.event import Event
from scene import Scene
from object import GameObject
import colors
from scenes.stages.maps import map_sequence
import utils
import pygame


class GameOverScene(Scene):
    def __init__(self, screen: pygame.Surface):
        self.title = GameObject((640, 360), (1280,720), utils.image_load("game_over.png"), colors.BLACK)
        self.restartbutton = GameObject((640, 560), (500, 160), utils.image_load("restart_button.png"))
        
            
        
        self.objects = [
            GameObject(pygame.Vector2(screen.get_size()) / 2, screen.get_size(), utils.make_surface(screen.get_size(), colors.BLACK)),
            self.title,
            self.restartbutton,
        ]
        super().__init__(screen, self.objects)

    def update(self, dt: float):
        pass

    def draw(self):
        pass


    def handle_event(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.restartbutton.get_rect().collidepoint(event.pos):
                print("Restart!!")
                self.manager.remove_scene_to_render(self.__class__.__name__)
                self.manager.play_time = 0.0
                self.manager.player_score = 0.0
                self.manager.add_scene_to_render('GameStage',None,map_sequence.get_next_map_sequence(None))
                pygame.key.stop_text_input()
