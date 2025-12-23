from pygame.event import Event
from scene import Scene
from object import GameObject
import colors
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
        self.guide_font_highlight_time = 0

        self.isConfirmed = False


        self.input_box = GameObject((640, 360), (310, 50), utils.image_load("input_box.png"))
        self.restartbutton = GameObject((640, 560), (500, 160), utils.image_load("restart_button.png"))
        self.confirm_button = GameObject((640, 430), (200, 50), utils.image_load("confirm_button.png"))
        self.leaderboard = GameObject((640, 260), (1000, 400), utils.image_load("leaderboard.png"))
        self.background = GameObject(pygame.Vector2(screen.get_size()) / 2, screen.get_size(), utils.make_surface(screen.get_size(), colors.BLACK))
        
        self.fonts = []

        #점수 계산
        self.player_score = 600 - 2 * int(play_time)
        if self.player_score < 0:
            self.player_score = 0
        self.player_score = int(self.player_score + player_score)

        self.clear_time = "CLEAR TIME : " + str(round(play_time,2)) + 's --- SCORE : ' + str(self.player_score) + 'P'
        self.clear_font = utils.make_font_surface(60, None, self.clear_time, colors.GREEN)

        self.objects = [
            self.background,
            self.input_box,
            self.confirm_button,
            self.restartbutton
        ]
        super().__init__(screen, self.objects)

    def update(self, dt: float):
        self.font = utils.make_font_surface(30,"malgungothic",self.text,colors.LIGHT_GRAY)
        if self.guide_font_highlight_time > 0:
            self. guide_font_highlight_time -= 1
        else:
            self.guide_font = utils.make_font_surface(self.font_size, None, 'Please enter your nickname', colors.BLUE)


    def draw(self):
        if not self.isConfirmed:
            typingFontPos = self.input_box.get_rect().topleft
            self.screen.blit(self.clear_font, (640 - self.clear_font.get_size()[0]/2, 260 - self.clear_font.get_size()[1]))  # 클리어 타임 폰트 렌더링
            self.screen.blit(self.guide_font, (640 - self.guide_font.get_size()[0]/2, 310 - self.guide_font.get_size()[1]))
            self.screen.blit(self.font, (typingFontPos[0] + 5, typingFontPos[1]))
        else:
            self.leaderboard._draw(self.screen)
            for font in self.fonts:
                self.leaderboard.texture.blit(*font)
                self.fonts.remove(font)
        

    def handle_event(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            #재시작 버튼
            if self.restartbutton.get_rect().collidepoint(event.pos):
                print("Restart!!")
                self.manager.remove_scene_to_render(self.__class__.__name__)
                self.manager.play_time = 0.0
                self.manager.player_score = 0.0
                self.manager.add_scene_to_render('MainMenuScene')

            #텍스트 상자
            if self.input_box.get_rect().collidepoint(event.pos) and not self.isConfirmed:
                self.isTyping = True
                pygame.key.start_text_input()
            
            #확인 버튼
            if self.confirm_button.get_rect().collidepoint(event.pos) and not self.isConfirmed:
                if self.text.strip() != "":
                    pygame.key.stop_text_input()
                    #requests.post('http://api-dev.kro.kr:8080/register?name=' + self.player_name + '&score=' + player_score) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 점수 저장
                    print("점수 저장 꺼져있음!!!!!!!!!!!!!!!!!!!!!!")
                    print(self.text + ' -> ' + str(self.player_score))
                    self.load_ranking()
                    self.isConfirmed = True
                else:
                    #nickname이 비어있을 때
                    self.guide_font = utils.make_font_surface(self.font_size, None, 'nickname is blank', colors.RED)
                    self.guide_font_highlight_time = utils.seconds_to_frames(0.5)
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
            if len(self.text) < 10:
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

        ranking = [('1st', colors.GOLD), ('2nd', colors.SILVER), ('3rd', colors.BRONZE), ('4th', colors.BLACK), ('5th', colors.BLACK)]

        for x in range(0,5):
            if x < len(sorted_list):
                text = ranking[x][0] + ' : ' + sorted_list[x].get("name",'nothing') + ' -> ' + str(sorted_list[x].get("score",'nothing')) + 'P'
                print(text)
                self.fonts.append((utils.make_font_surface(50, "malgungothic", text, ranking[x][1]),(15,80*x)))