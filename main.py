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
		self.can_fall = False
		self.latest_landing_y = self.rect.y
		self.latest_landing_x = self.rect.x
		self.max_jump_height = self.latest_landing_y - 200
		self.latest_landing_x_width = self.latest_landing_x
	
	def validate_jump(self):

		if self.rect.y >= self.latest_landing_y and self.rect.x >= self.latest_landing_x and self.rect.x <= self.latest_landing_x_width:
			self.can_jump = True
		
		if self.y <= self.max_jump_height:
			self.can_jump = False

	def checkCollision(self, Player, Platform):

		Platform.y -= Platform.h
		Platform.rect.y -= Platform.rect.h

		col = pygame.sprite.collide_rect(Player, Platform)
		if col == True:
			Platform.y += Platform.h
			Platform.rect.y += Platform.rect.h
			return True
		else:
			Platform.y += Platform.h
			Platform.rect.y += Platform.rect.h
			return False

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

				if self.can_fall == True:

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

	def update(self, event, move_size):

		self.move(event, move_size)

		if self.rect.x > (display_width - 68):
			self.rect.x = display_width - 68
			self.x = self.rect.x

		if self.rect.x < 0:
			self.rect.x = 0
			self.x = self.rect.x

		if self.rect.y < 0:
			self.rect.y = 0
			self.y = self.rect.y

		if self.rect.y > (display_height - 68):
			self.rect.y = display_height - 68
			self.y = self.rect.y

class Platform(MasterSprite):
	def __init__(self, x, y, w, h):

		pygame.sprite.Sprite.__init__(self)
		super().__init__('images/platform_blue.png')

		self.w = w
		self.rect.w = self.w

		self.h = h
		self.rect.h = self.h

		self.image = pygame.transform.scale(self.image, (self.w, self.h))
		self.image.convert_alpha()
		self.og_image = self.image

		self.set_xy(x, y)

		self.gravity_amt = 0

	def change_pic(self, new_img):

		self.image = pygame.image.load(new_img)
		self.image = pygame.transform.scale(self.image, (self.w, self.h))

	def gravity(self, amount):

		if self.gravity_amt == 0:
			self.gravity_amt = amount
		self.move_down(self.gravity_amt)

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

# go back to previous window/screen when p pressed on keyboard
def return_to_prev_screen(prev_screen, curr_screen):

	if prev_screen is None:
		return 'intro', prev_screen, curr_screen

	elif prev_screen == 'instructions':
		return 'instructions', prev_screen, curr_screen

	elif prev_screen == 'intro':
		return 'intro', prev_screen, curr_screen
	
	elif prev_screen == 'main' or prev_screen == 'death_screen':
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
	
	elif wdw == 'death_screen':
		return Death_Screen(prev_screen, curr_screen).display_screen()

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

	def draw_multiple_text(self, text, size, x, y, colour, text_type = 0, y_padding = 0):

		# instructions' text
		if text_type == 0:
			text_line_font = pygame.font.Font('fonts/Montserrat-Regular.ttf', size)
		else:
			text_line_font = pygame.font.Font('fonts/Montserrat-Bold.ttf', size)

		controls_text = text

		# put instructions on the screen
		for i in range(len(controls_text)):
			display.blit(text_line_font.render(controls_text[i], 1, colour), (x, (y_padding + (y * (i + 1)))))

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
					return ['instructions', self.prev_screen, self.curr_screen]
				
				if event.ui_element == self.play_game_btn:
					return ['main', self.prev_screen, self.curr_screen]

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
					return universal_k_event

				if local_k_event[0] != None:
					return local_k_event

				if local_b_event[0] != None:
					return local_b_event

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
				return ['intro', self.prev_screen, self.curr_screen]
		
		return [None, None, None]

	def draw_small_title_text(self, text, size, x, y, colour):

		text_line_font = pygame.font.Font('fonts/Montserrat-Regular.ttf', size)
		text_line_0 = text_line_font.render(text, 1, colour)
		display.blit(text_line_0, (x, y))

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
					return universal_k_event

				if local_k_event[0] != None:
					return local_k_event

				self.manager.process_events(event)
			self.manager.update(self.time_delta)

			self.draw_small_title_text('Controls:', 25, 5, 0, YELLOW)
			self.draw_multiple_text(['- To quit, either click the red button at the top left, or press', '   esc on the keyboard.', '- To go back to the previous page you were on, press', '   backspace on the keyboard.', '- To open up this page again, press i on the keyboard.', '- To go back to the main page, press m on the keyboard.', '- To move the main sprite, use the arrow keys.', '- To pause the game, press p on the keyboard.', '- You can click on any buttons - buttons always light up when ', '   they are hovered over.'], 25, 5, 27, WHITE)

			self.draw_small_title_text('Rules:', 25, 5, 324, RED)
			self.draw_multiple_text(['- The aim of the game is to survive for as long as possible.', '- Your score will increase based on how long you stay on a', '   platform for.', '- Your score will be displayed in the top-left corner of the', '   screen.', '- You can only jump 200 pixels up from the last platform you', '   landed on.', '- A new platform will spawn when an old one drops off the', '   edge of the screen.', '- You will fall with the platform you are standing on.', '- The first platform will only fall when you aren\'t on it.', '- If you hit any of the edges of the screen, you die.'], 25, 5, 27, WHITE, 0, 324)
			# TODO: CANNOT JUMP ON PLATFORMS UNTIL FIRST GONE

			self.manager.draw_ui(display)
			pygame.display.flip()

