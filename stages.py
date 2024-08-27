""" The stages for hangman22.  

class blueprints for :
    
    splash, active, outcome, credit, load, save
    
"""

import time
from datetime import datetime
from random import choice

import pygame

import classes as c
from settings import *
from support import (blit_multi_line, in_secret_word, is_solved,
                     read_flat_file, write_csv_file)

class Splash():
    """"The Splash Screen"""
    def __init__(self, app):
        self.stage = 'splash'
        self.app = app
        self.splash_screen_sprites = pygame.sprite.Group()
        self.button_sprites = pygame.sprite.Group()
        self.app.header = c.Header(self.app.screen, 'Hangman Simulation', self.app.font30, DARKTEXT)
        self.btn_splash_play = c.Button(self.app.width/2 - 80, 100, GREEN,         'Play',     self.app.font30)
        self.btn_splash_load = c.Button(self.app.width/2 - 80, 150, DODGERBLUE,    'Load',     self.app.font30)
        self.btn_splash_brag = c.Button(self.app.width/2 - 80, 200, DODGERBLUE,    'Credits',  self.app.font30)
        self.btn_splash_quit = c.Button(self.app.width/2 - 80, 250, LIGHTPINK,     'Quit',     self.app.font30)
        self.splash_screen_sprites.add(self.app.header, self.btn_splash_play,self.btn_splash_load, self.btn_splash_brag,self.btn_splash_quit)
        self.button_sprites.add(self.btn_splash_play,self.btn_splash_load, self.btn_splash_brag,self.btn_splash_quit)
    
    def on_event(self, event):
        """The method to handle pygame events. """
        if event.type == pygame.QUIT:
            self.app.is_running = False
        
        if event.type == pygame.MOUSEMOTION:
            for button in self.button_sprites.sprites():
                if type(button) == c.Button:
                    if button.rect.collidepoint(event.pos):
                        button.write_button_text(button.color_active, button.font)
                    else:
                        button.write_button_text(button.color_inactive, button.font)
        if event.type == pygame.MOUSEBUTTONDOWN:
             for button in self.button_sprites.sprites():
                user_response = button.check_click(event.pos)
                if user_response == 'Play':
                    self.app.game_state = 'active'
                elif user_response == 'Load':
                    self.app.game_state = 'load'
                elif user_response == 'Credits':
                    self.app.game_state = 'credit'
                elif user_response == 'Quit':
                    self.app.is_running = False
            
    def on_update(self):
        """The method to handle changes to game objects upon each cycle.  
        """
        self.splash_screen_sprites.update()
    
    def on_render(self):
        """The method to draw objects to the screen. """
        self.app.screen.blit(self.app.background, (0,0))
        self.splash_screen_sprites.draw(self.app.screen)
        pygame.display.flip()
    
    def run(self):
        """The method to control the Splash class. 
        """
        for event in pygame.event.get():
            self.on_event(event)
            self.on_update()
            self.on_render()

