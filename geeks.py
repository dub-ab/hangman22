# import pygame module
import pygame

# import time module
import time

# initialize the pygame module
pygame.init()

# set the window screen size
display_screen = pygame.display.set_mode((500, 500))

# add some text
text = 'Hello Guys!!'

# add default font style with font
# size
font = pygame.font.SysFont(None, 40)

# render the text
img = font.render(text, True, (255, 0, 0))

rect = img.get_rect()
rect.topleft = (20, 20)
cursor = pygame.Rect(rect.topright, (3, rect.height))

running = True

while running:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		# detect if key is physically
		# pressed down
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE:
				if len(text) > 0:
					
					# stores the text except last
					# character
					text = text[:-1]

			else:
				text += event.unicode
				
			img = font.render(text, True, (255, 0, 0))
			rect.size = img.get_size()
			cursor.topleft = rect.topright

	# Add background color to the window screen
	display_screen.fill((200, 255, 200))
	display_screen.blit(img, rect)
	
	# cursor is made to blink after every 0.5 sec
	if time.time() % 1 > 0.5:
		pygame.draw.rect(display_screen, (255, 0, 0), cursor)
		
	# update display
	pygame.display.update()

pygame.quit()
