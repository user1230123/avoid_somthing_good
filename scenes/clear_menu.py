from pygame.event import Event
from scene import Scene
from object import GameObject
import colors
from scenes.stages.maps import map_sequence
import utils
import pygame

class GameClearScene(Scene):
    def __init__(self, screen: pygame.Surface, play_time):
        #self.title = GameObject((640, 360), (1280, 720), utils.image_load("game_over.png"), colors.BLACK)
        self.restartbutton = GameObject((640, 560), (500, 170), utils.image_load("restart_button.png"), colors.BLACK)
        
        self.clear_time = "CLEAR TIME : " + str(round(play_time,2))
        self.clear_time_font = utils.make_font_surface(180, None, self.clear_time, colors.PINK)

        self.objects = [
            GameObject(pygame.Vector2(screen.get_size()) / 2, screen.get_size(), utils.make_surface(screen.get_size(), colors.BLACK)),
            #self.title, 
            self.restartbutton
        ]
        super().__init__(screen, self.objects)

    def update(self, dt: float):
        pass

    def draw(self):
        self.screen.blit(self.clear_time_font, (640 - self.clear_time_font.get_size()[0]/2, 320 - self.clear_time_font.get_size()[1]))  # 클리어 타임 폰트 렌더링

    def handle_event(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.restartbutton.get_rect().collidepoint(event.pos):
                print("Restart!!")
                self.manager.remove_scene_to_render(self.__class__.__name__)
                self.manager.play_time = 0.0
                self.manager.add_scene_to_render('GameStage',None,map_sequence.get_next_map_sequence(None))