class Active():
    """The Active Playing Screen"""
    def __init__(self, app):
        """The Active screen constructor. """
        self.app = app
        self.stage = 'active'

        self.secret_word_list = self.app.secret_word_list 
        self.secret_word = ''
        self.result = ''
        self.gallows_index = 0
        self.gallows = [
            c.Gallows('hangman_0.png'),
            c.Gallows('hangman_1.png'),
            c.Gallows('hangman_2.png'),
            c.Gallows('hangman_3.png'),
            c.Gallows('hangman_4.png'),
            c.Gallows('hangman_5.png'),
            c.Gallows('hangman_6.png')]
 
        self.app.header = c.Header(self.app.screen, 'Play Hangman', self.app.font30, DARKTEXT)
        
        self.text_info_sprite = pygame.sprite.Sprite()
        self.text_info_sprite.name = 'text_info'
        self.text_info_sprite.image =pygame.Surface([self.app.width,16])
        self.text_sprites = pygame.sprite.Group()
        self.text_sprites.add(self.app.header, self.text_info_sprite)

        self.strike_zone = c.Strikezone(GRAY, 75, 230, self.app.font16)
        self.strike_zone_sprites = pygame.sprite.Group()
        self.strike_zone_sprites.add(self.strike_zone)
        self.strike_letter_sprites = pygame.sprite.Group()  # get added during the event loop

        self.popup_flag = False
        self.instruction_surf = pygame.sprite.Sprite()
        self.instruction_surf.image = pygame.Surface((140, 140))
        self.instruction_surf.image.fill(GRAY)
        self.instruction_surf.rect = self.instruction_surf.image.get_rect(center=
                                        (self.app.width/2, self.app.height/2))
        
        self.btn_instructions = c.Button(self.app.width/2-80, 
                                        self.app.height-55, 
                                        DODGERBLUE, "Instructions", self.app.font20)
        self.btn_exit = c.Button(self.app.width/2-80, 
                                 self.app.height-55, 
                                 LIGHTPINK, "Exit", self.app.font20)

        self.allsprites = pygame.sprite.Group()
        self.new_game()

    def get_secret_word_sprites(self,  secret):
        ''' a function to make the secret word sprites group
        
        Parameters:
            secret: str
                the secret word
        Return:
            secret_word_sprites: Group
                each sprite of the secret word grouped
        '''
        self.app.secret_word_sprites.empty()
        for letter_idx, letter in enumerate(secret):
            letter_block = c.Letter(letter_idx, letter, self.app.font30)
            self.app.secret_word_sprites.add(letter_block)

    def new_game(self):
        """The method to make the secret word sprites group. 
                Parameters:
                    secret: str
                        the secret word

                Return:
                    secret_word_sprites: Group
                        each sprite of the secret word grouped"""
        self.allsprites.empty()
        self.strike_letter_sprites.empty()
        self.gallows_index = 0
        self.secret_word = choice(self.secret_word_list)
        self.get_secret_word_sprites(self.secret_word)

        print(self.secret_word)

        if self.app.games == 0:
            percentage = 0
        else:
            percentage = (self.app.wins/self.app.games)
        self.text_info_sprite.image = self.app.font16.render(f'wins: {self.app.wins}   games: {self.app.games}   pct: {percentage:.2%}', True, DARKTEXT)
        self.text_info_sprite.rect = self.text_info_sprite.image.get_rect(center=(self.app.width / 2, 300))

        self.allsprites.add(self.text_sprites, self.app.secret_word_sprites, 
                            self.gallows[self.gallows_index], self.strike_zone_sprites, 
                            self.btn_instructions)
    

    def make_popup(self):
        """teh method to make the popup
        """
        self.width = self.app.width * 0.8
        self.height = self.app.height * 0.6
        self.popup_surf = pygame.Surface((self.width, self.height))
        self.popup_surf.fill(GRAY)
        instruction_text = (
            '        Instructions'
            '\n\n'
            'This is a guessing simulation. You try to guess the secret ' 
            'word by typing letters onto the keyboard.  '
            '\n\n'
            'Typing a letter not in the secret word will be a "strike" against '
            'you.  ' 
            '\n\n' 
            'Six strikes (6 missed letters) and you loose the game. '
            '\n\n')
        blit_multi_line(self.popup_surf, 
                        instruction_text, (15, 10), 
                        self.app.font16, color=DARKTEXT)

        self.popup_rect = self.popup_surf.get_rect()
        self.popup_rect.centerx = self.app.width/2
        self.popup_rect.centery = self.app.width/2
        self.app.screen.blit(self.popup_surf, self.popup_rect)
        pygame.draw.rect(self.app.screen, DARKGREEN, 
                        (self.popup_rect.left - 0, 
                        self.popup_rect.top, self.width + 8, self.height), 8)

    def on_event(self, event):
        """The method to handle user inputs."""
        if event.type == pygame.QUIT:
            self.app.is_running = False
        if event.type == pygame.MOUSEMOTION:
            for button in self.allsprites.sprites():
                if type(button) == c.Button:
                    if button.rect.collidepoint(event.pos):
                        button.write_button_text(button.color_active, button.font)
                    else:
                        button.write_button_text(button.color_inactive, button.font)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.allsprites.sprites():
                if type(button) == c.Button:
                    user_response = button.check_click(event.pos)
                    if user_response == 'Instructions':
                        self.popup_flag = True
                    if user_response == 'Exit':
                        self.popup_flag = False
                        self.allsprites.remove(self.instruction_surf, self.btn_exit)
                        self.allsprites.add(self.btn_instructions)
        
        
        
        if (event.type == pygame.KEYDOWN and 
            event.key > 96 and event.key < 123 
            and not is_solved(self.app.secret_word_sprites)):   
            keypressed = chr(event.key)
            if in_secret_word(self.secret_word, keypressed):
                for letter_index, letter in enumerate(self.secret_word):
                    if keypressed == letter:
                        self.app.secret_word_sprites.sprites()[letter_index].solved = True
                        pygame.mixer.Sound.play(self.app.good_sound)

                    if is_solved(self.app.secret_word_sprites):
                        self.app.result = 'won'
                        self.app.game_state = 'outcome'
                        self.app.outcome = Outcome(self.app)
                        self.allsprites.remove(self.btn_instructions)
                        break
            else:
                strike_block = c.Strike(self.gallows_index, keypressed, self.app.font30)
                self.strike_letter_sprites.add(strike_block)
                self.allsprites.add(self.strike_letter_sprites)
                self.gallows_index += 1
                pygame.mixer.Sound.play(self.app.bad_sound)
                if self.gallows_index < len(self.gallows) - 1:
                    self.allsprites.remove(self.gallows)
                    self.allsprites.add(self.gallows[self.gallows_index])
                else:
                    self.app.result = 'lost'
                    self.app.game_state = 'outcome'
                    self.allsprites.remove(self.gallows, self.btn_instructions)
                    self.allsprites.add(self.gallows[len(self.gallows)-1])
                    self.app.outcome = Outcome(self.app)

    def on_update(self):
        """The method to update the Active screen upon each cycle. """
        self.allsprites.update()

    def on_render(self):
        """The method to draw Active screen objects to the App.screen. """
        self.app.screen.blit(self.app.background, (0,0))
        self.allsprites.draw(self.app.screen)
        if self.popup_flag:
            self.allsprites.remove(self.btn_instructions)
            self.allsprites.add(self.btn_exit)
            self.make_popup()
        pygame.display.flip()
    
    def run(self):
        """The method to control the Active class. """
        for event in pygame.event.get():
            self.on_event(event)
            self.on_update()
            self.on_render()

