from pygame.event import Event
from scene import Scene
from object import GameObject
import colors
from scenes.stages.maps import map_sequence
import utils
import requests
import pygame
import ast


class GameClearScene(Scene):
    def __init__(self, screen: pygame.Surface, play_time, player_score):
        self.text = ""
        self.font_size = 60
        self.isTyping = False
        self.font = utils.make_font_surface(self.font_size, None, self.text, colors.LIGHT_GRAY)
        self.guide_font = utils.make_font_surface(self.font_size, None, 'Please enter your nickname', colors.BLUE)

        self.isConfirmed = False

        self.input_box = GameObject((640, 360), (300, 40), utils.make_surface((300, 50),colors.GRAY))
        self.restartbutton = GameObject((640, 560), (500, 160), utils.image_load("restart_button.png"))
        self.confirm_button = GameObject((640, 430), (200, 50), utils.image_load("confirm_button.png"))
        self.leaderboard = GameObject((640, 260), (1000, 400), utils.image_load("button.png"))
        
        self.fonts = []

        #점수 계산
        self.player_score = 600 - 2 * int(play_time)
        if self.player_score < 0:
            self.player_score = 0
        self.player_score = self.player_score + player_score

        self.clear_time = "CLEAR TIME : " + str(round(play_time,2)) + 's --- SCORE : ' + str(int(self.player_score)) + 'P'
        self.clear_font = utils.make_font_surface(60, None, self.clear_time, colors.GREEN)

        self.objects = [
            GameObject(pygame.Vector2(screen.get_size()) / 2, screen.get_size(), utils.make_surface(screen.get_size(), colors.BLACK)),
            self.input_box,
            self.confirm_button,
            self.restartbutton
        ]
        super().__init__(screen, self.objects)

    def update(self, dt: float):
        self.font = utils.make_font_surface(30,"malgungothic",self.text,colors.LIGHT_GRAY)

    def draw(self):
        if not self.isConfirmed:
            self.screen.blit(self.clear_font, (640 - self.clear_font.get_size()[0]/2, 260 - self.clear_font.get_size()[1]))  # 클리어 타임 폰트 렌더링
            self.screen.blit(self.guide_font, (640 - self.guide_font.get_size()[0]/2, 310 - self.guide_font.get_size()[1]))
            self.input_box.texture.fill(colors.GRAY)
            self.input_box.texture.blit(self.font,(0,0))
        else:
            self.leaderboard._draw(self.screen)
            for font in self.fonts:
                self.leaderboard.texture.blit(*font)

    def handle_event(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.restartbutton.get_rect().collidepoint(event.pos):
                print("Restart!!")
                self.manager.remove_scene_to_render(self.__class__.__name__)
                self.manager.play_time = 0.0
                self.manager.player_score = 0.0
                self.manager.add_scene_to_render('GameStage',None,map_sequence.get_next_map_sequence(None))

            if self.input_box.get_rect().collidepoint(event.pos):
                self.isTyping = True
                pygame.key.start_text_input()
            
            if self.confirm_button.get_rect().collidepoint(event.pos):
                #requests.post('http://api-dev.kro.kr:8080/register? name=' + self.player_name + '&score=' + player_score) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 점수 저장
                print("점수 저장 꺼져있음!!!!!!!!!!!!!!!!!!!!!!")
                player_name = self.text
                print(player_name + '   ' + str(self.player_score))
                self.load_ranking()
                self.isConfirmed = True
        if self.isTyping:
            self.textInput(event)
    
    def textInput(self, event:Event):
        #이름 입력
        if event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_BACKSPACE: #백스페이스 처리
                self.text = self.text[:-1]
                print("입력 증:", self.text)
            elif event.key == pygame.K_RETURN:#엔터 처리
                print("입력 완료:", self.text)
                self.isTyping = False
                pygame.key.stop_text_input()
        elif event.type == pygame.TEXTINPUT:
            if len(self.text) < 6:
                # 완성된 글자가 들어옴 (한글 포함)
                self.text += event.text
                print("입력 중:", self.text)
    
    def load_ranking(self):
        response = requests.get('http://api-dev.kro.kr:8080/leaderboard')
        print(response.text)
        leaderboard_list = ast.literal_eval(response.text)
        dict_list = [dict(elm) for elm in leaderboard_list]
        sorted_list = sorted(dict_list, key=lambda x: x.get("score", 0), reverse=True)
        print(sorted_list)

        ranking = ['1st','2nd','3rd','4th','5th']

        for x in range(0,5):
            if x < len(sorted_list):
                text = ranking[x] + ' : ' + sorted_list[x].get("name",'nothing') + ' -> ' + str(sorted_list[x].get("score",'nothing')) + 'P'
                print(text)
                self.fonts.append((utils.make_font_surface(50, "malgungothic", text, colors.GOLD),(15,80*x)))