# main gameplay screen
class Main(Screen):
	def __init__(self, prev_screen, curr_screen):
		
		super().__init__(prev_screen, curr_screen)

		self.is_paused = False
		self.is_dead = False

	def local_keyboard_events(self, event):
	
		if event.type == pygame.KEYDOWN:
			# press m to go the intro screen
			if event.key == pygame.K_m:
				return ['intro', self.prev_screen, self.curr_screen]

			# press i to see instructions
			if event.key == pygame.K_i:
				return ['instructions', self.prev_screen, self.curr_screen]

		return [None, None, None]

	def local_button_events(self, event):

		if event.type == pygame.USEREVENT:
			# where to go when buttons clicked
			if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
				
				if event.ui_element == self.continue_btn:
					self.unpause()
				
				if event.ui_element == self.quit_btn:
					quit_game()
		
		return [None, None, None]

	def create_buttons_pause(self):
	
		# continue button
		self.continue_btn = pygame_gui.elements.UIButton(
		relative_rect = pygame.Rect((100, 400), (200, 100)),
		text = 'Continue', manager = self.manager, object_id = '#play_game')

		# quit button
		self.quit_btn = pygame_gui.elements.UIButton(
		relative_rect = pygame.Rect((500, 400), (200, 100)),
		text = 'Quit', manager = self.manager, object_id = '#quit')

	def pause(self):

		if self.is_paused == True:

			self.create_buttons_pause()
			self.draw_title_text('PAUSED', 50, (display_width / 2), (display_height / 8), BLACK)

			while self.is_paused:
				for event in pygame.event.get():
					
					universal_k_event = self.universal_keyboard_events(event)
					local_k_event = self.local_keyboard_events(event)
					local_b_event = self.local_button_events(event)
					
					if universal_k_event[0] != None:
						return universal_k_event

					if local_k_event[0] != None:
						return local_k_event
					
					if local_b_event[0] != None:
						return local_b_event

					self.manager.process_events(event)

				self.manager.update(self.time_delta)
				self.manager.draw_ui(display)
				pygame.display.flip()
		
		else:
			self.unpause()

	def unpause(self):

		self.is_paused = False
		self.clear_screen()
		self.manager.update(self.time_delta)
		self.manager.draw_ui(display)
		pygame.display.flip()

	def display_screen(self):

		self.set_prev_curr_screen('main')
		self.clear_screen()

		possible_gravities = []

		for x in range(1, 6):
			possible_gravities.append(x)
		
		user = Player(368, 680)
		first_platform = Platform(325, 745, 150, 15)

		platforms = pygame.sprite.Group()

		total_platforms = random.randint(5, 7)
		platform_counter = 0
		platforms_touched = 0

		temp_list_x = []
		temp_list_y = []

		for platform_number in range(total_platforms):
			if platform_number == 0:
				plat = Platform(325, 605, 150, 15)
			else:
				plat = Platform(random.randint(0, 550), random.randint((user.rect.y // 4), (user.rect.y - 50)), random.randint(100, 250), 15)
				for each in temp_list_x:
					if each == plat.x:
						if each >= 275:
							plat.x = random.randint(0, each // 2)
						else:
							plat.x = random.randint(275, (275 + (each // 2)))
				while plat.y in temp_list_y:
					plat.y = random.randint((user.rect.y // 4), (user.rect.y - 50))
				temp_list_x.append(plat.x)
				temp_list_y.append(plat.y)

			platforms.add(plat)

		display.blit(main_bg, (0, 0))

		while True:

			self.clock_sync()

			for platform in platforms:
				platform.gravity(possible_gravities[random.randint(0, 4)])

			if first_platform.y <= display_height:

				if user.checkCollision(user, first_platform) == True:
					
					# update jump height and values for gravity to work
					user.rect = user.get_rect()
					first_platform.rect = first_platform.get_rect()

					user.latest_landing_y = first_platform.y
					user.max_jump_height = user.y - 200
					user.latest_landing_x = first_platform.x
					user.latest_landing_x_width = user.latest_landing_x + first_platform.w

					user.can_jump = True
					user.can_fall = False

					platforms_touched += 1

					# can't go below first platform
					if user.rect.y > first_platform.y:
						user.set_y(user.latest_landing_y)
				
				else:
					
					# player and platform fall
					# user.can_fall = True
					first_platform.gravity(2)
					# user.gravity()

					platform_counter = 0
					any_platform_collide = False

					for platform in platforms:
						
						platform_counter += 1
						
						if platform_counter == 1:

							if user.checkCollision(user, platform) == True:

								any_platform_collide = True
								
								# update jump height and values for gravity to work
								user.rect = user.get_rect()
								platform.rect = platform.get_rect()

								user.latest_landing_y = platform.y
								user.max_jump_height = user.y - 200
								user.latest_landing_x = platform.x
								user.latest_landing_x_width = user.latest_landing_x + platform.w

								user.can_jump = True
								user.can_fall = False

								platforms_touched += 1

								# can't go below first platform
								if user.rect.y > platform.y:
									user.set_y(user.latest_landing_y)
							
							else:

								# player and platform fall
								user.can_fall = True
								platform.gravity(1)
								user.gravity()
							
						else:
							pass
			
			else:

				any_platform_collide = False
				platform_counter = 0
				
				for platform in platforms:
					
					platform_counter += 1

					if user.checkCollision(user, platform) == True:

						any_platform_collide = True

						user.rect = user.get_rect()
						platform.rect = platform.get_rect()

						user.latest_landing_y = platform.y
						user.max_jump_height = user.y - 200
						user.latest_landing_x = platform.x
						user.latest_landing_x_width = user.latest_landing_x + platform.w

						user.move_down(platform.gravity_amt)

						user.can_jump = True
						user.can_fall = False

						platforms_touched += 1

						# can't go below first platform
						if user.y > platform.y:
							user.set_y(user.latest_landing_y)
					
					else:

						if any_platform_collide == False and (platform_counter == total_platforms or platform_counter == (total_platforms - 1)):
							user.can_fall = True
							user.gravity()
							platform.gravity(platform.gravity_amt)

			temp_list_x = []
			temp_list_y = []
	
			while platform_counter < total_platforms:
	
				for platform_number in range(total_platforms - platform_counter):
					try:
						plat = Platform(random.randint(0, 550), random.randint((user.rect.y // 4), (user.rect.y - 50)), random.randint(100, 250), 15)
					except ValueError:
						plat = Platform(random.randint(0, 550), random.randint(0, 550), random.randint(100, 250), 15)
					for each in temp_list_x:
						if each == plat.x:
							if each >= 275:
								plat.x = random.randint(0, each // 2)
							else:
								plat.x = random.randint(275, (275 + (each // 2)))
					while plat.y in temp_list_y:
						plat.y = random.randint((user.rect.y // 4), (user.rect.y - 50))
					temp_list_x.append(plat.x)
					temp_list_y.append(plat.y)

					platforms.add(plat)
					platform_counter += 1
			
			# you died screen on boundary touch
			if user.rect.x >= (display_width - 68) or user.rect.x <= 0 or user.rect.y <= 0 or user.rect.y >= (display_height - 68):
				self.is_dead = True

			if self.is_dead == True:
				return ['death_screen', prev_screen, curr_screen]

			for event in pygame.event.get():

				temp_list_x = []
				temp_list_y = []
		
				while platform_counter < total_platforms:
		
					for platform_number in range(total_platforms - platform_counter):
						try:
							plat = Platform(random.randint(0, 550), random.randint((user.rect.y // 4), (user.rect.y - 50)), random.randint(100, 250), 15)
						except ValueError:
							plat = Platform(random.randint(0, 550), random.randint(0, 550), random.randint(100, 250), 15)
						for each in temp_list_x:
							if each == plat.x:
								if each >= 275:
									plat.x = random.randint(0, each // 2)
								else:
									plat.x = random.randint(275, (275 + (each // 2)))
						while plat.y in temp_list_y:
							plat.y = random.randint((user.rect.y // 4), (user.rect.y - 50))
						temp_list_x.append(plat.x)
						temp_list_y.append(plat.y)

						platforms.add(plat)
						platform_counter += 1

				user.update(event, 10)

				# press p to pause game
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_p:
						if self.is_paused == False:
							self.is_paused = True
							self.pause()
						else:
							self.unpause()

				universal_k_event = self.universal_keyboard_events(event)
				local_k_event = self.local_keyboard_events(event)
				
				if universal_k_event[0] != None:
					return universal_k_event

				if local_k_event[0] != None:
					return local_k_event

				self.manager.process_events(event)
			self.manager.update(self.time_delta)

			display.blit(main_bg, (0, 0))
			self.draw_multiple_text(['score: ' + str(platforms_touched)], 25, 10, 10, BLACK, 1)
			display.blit(user.get_surface(), user.get_rect())

			if first_platform.rect.y < display_height:
				display.blit(first_platform.get_surface(), first_platform.get_rect())

			for platform in platforms:
				if platform.rect.y < display_height:
					display.blit(platform.get_surface(), platform.get_rect())
				else:
					platforms.remove(platform)
					platform.kill()
			
			self.manager.draw_ui(display)
			pygame.display.flip()

# screen displayed when user crashes into window edges
class Death_Screen(Screen):
	def local_keyboard_events(self, event):
		
		if event.type == pygame.KEYDOWN:
			# press m to go the intro screen
			if event.key == pygame.K_m:
				return ['intro', self.prev_screen, self.curr_screen]

			# press i to see instructions
			if event.key == pygame.K_i:
				return ['instructions', self.prev_screen, self.curr_screen]

		return [None, None, None]

	def local_button_events(self, event):

		if event.type == pygame.USEREVENT:
			# where to go when buttons clicked
			if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
				
				if event.ui_element == self.play_again_btn:
					return 'main', self.prev_screen, self.curr_screen
				
				if event.ui_element == self.quit_btn:
					quit_game()
		
		return [None, None, None]

	def create_buttons_dead(self):
	
		# play again button
		self.play_again_btn = pygame_gui.elements.UIButton(
		relative_rect = pygame.Rect((100, 400), (200, 100)),
		text = 'Play Again', manager = self.manager, object_id = '#play_game')

		# quit button
		self.quit_btn = pygame_gui.elements.UIButton(
		relative_rect = pygame.Rect((500, 400), (200, 100)),
		text = 'Quit', manager = self.manager, object_id = '#quit')

	def display_screen(self):

		self.set_prev_curr_screen('instructions')
		self.clear_screen()
	
		self.create_buttons_dead()
		self.draw_title_text('YOU DIED :(', 50, (display_width / 2), (display_height / 8), BLACK)

		while True:

			self.clock_sync()

			for event in pygame.event.get():

				universal_k_event = self.universal_keyboard_events(event)
				local_k_event = self.local_keyboard_events(event)
				local_b_event = self.local_button_events(event)
				
				if universal_k_event[0] != None:
					return universal_k_event

				if local_k_event[0] != None:
					return local_k_event
				
				if local_b_event[0] != None:
					return local_b_event

				self.manager.process_events(event)
			self.manager.update(self.time_delta)

			self.manager.draw_ui(display)
			pygame.display.flip()
		
		return [None, None, None]


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