class Outcome():
    """The stage to handle events when the player has played. """
    def __init__(self, app):
        """The Outcome constructor. """
        self.app = app
        #self.active = active
        self.allsprites = pygame.sprite.Group()

        self.text_info_sprite = pygame.sprite.Sprite()
        self.text_info_sprite.name = 'text_info'
        self.text_info_sprite.image =pygame.Surface([self.app.width,16])
        self.text_info_sprite.rect = self.text_info_sprite.image.get_rect(center=(self.app.width / 2, 300))
        self.text_sprites = pygame.sprite.Group()
        self.text_sprites.add(self.text_info_sprite)

        # if self.active.result == 'won':
        if self.app.result == 'won':
            self.app.header = c.Header(self.app.screen, "You're A Winner", self.app.font30, WHITE, GREEN)  
            self.app.wins +=1
            print(self.app.wins)
            self.app.games +=1
            self.text_info_sprite.image = self.app.font16.render(f'wins: {self.app.wins}   games: {self.app.games}   pct: {(self.app.wins/self.app.games):.2%}', True, DARKTEXT)
            self.text_info_sprite.rect = self.text_info_sprite.image.get_rect(center=(self.app.width / 2, 300))
        # if self.active.result == 'lost':
        if self.app.result == 'lost':
            self.app.header = c.Header(self.app.screen, "You've LOST", self.app.font30, RED)  
            self.app.games += 1
            # for letter in self.active.secret_word_sprites.sprites():
            for letter in self.app.secret_word_sprites.sprites():
                letter.solved = True
                # self.active.secret_word_sprites.add(letter)
                self.app.secret_word_sprites.add(letter)
            self.text_info_sprite.image = self.app.font16.render(f'wins: {self.app.wins}   games: {self.app.games}   pct: {(self.app.wins/self.app.games):.2%}', True, DARKTEXT)
            self.text_info_sprite.rect = self.text_info_sprite.image.get_rect(center=(self.app.width / 2, 300))
            pygame.mixer.Sound.play(self.app.bad_sound)

        self.btn_play_again = c.Button( 40, self.app.height - 55, GREEN,       'Play Again',   self.app.font20)
        self.btn_quit_game  = c.Button(220, self.app.height - 55, LIGHTPINK,   'Quit Game',    self.app.font20)
        self.button_sprites = pygame.sprite.Group()
        self.button_sprites.add(self.btn_play_again, self.btn_quit_game)     
        
        self.allsprites.add(self.app.header, self.text_sprites, self.button_sprites)
    
    def on_event(self, event):
        """The method to handle pygame events. """
        if event.type == pygame.QUIT:
            self.app.is_running = False
        
        if event.type == pygame.MOUSEMOTION:
            for button in self.button_sprites.sprites():
                if type(button) == c.Button:
                    if button.rect.collidepoint(event.pos):
                        button.write_button_text(button.color_active, button.font)
                    else:
                        button.write_button_text(button.color_inactive, button.font)

        if pygame.key.get_pressed()[pygame.K_RETURN] != 0:
            self.app.active.new_game()                    
            self.app.game_state = 'active'

        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.button_sprites.sprites():
                user_response = button.check_click(event.pos)
                if user_response == 'Play Again':
                    self.app.active.new_game()                    
                    self.app.game_state = 'active'

                if user_response == 'Quit Game':
                    
                    now = datetime.now()
                    data = list(self.app.high_scores)      # copy the app high scores
                    elibible_to_save = False
                    current_pct = self.app.wins/self.app.games

                    min_saved_pct = 1.0
                    for record in data:
                        if int(record[1])/int(record[2]) < min_saved_pct:
                            min_saved_pct = int(record[1])/int(record[2])
                    #print(min_saved_pct)
                    if current_pct >= min_saved_pct:     # eligible to test denominator    
                        data.append([str(now), self.app.wins, self.app.games])      

                        sorted_data_scores = list(sorted(data, key=lambda x: [int(x[1])/int(x[2]), int(x[2]), x[0]], reverse=True))
                        elibible_data = list(sorted_data_scores[0:5])

                        elibible_to_save = False
                        for lst in elibible_data:
                            if str(now) not in lst:
                                elibible_to_save = False                           
                            else:
                                elibible_to_save = True
                                break
                    
                    if elibible_to_save:
                        self.app.game_state = 'save'
                        self.app.save = Save(self.app)
                    else:
                        del self.app.active                     
                        self.app.active = Active(self.app)
                        self.app.active.new_game()       
                        self.app.wins = 0
                        self.app.games = 0               
                        self.app.game_state = 'splash'     

    def on_update(self):
        pass 

    def on_render(self):
        blank_header_surf = pygame.Surface([self.app.width,44])
        blank_header_surf.fill(GRAY)
        self.app.screen.blit(blank_header_surf, (0,0))
        blank_info_surf = pygame.Surface([self.app.width,16])
        blank_info_surf.fill(GRAY)
        self.app.screen.blit(blank_info_surf, (0,self.text_info_sprite.rect.y))
        self.allsprites.draw(self.app.screen)
        pygame.display.flip()
    
    def run(self):
        """The method to control the Outcome class. 
        """
        for event in pygame.event.get():

            self.on_event(event)
            self.on_update()
            self.on_render()

