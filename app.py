
"""The app module is the main entry point of the hangman22 simulation."""

__author__      = "Anthony B. Washington"
__license__     = 'MIT'  # https://mit-license.org/

import os
import sys

import pygame

import classes as c
from settings import *
from stages import *
from support import load_sound, read_csv_file, main_dir, assets_dir, read_flat_file

class App():
    """ The main application and state manager. 
    """
    def __init__(self):
        """ The App class constructor.  The method to initialize pygame modules 
        and application wide variables.  
        """
        self.main_dir = main_dir
        self.asset_dir = assets_dir
        pygame.init()
        self.is_running = True
        self.size = self.width, self.height = GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT       
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Hangman Simulation')
        self.app_clock = pygame.time.Clock()

        # prepre font resources
        if pygame.font:
            font_name = os.path.join(assets_dir, 'JAi_____.TTF')
            self.font30 = pygame.font.Font(None, 34)
            self.font20 = pygame.font.Font(None,24)
            self.font16 = pygame.font.Font(font_name,16)
        # prepare mixer resources
        if pygame.mixer:
            self.good_sound = load_sound('_ding.wav')
            #pygame.mixer.Sound.set_volume(self.good_sound, 0.1)
            self.bad_sound = load_sound('_wrong.wav')
            pygame.mixer.Sound.set_volume(self.bad_sound, 0.5) 

        # create the background
        self.background = pygame.Surface(self.size)
        self.background = self.background.convert()
        self.background.fill(GRAY)

        self.header = c.Header(self.screen, '', self.font30, GRAY)

        # perpare game objects
        self.game_state = 'active'
        self.wins = 0
        self.games = 0       
        self.result = ''
        self.high_scores = read_csv_file('highscores.csv')
        self.secret_word_list = read_flat_file('wordlist.txt')
        self.secret_word_sprites = pygame.sprite.Group()
    

        self.splash = Splash(self)
        self.active = Active(self)
        self.outcome = Outcome(self)
        self.credit = Credit(self)
        self.load = Load(self)
        self.save = Save(self) 
        


    def on_execute(self):
        """The method to start the application.  """

        while( self.is_running ):
            # test game_states
            if self.game_state == 'splash':
                self.splash.run()
            elif self.game_state == 'active':
                self.active.run()
            elif self.game_state == 'outcome':
                self.outcome.run()
            elif self.game_state == 'credit':
                self.credit.run()
            elif self.game_state == 'load':
                self.load.run()
            elif self.game_state == 'save':
                self.save.run()

        self.app_clock.tick(60)
        pygame.quit()
        sys.exit()

if __name__ == "__main__" :
    app = App()
    app.on_execute()
