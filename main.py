import math
import numpy
import pygame
from pygame.locals import *
import pygame_gui
import random
import sys

# Define some colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255,255,0)
WHITE = (255, 255, 255)
BRIGHTORANGE = (255, 174, 0)
SILVER = (192,192,192)
GRAY = (128,128,128)
MAROON = (128,0,0)
PURPLE = (128,0,128)
CORN_FLOWER_BLUE = (100,149,237)
DARK_GREEN = (8, 76, 8)
DARK_BLUE = (29, 80, 255)

is_paused = False
# initialize variables

# used to identify where to go when previous screen button pressed
curr_screen = None
prev_screen = None

# pygame initialization
pygame.init()
clock = pygame.time.Clock()

# set window + dock icon
display_height = 800
display_width = 800
display_size = (display_width, display_height)
display = pygame.display.set_mode(display_size, 0, 32)
manager = pygame_gui.UIManager(display_size, 'themes/button_themes.json')

dock_icon = pygame.image.load('images/dock_icon.png')
main_bg = pygame.image.load('images/bg_main.png')

pygame.display.set_caption("Fake Doodle Jump")
pygame.display.set_icon(dock_icon)

pygame.key.set_repeat(10, 10)

# set background
display.fill(GRAY)

# creates surface with same size as window - draw/create shapes on it
background = pygame.Surface(display_size)
display.blit(background, (0, 0))

pygame.display.update()

class MasterSprite(pygame.sprite.Sprite):
	def __init__(self, image, x = 0, y = 0):

		self.x = x
		self.y = y
		self.image = pygame.image.load(image)
		self.rect = self.image.get_bounding_rect()
		self.rect.x = x
		self.rect.y = y
		self.display_size = pygame.display.get_surface().get_size()

	def move_right(self, pixels):
		self.x += pixels
		self.rect.x += pixels

	def move_left(self, pixels):
		self.x -= pixels
		self.rect.x -= pixels

	def move_up(self, pixels):
		self.y -= pixels
		self.rect.y -= pixels

	def move_down(self, pixels):
		self.y += pixels
		self.rect.y += pixels

	def get_rect(self):
		return self.rect

	def get_surface(self):
		return self.image

	def set_x(self, x):
		self.x = x
		self.rect.x = x

	def set_y(self, y):
		self.y = y
		self.rect.y = y

	def set_xy(self, x, y):
		self.set_x(x)
		self.set_y(y)

class Player(MasterSprite):
	def __init__(self, x, y):

		super().__init__('images/ninja.png')

		self.rotate = -15
		self.image = pygame.transform.rotate(self.image, self.rotate)
		self.image.convert_alpha()
		self.og_image = self.image
		self.flip_x = False

		self.set_xy(x, y)

		self.can_jump = True
		self.latest_landing_y = self.rect.y
		self.latest_landing_x = self.rect.x
		self.max_jump_height = self.latest_landing_y - 200
		self.latest_landing_x_width = self.latest_landing_x
	
	def validate_jump(self):
		
		if self.rect.y >= self.latest_landing_y and self.rect.x >= self.latest_landing_x and self.rect.x <= self.latest_landing_x_width:
			self.can_jump = True
		
		if self.rect.y <= self.max_jump_height:
			self.can_jump = False

	def image_transformations(self):
		self.image = pygame.transform.flip(self.og_image, self.flip_x, False)
		self.image = pygame.transform.rotate(self.image, self.rotate)

	def move(self, event, move_size):

		self.validate_jump()
		
		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_UP: 

				if self.can_jump == True:

					if self.flip_x == False:
						self.rotate = 15
					else:
						self.rotate = -15

					self.image_transformations()

					self.move_up(move_size)

			elif event.key == pygame.K_DOWN:

				if self.flip_x == False:
					self.rotate = -105
				else:
					self.rotate = 105

				self.image_transformations()

				self.move_down(move_size)

			elif event.key == pygame.K_LEFT:
				self.flip_x = True
				self.rotate = 0
				self.image_transformations()

				self.move_left(move_size)

			elif event.key == pygame.K_RIGHT:
				self.flip_x = False
				self.rotate = 0
				self.image_transformations()

				self.move_right(move_size)
		
		elif event.type == pygame.KEYUP:
			self.rotate = 0
			self.image_transformations()

	def gravity(self):

		self.move_down(8)

		if self.rect.y > (display_height - 68):
			self.rect.y = display_height - 68

	def update(self, event, move_size):

		self.move(event, move_size)

		if self.rect.x > (display_width - 68):
			self.rect.x = display_width - 68

		if self.rect.x < 0:
			self.rect.x = 0

		if self.rect.y < 0:
			self.rect.y = 0

		if self.rect.y > (display_height - 68):
			self.rect.y = display_height - 68