class Credit():
    """The object allowing the author to brag. """
    def __init__(self, app):
        """The Credit screen constructor. 

        Args:
            app (class): A reference to the App class.
        """
        self.app = app
        self.stage = 'Credits'
        self.app.header = c.Header(self.app.screen, 'Hangman Simulation', self.app.font30, DARKTEXT)

        self.info_sprite = pygame.sprite.Sprite()
        self.info_sprite.name = 'screen_info'
        margin_width = 20
        self.info_sprite.image = pygame.Surface((self.app.width - (2 * margin_width),
                                                self.app.height - (4 * margin_width)))
        self.info_sprite.image.fill(GRAY)
        self.info_sprite.rect = self.info_sprite.image.get_rect(topleft=(20, 50))
        credit_text = (
                    'This simulation has been uniquely \n' \
                    'designed and written by: \n\nAnthony B. Washington \n' \
                    'MIT License \n' \
                    'Copyright (c) 2022 dub-ab\n\n'
                    'Acknowledgements: \n'
                    '- HaelDB (Brandonmorris12@gmail.com) for the sound files. \n'
                    '- Clear Code (https://www.youtube.com/c/ClearCode) for inspiration. '
                    )
        blit_multi_line(self.info_sprite.image, credit_text, (0, 0), self.app.font16, color=DARKTEXT)
        self.btn_exit = c.Button(self.app.width/2-80, 300, LIGHTPINK, 'Exit', self.app.font20)
        self.allsprites = pygame.sprite.Group()
        self.allsprites.add(self.app.header, self.info_sprite, self.btn_exit)

    def on_event(self, event):
        """The method to handle inputs form the pygame event queue. 

        Args:
            event (event): An event from the event message queue. 
        """
        if event.type == pygame.QUIT:
            self.app.is_running = False
        if event.type == pygame.MOUSEMOTION:
            for button in self.allsprites.sprites():
                if type(button) == c.Button:
                    if button.rect.collidepoint(event.pos):
                        button.write_button_text(button.color_active, button.font)
                    else:
                        button.write_button_text(button.color_inactive, button.font)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.allsprites.sprites():
                if type(button) == c.Button:
                    user_response = button.check_click(event.pos)
                    if user_response == 'Exit':
                        self.app.active.new_game()
                        self.app.game_state = 'splash'

    def on_update(self):
        """The method to react to changes in the class variables"""
        pass

    def on_render(self):
        """The method to draw Credit objects to the App.screen.  
        """
        self.app.screen.blit(self.app.background, (0, 0))
        self.allsprites.draw(self.app.screen)
        pygame.display.flip()
    
    def run(self):
        """The method to control the Credit class. 
        """
        for event in pygame.event.get():
            self.on_event(event)
            self.on_update()
            self.on_render()

