""" This module holds the class objects for hangman22. """

import pygame

from settings import DARKTEXT, DODGERBLUE, GRAY, LIGHTPINK, NAVY, RED, WHITE
from support import load_image

class Button(pygame.sprite.Sprite):
    '''the play again button object
    
    Attributes:
        x: int
            x position of the button
        y: int
            y position of the button
        width: int
            the width of the button
        height: int
            the height of the button
        color: 
            the button color
        label_text: str
            the button label text
        
        
    '''
    def __init__(self, x, y, color, label_text, font):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.x = x
        self.y = y
        self.width = 160
        self.height = 40
        self.color_inactive = color
        self.color_active = (self.color_inactive.r, 
                             self.color_inactive.g + self.color_inactive.g * .35, 
                             self.color_inactive.b)
        self.label = label_text
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color_inactive)
        self.font = font
        label_text = self.font.render(self.label, True, DARKTEXT)
        self.image.blit(label_text, label_text.get_rect(center=(self.width / 2, self.height / 2)))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    
    def write_button_text(self, btn_colour, font):
        self.image.fill(btn_colour)
        text = font.render(self.label, True, DARKTEXT)
        self.image.blit(text, text.get_rect(center=(self.width / 2, self.height / 2)))
 
    def check_click(self, mouse):
        '''return text value if mouse and button collide'''
        if self.rect.collidepoint(mouse):
            return self.label

    def update(self):
        '''method to update the button on each cycle'''
        #self.handle_event(event)
        pass

class Header(pygame.sprite.Sprite):
    '''
    A sprite that represents the header section of the screen.
    
    Parameters:
        surface: Surface
            The surface on which to place the header.
        font: Font
            the font used to render the header text 
        text: str
            the header text
        margin: int  (default: 10)
            interger value to offset 
    Attributes:
        margin: int
            the distance between the display edge and the header edge
        image: Surface
            the sprite image of the header
        rect: Rect
            the position and dimensions of the image

    '''
    def __init__(self, surface, text, font, color=DARKTEXT, bg_color=GRAY, margin=10) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.margin = margin

        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(235/2,30/2))
        bg_surf = pygame.Surface([235, 30], pygame.SRCALPHA)
        bg_surf.fill(bg_color)
        bg_surf = bg_surf.copy().convert_alpha()

        bg_surf.blit(text_surf,text_rect)


        self.image = bg_surf.copy().convert_alpha()
        self.rect = self.image.get_rect(topleft=[self.margin, (1.5 * self.margin)])
        self.rect.centerx = surface.get_width() /2

class TextBlock(pygame.sprite.Sprite):
    '''a sprite image used to hold rows of text
        
        Parameters:
            text: str
                the text
            font: Font
                the font used to render the text  
            margin: int  (default: 10)
                interger value to offset 
        
        Attributes:
            margin: int
            text_surf: Surface
            image: Surface
            rect: Rect
    '''
    def __init__(self, surface, text, font=None, margin=10) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface

        if font is None:
            font = pygame.font.Font(None, 16)
        else:
            font = font
        self.margin = margin
        textblock_surf = self.blit_multi_line(self.surface,text, (20,75), font, )
        self.image = textblock_surf.copy().convert_alpha()
        self.rect = self.image.get_rect()
    
    def blit_multi_line(self,surface, text, pos, font, color=('black')):
        '''function to render each word and check how many words can fit 
        the screen by using `surface.get_width()`. Then blit the rest on the 
        other row which will be `surface.get_height()` pixels lower
        https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame'''
        
        surface_size = self.surface.get_size()
        credits_surf = pygame.Surface((surface_size), pygame.SRCALPHA)
        #credits_surf.fill('grey')
        
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0] # the width of a space.
        max_width, max_height = surface_size
        x, y = pos
        for line in words:
            for word in line:
                word_surf = font.render(word, True, color)
                word_width, word_height = word_surf.get_size()
                if x + word_width >= max_width - self.margin:
                    x = pos[0] # reset the x.
                    y += word_height # start on a new row.
                credits_surf.blit(word_surf, (x, y))
                x += word_width + space
            x = pos[0] # reset the x.
            y += word_height
        return credits_surf

class Gallows(pygame.sprite.Sprite):
    '''
    the gallows sprite object
    '''
    def __init__(self, image) -> None:
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image(image, -1)

    def update(self, *args):
        ''' the method to update the gallows object'''
        pass

# superclass for letter blocks and strike blocks
class Block(pygame.sprite.Sprite):
    '''The Block sprite object '''
    def __init__(self, index, letter, font):
        '''the block constructor'''
        pygame.sprite.Sprite.__init__(self)
        self.block_idx = index
        self.character = letter
        self.font = font
        self.image = pygame.Surface([30, 33])
        self.rect = self.image.get_rect()
        self.field = pygame.Surface([self.rect.width, 30])
        self.field_rect = self.field.get_rect()

class Letter(Block):
    ''' 
    the class managing a correctly guessed letter in the secret word.

    Attributes
        letter_index : int
            the index of the letter 
        letter : str
            a letter which is not in the secret word

    Methods 
        update():
            manage the state of the Letter on each cycle

    '''
    def __init__(self, letter_index, letter, font):
        '''the letter constructor'''
        Block.__init__(self, letter_index, letter, font)
        self.block_idx = letter_index
        self.font = font
        self.rect = self.image.get_rect(topleft=(self.image.get_width() + (34*self.block_idx), 325))
        self.image.fill(NAVY)        
        self.field.fill(DODGERBLUE)
        self.image.blit(self.field, self.field_rect)
        self.solved = False


    def update(self, *args):
        '''the method to update the letter on each cycle'''
        if self.solved:
            text = self.font.render(self.character, False, WHITE)
            textpos = text.get_rect(center=(self.rect.width / 2, self.rect.height / 2))
            self.image.blit(text, textpos)

class Strike(Block):
    ''' 
    The class managing a guess not in the secret word.

    Attributes
        letter_index : int
            the index of the letter 
        letter : str
            a letter which is not in the secret word

    Methods 
        update():
            manage the state of the Strike object on each cycle
    '''
    def __init__(self, strike_index,letter, font) -> None:
        '''the strike constructor'''
        Block.__init__(self, strike_index, letter, font)  # call Block initializer
        self.block_idx = strike_index
        self.font = font
        self.rect = self.image.get_rect(topleft=(321, 75  + (34*self.block_idx)))
        self.image.fill(RED)
        self.field.fill(LIGHTPINK)
        self.image.blit(self.field, self.field_rect)


    def update(self, *args):
        '''the method to update the strike on each cycle'''
        text = self.font.render(self.character, False, DARKTEXT)
        textpos = text.get_rect(center=(self.rect.width / 2, self.rect.height / 2))
        self.image.blit(text, textpos)

class Strikezone(pygame.sprite.Sprite):
    '''an area to hold the strike sprites''' 
    def __init__(self, color, width, height, font):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect(topleft=(300,50))
        
        text = font.render('Strikes', True, color)
        textpos = text.get_rect(centerx=self.image.get_width() / 2, top=4)
        self.image.blit(text, textpos)
    
    def update(self, *args):
        '''the method to update the strike zone'''
        pass

class Tablecell(pygame.sprite.Sprite):
    '''A Sprite to who's surface holds a value.''' 
    def __init__(self, value, pos, font):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(str(value), True, DARKTEXT)
        self.rect = self.image.get_rect(topleft=(pos))
    
    def update(self):
        """The update method for the sprite. """
        pass