class Platform(MasterSprite):
	def __init__(self, x, y, w, h):

		pygame.sprite.Sprite.__init__(self)
		super().__init__('images/platform_blue.png')

		self.w = w
		self.h = h

		self.image = pygame.transform.scale(self.image, (self.w, self.h))
		self.image.convert_alpha()
		self.og_image = self.image

		self.set_xy(x, y)

	def change_pic(self, new_img):

		self.image = pygame.image.load(new_img)
		self.image = pygame.transform.scale(self.image, (self.w, self.h))

	def gravity(self, amount):

		self.move_down(amount)

		if self.rect.y > display_height:
			self.kill()

# quickly create objects (rects)
def text_objects(text, font, colour):

	text_surf = font.render(text, True, colour)
	return text_surf, text_surf.get_rect()

# basic game functions
def quit_game():
	pygame.quit()
	sys.exit()
	quit()

def unpause():
	global is_paused
	is_paused = False

def pause():

	# LargeText = pygame.font.SysFont("Keyboard.ttf", 115)
	# TextSurf, TextRect = TextObjects("Paused", LargeText)
	# TextRect.center = ((display_width/2), (display_height/2))
	# GameDisplay.blit(TextSurf, TextRect)

	# while is_paused:
	# 	for event in pygame.event.get():
	# 		#print(event)
	# 		if event.type == pygame.QUIT:
	# 			pygame.quit()
	# 			quit()

	# 	#GameDisplay.fill(Blue)

	# 	Button("CONTINUE", 250, 450, 100, 50, Green, BrightGreen, unpause)
	# 	Button("RETURN", 450, 450, 100, 50, Orange, BrightOrange, Introduction)
	# 	Button("QUIT", 650, 450, 100, 50, Red, BrightRed, quit_game)

	# 	pygame.display.update()
	# 	Clock.tick(15)

	pass

# go back to previous window/screen when p pressed on keyboard
def return_to_prev_screen(prev_screen, curr_screen):

	if prev_screen is None:
		return 'intro', prev_screen, curr_screen

	elif prev_screen == 'instructions':
		return 'instructions', prev_screen, curr_screen

	elif prev_screen == 'intro':
		return 'intro', prev_screen, curr_screen
	
	elif prev_screen == 'main':
		return 'main', prev_screen, curr_screen

	else:
		return 'intro', prev_screen, curr_screen

# run window/screen based on user's choices
def screen_to_run(wdw, prev_screen, curr_screen):

	if wdw is False:
		quit_game()

	elif wdw == 'intro':
		return Introduction(prev_screen, curr_screen).display_screen()

	elif wdw == 'instructions':
		return Instructions(prev_screen, curr_screen).display_screen()
	
	elif wdw == 'main':
		return Main(prev_screen, curr_screen).display_screen()

	elif wdw == 'return_to_prev_screen':
		return return_to_prev_screen(prev_screen, curr_screen)

	else:
		return Introduction(prev_screen, curr_screen).display_screen()

	return wdw, prev_screen, curr_screen