class Load():
    """The Load screen handles reading and rendering the highscore.json file. 
    """
    def __init__(self, app):
        """The Load screen constructor. 

        Args:
            app (class): A reference to the App class. 
        """
        self.app = app
        self.stage = 'Load'
        self.allsprites = pygame.sprite.Group()        
        self.app.header = c.Header(self.app.screen, 'High Scores', self.app.font30, WHITE, GREEN)

        self.hs = self.app.high_scores  # just to make it easier to write

        self.col_name = c.Tablecell('Name',     ( 30, 100), self.app.font20)
        self.col_wins = c.Tablecell('Wins',     (165, 100), self.app.font20)
        self.col_game = c.Tablecell('Games',    (230, 100), self.app.font20)
        self.col_pcnt = c.Tablecell('Pct.',     (318, 100), self.app.font20)
        self.underline = c.Tablecell('--------------------------------------------------------------------', (30, 110), self.app.font20)
            
        if self.hs:    
            self.hs_0_name = c.Tablecell(self.hs[0][3],                                             ( 30, 130), self.app.font20)
            self.hs_0_wins = c.Tablecell(self.hs[0][1],                                             (180, 130), self.app.font20)
            self.hs_0_game = c.Tablecell(self.hs[0][2],                                             (260, 130), self.app.font20)
            self.hs_0_pcnt = c.Tablecell("%10s" % f'{(int(self.hs[0][1])/int(self.hs[0][2])):0.2%}', (300, 130), self.app.font20)

            self.hs_1_name = c.Tablecell(self.hs[1][3],                                             ( 30, 160), self.app.font20)
            self.hs_1_wins = c.Tablecell(self.hs[1][1],                                             (180, 160), self.app.font20)
            self.hs_1_game = c.Tablecell(self.hs[1][2],                                             (260, 160), self.app.font20)
            self.hs_1_pcnt = c.Tablecell("%10s" % f'{(int(self.hs[1][1])/int(self.hs[1][2])):0.2%}', (300, 160), self.app.font20)

            self.hs_2_name = c.Tablecell(self.hs[2][3],                                             ( 30, 190), self.app.font20)
            self.hs_2_wins = c.Tablecell(self.hs[2][1],                                             (180, 190), self.app.font20)
            self.hs_2_game = c.Tablecell(self.hs[2][2],                                             (260, 190), self.app.font20)
            self.hs_2_pcnt = c.Tablecell("%10s" % f'{(int(self.hs[2][1])/int(self.hs[2][2])):0.2%}', (300, 190), self.app.font20)

            self.hs_3_name = c.Tablecell(self.hs[3][3],                                             ( 30, 220), self.app.font20)
            self.hs_3_wins = c.Tablecell(self.hs[3][1],                                             (180, 220), self.app.font20)
            self.hs_3_game = c.Tablecell(self.hs[3][2],                                             (260, 220), self.app.font20)
            self.hs_3_pcnt = c.Tablecell("%10s" % f'{(int(self.hs[3][1])/int(self.hs[3][2])):0.2%}', (300, 220), self.app.font20)

            self.hs_4_name = c.Tablecell(self.hs[4][3],                                             ( 30, 250), self.app.font20)
            self.hs_4_wins = c.Tablecell(self.hs[4][1],                                             (180, 250), self.app.font20)
            self.hs_4_game = c.Tablecell(self.hs[4][2],                                             (260, 250), self.app.font20)
            self.hs_4_pcnt = c.Tablecell("%10s" % f'{(int(self.hs[4][1])/int(self.hs[4][2])):0.2%}', (300, 250), self.app.font20)

            self.allsprites.add(self.hs_0_name, self.hs_0_wins, self.hs_0_game, self.hs_0_pcnt,
                                self.hs_1_name, self.hs_1_wins, self.hs_1_game, self.hs_1_pcnt,
                                self.hs_2_name, self.hs_2_wins, self.hs_2_game, self.hs_2_pcnt,
                                self.hs_3_name, self.hs_3_wins, self.hs_3_game, self.hs_3_pcnt,            
                                self.hs_4_name, self.hs_4_wins, self.hs_4_game, self.hs_4_pcnt)

        self.btn_exit = c.Button(self.app.width/2-80, 300, LIGHTPINK, 'Exit', self.app.font20)

        self.allsprites.add(self.app.header, 
            self.col_name, self.col_wins, self.col_game, self.col_pcnt,
            self.underline, self.btn_exit)
    
    def on_event(self, event):
        """The method to respond to events in the pygame event queue. 

        Args:
            event (Eventlist): A message from the event queue.  
        """
        if event.type == pygame.QUIT:
            self.app.is_running = False
        elif event.type == pygame.MOUSEMOTION:
            for button in self.allsprites.sprites():
                if type(button) == c.Button:
                    if button.rect.collidepoint(event.pos):
                        button.write_button_text(button.color_active, button.font)
                    else:
                        button.write_button_text(button.color_inactive, button.font)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.allsprites.sprites():
                if type(button) == c.Button:
                    user_response = button.check_click(event.pos)
                    if user_response == 'Exit':
                        self.app.active.new_game()
                        self.app.game_state = 'splash'


    def on_update(self):
        """The method to update values upon each cycle. 
        """
        pass

    def on_render(self):
        """The method to draw objects to the App.screen 
        """
        self.app.screen.blit(self.app.background, (0,0))
        
        self.allsprites.draw(self.app.screen)
        

        pygame.display.flip()

    def run(self):
        """The method to control the Load class.  
        """
        for event in pygame.event.get():
            self.on_event(event)
            self.on_update()
            self.on_render()

