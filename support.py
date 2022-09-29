""" This module contains supporting functions and resources
for hangman22. """

import csv
import os

import pygame

from settings import WHITE

main_dir = os.path.split(os.path.abspath(__file__))[0]
assets_dir = os.path.join(main_dir, 'assets')

def load_image(name, colorkey=None):
    """The function to create an image surface from a file. 

    Args:
        name (str): The name of an image to load
        colorkey (tuple, optional): Sets the transparent colorkey. Defaults to None.
    
    Returns:
        A tuple containing the image surface and the image rect. 
    """
    fullname = os.path.join(assets_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect(left=5, top=40)

def load_sound(name):
    """The function to create a new Sound object from a file.  

    Args:
        name (str): The name of the sound file. 

    Returns:
        The named Sound object
    """
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join(assets_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load sound:', fullname)
        raise SystemExit(message)
    return sound

def read_flat_file(name, raw=False):
    """The function to read the contents of a flat file and return
    each line of the file as an item in a list.  

    Args:
        name (str): The name of the file to read. 
        raw (raw, optional): A switch to replace new line character 
        at the end of each line. Defaults to False.

    Returns:
        A list of each line. 
    """
    fullname = os.path.join(assets_dir, name)
    with open(fullname, 'r') as f:
        result = []
        for line in f.readlines():
            if not raw:
                line = line.replace('\n', '')
            result.append(line)
    return result

def read_csv_file(name):
    """A function to open and read csv

    Args:
        name (str): The name of the file to read. 
    
    Return:
        A sorted list of rows read from the file. 
    """
    fullname = os.path.join(assets_dir, name)
    
    with open(fullname, 'r') as f:
        csv_reader = csv.reader(f)
        data = []
        for row in csv_reader:
            data.append(row)
    # if data:
    #     data = sorted(data, key=lambda x: [int(x[2]), int(x[1])/int(x[2]), x[0]], reverse=True)
    return data

def write_csv_file(name, data):
    """A function to open and write csv. 

    Args:
        name (str): The name of the file on which to write. 
        data (obj): The data to write. 
    """
    fullname = os.path.join(assets_dir, name)    

    with open(fullname, 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f)
        wr.writerows(data)

def in_secret_word(secret, key):
    ''' a function to determine if the key value exists in the secret word
    
    Parameters:
        secret: str
            the secret word
        key: str
            a Unicode string of one character 

    Returns:
        bool
    '''
    # true if key is in secret else false
    return key in secret

def is_solved(secret):
    '''function to see if all solved properties are true'''
    count_of_sprites = len(secret)
    count_of_truths = 0
    for t in secret.sprites():
        if t.solved:
            count_of_truths += 1
    return count_of_truths == count_of_sprites

def blit_multi_line(surface, text, pos, font, color=WHITE):
    '''function to render each word and check how many words can fit 
    the screen by using `surface.get_width()`. Then blit the rest on the 
    other row which will be `surface.get_height()` pixels lower
    https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame'''
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0] # the width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surf = font.render(word, True, color)
            word_width, word_height = word_surf.get_size()
            if x + word_width >= max_width:
                x = pos[0] # reset the x.
                y += word_height # start on a new row.
            surface.blit(word_surf, (x, y))
            x += word_width + space
        x = pos[0] # reset the x.
        y += word_height