# parent class for all screens
class Screen:
	def __init__(self, prev_screen, curr_screen):

		self.prev_screen = prev_screen
		self.curr_screen = curr_screen

	def set_prev_curr_screen(self, curr):
		
		try:
			self.prev_screen = self.curr_screen

		except UnboundLocalError:
			self.prev_screen = 'intro'

		self.curr_screen = curr
	
	def clear_screen(self):

		# set window + clear screen
		self.manager = pygame_gui.UIManager(display_size, 'themes/button_themes.json')

	def draw_title_text(self, text, size, x, y, colour):

			# title Fake Doodle Jump at top of the screen
			title_text_font = pygame.font.Font('fonts/Montserrat-Bold.ttf', size)
			text_surf, text_rect = text_objects(text, title_text_font, colour)
			text_rect.center = (x, y)
			display.blit(text_surf, text_rect)

	def draw_multiple_text(self, text, size, x, y, colour):

		# instructions' text
		text_line_font = pygame.font.Font('fonts/Montserrat-Regular.ttf', size)
		controls_text = text

		# put instructions on the screen
		for i in range(len(controls_text)):
			display.blit(text_line_font.render(controls_text[i], 1, colour), (x, (y * (i + 1))))

	def clock_sync(self):

		# don't load faster than needed
		clock.tick(60) / 1000
		self.time_delta = clock.tick(60) / 1000

	def universal_keyboard_events(self, event):

		# red x on top left of every window = quit
		if event.type == pygame.QUIT:
			quit_game()

		if event.type == pygame.KEYDOWN:

			# press escape to quit
			if event.key == pygame.K_ESCAPE:
				quit_game()

			# press backspace to go to previous screen/window
			if event.key == pygame.K_BACKSPACE:
				return ['return_to_prev_screen', self.prev_screen, self.curr_screen]
		
		return [None, None, None]

# screen game opens with
class Introduction(Screen):
	def create_buttons(self):

		# instructions button under title
		self.instructions_btn = pygame_gui.elements.UIButton(
		relative_rect = pygame.Rect((300, 200), (200, 100)),
		text = 'Instructions', manager = self.manager, object_id = '#instructions')

		# play game button
		self.play_game_btn = pygame_gui.elements.UIButton(
		relative_rect = pygame.Rect((100, 400), (200, 100)),
		text = 'Play Game', manager = self.manager, object_id = '#play_game')

		# quit button
		self.quit_btn = pygame_gui.elements.UIButton(
		relative_rect = pygame.Rect((500, 400), (200, 100)),
		text = 'Quit', manager = self.manager, object_id = '#quit')

	def local_keyboard_events(self, event):

		# press i to see instructions
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_i:
				return ['instructions', self.prev_screen, self.curr_screen]
		
		return [None, None, None]

	def local_button_events(self, event):

		if event.type == pygame.USEREVENT:
			# where to go when buttons clicked
			if event.user_type == pygame_gui.UI_BUTTON_PRESSED:

				if event.ui_element == self.instructions_btn:
					return 'instructions', self.prev_screen, self.curr_screen
				
				if event.ui_element == self.play_game_btn:
					return 'main', self.prev_screen, self.curr_screen

				if event.ui_element == self.quit_btn:
					quit_game()
		
		return [None, None, None]

	def display_screen(self):
		
		self.set_prev_curr_screen('intro')
		self.clear_screen()

		display.fill(GRAY)

		self.create_buttons()
		self.draw_title_text('FAKE DOODLE JUMP', 50, (display_width / 2), (display_height / 8), BLACK)

		while True:

			self.clock_sync()

			for event in pygame.event.get():

				universal_k_event = self.universal_keyboard_events(event)
				local_k_event = self.local_keyboard_events(event)
				local_b_event = self.local_button_events(event)
				
				if universal_k_event[0] != None:
					return universal_k_event[0], universal_k_event[1], universal_k_event[2]

				if local_k_event[0] != None:
					return local_k_event[0], local_k_event[1], local_k_event[2]

				if local_b_event[0] != None:
					return local_b_event[0], local_b_event[1], local_b_event[2]

				self.manager.process_events(event)
			self.manager.update(self.time_delta)

			# display.blit(background, (0, 0))
			self.manager.draw_ui(display)
			pygame.display.flip()