class Save():
    """The Save class handles gathering and writing game data to the highscore.json file. 
    """
    def __init__(self, app):
        """The Save screen constructor

        Args:
            app (class): A reference to the App class
            data (list): The list of data to be saved
        """
        self.app = app
        self.data = self.app.high_scores
        self.stage = 'Save'
        self.allsprites = pygame.sprite.Group()
        self.app.header = c.Header(self.app.screen, 'Save Game?', self.app.font30, RED)
        
        self.info_sprite = pygame.sprite.Sprite()
        self.info_sprite.image = pygame.Surface((self.app.width - 60,
                                                self.app.height - 205))
        self.info_sprite.image.fill(GRAY)        
        self.info_sprite.rect = self.info_sprite.image.get_rect(center=(self.app.width/2, self.app.height/2 - 50))
        
        self.text1 = pygame.sprite.Sprite()
        self.text1.image = self.app.font20.render('Your score ranks among the best!', True, DARKTEXT)
        self.text1.rect = self.text1.image.get_rect(center=(self.app.width/2, self.info_sprite.rect.top + 20))

        self.text2 = pygame.sprite.Sprite()
        self.text2.image = self.app.font20.render('Enter your name into the box below:', True, DARKTEXT)
        self.text2.rect = self.text2.image.get_rect(center=(self.app.width/2, self.info_sprite.rect.top + 80))
        
        # input textbox to get the name 
        self.input_box = pygame.Rect(self.app.width/2-60,self.app.height/2, 120,24)
        #self.color_inactive = DODGERBLUE
        self.color = GREEN
        #self.color = self.color_inactive
        self.is_active = True
        # get datetime to store in record
        self.btn_continue = c.Button(self.app.width/2-80, 300, DODGERBLUE, 'Continue', self.app.font20)
        
        self.player_name = ''
        self.player_name_surf = pygame.sprite.Sprite()
        self.player_name_surf.image = self.app.font20.render(self.player_name, True, DARKTEXT)
        self.player_name_surf.rect = self.player_name_surf.image.get_rect(topleft=(self.input_box.x+5, self.input_box.y+5))

        self.cursor = pygame.Rect(self.player_name_surf.rect.topright, (3, self.player_name_surf.rect.height-3))

        self.allsprites.add(self.app.header, self.btn_continue, 
        self.info_sprite, self.text1, self.text2, self.player_name_surf)


    def on_event(self, event):
        """The method to handle inputs from the pygame event queue. 

        Args:
            event (event): An event from the event message queue. 
        """
        if event.type == pygame.QUIT:
            self.app.is_running = False
        if event.type == pygame.MOUSEMOTION:
            for button in self.allsprites.sprites():
                if type(button) == c.Button:
                    if button.rect.collidepoint(event.pos):
                        button.write_button_text(button.color_active, button.font)
                    else:
                        button.write_button_text(button.color_inactive, button.font)
        if event.type == pygame.MOUSEBUTTONDOWN:

            for button in self.allsprites.sprites():
                if type(button) == c.Button:
                    user_response = button.check_click(event.pos)
                    if user_response == 'Continue':
                        self.save()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.save()
            if event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            else:                        
                if len(self.player_name) > 11:
                    pygame.mixer.Sound.play(self.app.bad_sound)
                    self.player_name[:-1]
                else:
                    self.player_name += event.unicode
                    
                # cursor
            self.player_name_surf.image = self.app.font20.render(self.player_name, True, DARKTEXT)
            self.player_name_surf.rect.size = self.player_name_surf.image.get_size()
            self.cursor.topleft = self.player_name_surf.rect.topright

    def save(self):
        now = datetime.now()
        self.app.high_scores.append([str(now), self.app.wins, self.app.games, self.player_name])
        sorted_high_scores = list(sorted(self.app.high_scores, key=lambda x: [int(x[1])/int(x[2]), int(x[2]), x[0]], reverse=True))
        self.app.high_scores = list(sorted_high_scores[0:5])
        write_csv_file('highscores.csv', self.app.high_scores)
        self.player_name = ' '
        self.app.active.new_game()
        self.app.wins = 0
        self.app.games = 0
        self.app.game_state = 'load'
        self.app.load = Load(self.app)
                            
                        
                        

    def on_update(self):
        """The method to react to changes in the class variables"""
        pass


    def on_render(self):
        """The method to draw Save screen objects to the App.screen. """
        self.app.screen.blit(self.app.background, (0, 0))
        self.allsprites.draw(self.app.screen)       
        pygame.draw.rect(self.app.screen, self.color, self.input_box, 3)        
        # cursor is made to blink after every 0.5 sec
        if time.time() % 1 > 0.5:
            pygame.draw.rect(self.app.screen, RED, self.cursor)
        
        pygame.display.flip()

    def run(self):
        """The method to control the Save class. """
        for event in pygame.event.get():
            self.on_event(event)
            self.on_update()
        #self.on_render()
        self.app.screen.blit(self.app.background, (0, 0))
        self.allsprites.draw(self.app.screen)       
        pygame.draw.rect(self.app.screen, self.color, self.input_box, 3)        
        # cursor is made to blink after every 0.5 sec
        if time.time() % 1 > 0.5:
            pygame.draw.rect(self.app.screen, RED, self.cursor)
        
        pygame.display.flip()
  