# screen with instruction
class Instructions(Screen):
	def local_keyboard_events(self, event):

		if event.type == pygame.KEYDOWN:
			# press m to go the intro screen
			if event.key == pygame.K_m:
				return 'intro', self.prev_screen, self.curr_screen
		
		return [None, None, None]

	def draw_small_title_text(self, text, size, x, y, colour):

		text_line_font = pygame.font.Font('fonts/Montserrat-Regular.ttf', size)
		text_line_0 = text_line_font.render(text, 1, colour)
		display.blit(text_line_0, (x, (y * 0)))

	def display_screen(self):

		self.set_prev_curr_screen('instructions')
		self.clear_screen()

		display.fill(DARK_GREEN)

		while True:

			self.clock_sync()

			for event in pygame.event.get():

				universal_k_event = self.universal_keyboard_events(event)
				local_k_event = self.local_keyboard_events(event)
				
				if universal_k_event[0] != None:
					return universal_k_event[0], universal_k_event[1], universal_k_event[2]

				if local_k_event[0] != None:
					return local_k_event[0], local_k_event[1], local_k_event[2]

				self.manager.process_events(event)
			self.manager.update(self.time_delta)

			self.draw_small_title_text('Controls:', 25, 5, 27, YELLOW)
			self.draw_multiple_text(['- To quit, either click the red button at the top left, or press', '   esc on the keyboard.', '- To go back to the previous page you were on, press', '   backspace on the keyboard.', '- To open up this page again, press i on the keyboard.', '- To go back to the main page, press m on the keyboard.', '- To move the main sprite, use the arrow keys.', '- To pause the game, press p on the keyboard.', '- You can click on any buttons - buttons always light up when ', '   they are hovered over.'], 25, 5, 27, WHITE)

			self.manager.draw_ui(display)
			pygame.display.flip()

# main gameplay screen
class Main(Screen):
	def local_keyboard_events(self, event):
	
		if event.type == pygame.KEYDOWN:
			# press m to go the intro screen
			if event.key == pygame.K_m:
				return 'intro', self.prev_screen, self.curr_screen

			# press i to see instructions
			if event.key == pygame.K_i:
				return ['instructions', self.prev_screen, self.curr_screen]

		return [None, None, None]

	def display_screen(self):

		self.set_prev_curr_screen('main')
		self.clear_screen()

		possible_gravities = []

		for x in range(4, 19):
			possible_gravities.append(x / 4)
		
		print(possible_gravities)

		user = Player(368, 666)
		first_platform = Platform(325, 730, 150, 15)

		platforms = pygame.sprite.Group()

		for platform_number in range(random.randint(5, 7)):
			plat = Platform(random.randint(0, 550), random.randint((user.rect.y // 4), (user.rect.y - 50)), random.randint(100, 250), 15)
			platforms.add(plat)

		display.blit(main_bg, (0, 0))

		while True:

			self.clock_sync()

			if user.get_rect().colliderect(first_platform.get_rect()) and first_platform.rect.y <= 800:
				pass
			elif first_platform.rect.y >= display_height:
				user.gravity()
			else:
				first_platform.gravity(1.5)
				user.gravity()

			for platform in platforms:
				platform.gravity(possible_gravities[random.randint(0, 6)])
			
			for platform in platforms:
				if user.get_rect().colliderect(platform.get_rect()):
					user.latest_landing_y = user.rect.y
					user.latest_landing_x = user.rect.x
					user.latest_landing_x_width = user.latest_landing_x + platform.rect.w

			for event in pygame.event.get():

				user.update(event, 10)

				universal_k_event = self.universal_keyboard_events(event)
				local_k_event = self.local_keyboard_events(event)
				
				if universal_k_event[0] != None:
					return universal_k_event[0], universal_k_event[1], universal_k_event[2]

				if local_k_event[0] != None:
					return local_k_event[0], local_k_event[1], local_k_event[2]

				self.manager.process_events(event)
			self.manager.update(self.time_delta)

			display.blit(main_bg, (0, 0))
			display.blit(user.get_surface(), user.get_rect())

			if first_platform.rect.y < display_height:
				display.blit(first_platform.get_surface(), first_platform.get_rect())

			for platform in platforms:
				if platform.rect.y < display_height:
					display.blit(platform.get_surface(), platform.get_rect())
			
			self.manager.draw_ui(display)
			pygame.display.flip()


# used to choose which screen to run
user_wdw, user_prev, user_curr = True, prev_screen, curr_screen

# driver code
if __name__ == "__main__":

	# first initialization - start on intro page
	user_wdw, user_prev, user_curr = Introduction(user_prev, user_curr).display_screen()

	# choose which screen to run as long as not quitting
	while user_wdw is not False:
		user_wdw, user_prev, user_curr = screen_to_run(user_wdw, user_prev, user_curr)

# close everything
quit_game()
