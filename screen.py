import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk_1 = pygame.image.load('RunnerGame\graphics\Player\player_walk_1.png').convert_alpha()
		player_walk_2 = pygame.image.load('RunnerGame\graphics\Player\player_walk_2.png').convert_alpha()
		self.player_walk = [player_walk_1,player_walk_2]
		self.player_index = 0
		self.player_jump = pygame.image.load('RunnerGame\graphics\Player\jump.png').convert_alpha()

		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80,300))
		self.gravity = 0

		self.jump_sound = pygame.mixer.Sound('RunnerGame\sounds\jump.mp3')
		self.jump_sound.set_volume(0.3)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
			self.gravity = -20
			self.jump_sound.play()

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 300:
			self.rect.bottom = 300

	def animation_state(self):
		if self.rect.bottom < 300:
			#jump - display the jump surface when player is not on floor
			self.image = self.player_jump        
		else:
			#walk - play walking animation if the player is on floor
			self.player_index += 0.1  
			if self.player_index >= len(self.player_walk): 
				self.player_index = 0 
			self.image = self.player_walk[int(self.player_index)]        

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self, type):
		super().__init__()
		
		if type == 'fly':
			fly_1 = pygame.image.load('RunnerGame\graphics\Fly\Fly1.png').convert_alpha()
			fly_2 = pygame.image.load('RunnerGame\graphics\Fly\Fly2.png').convert_alpha()
			self.frames = [fly_1, fly_2]
			y_pos = 210        
		else:
			snail_1 = pygame.image.load('RunnerGame\graphics\snail\snail1.png').convert_alpha()
			snail_2 = pygame.image.load('RunnerGame\graphics\snail\snail2.png').convert_alpha()
			self.frames = [snail_1, snail_2]
			y_pos = 300
		
		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))

	def animation_state(self):
		self.animation_index += 0.1
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def destroy(self):
		if self.rect.x <= -100:
			self.kill() 

	def update(self):
		self.animation_state()
		self.rect.x -= 6
		self.destroy()
		 
def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group, False):
		obstacle_group.empty()
		return False
	else:
		return True

def display_score():
	current_time = int(pygame.time.get_ticks() /1000) - start_time
	score_surface = text_font.render(f'Score: {current_time}', False, (64,64,64))
	score_rectangle = score_surface.get_rect(center = (400,50)) 
	screen.blit(score_surface, score_rectangle)
	return current_time

def obstacle_movement(obstacle_list):
	if obstacle_rectangle_list:
		for obstacle_rect in obstacle_rectangle_list:
			obstacle_rect.x -= 5

			if obstacle_rect.bottom == 300: screen.blit(snail_surface, obstacle_rect)
			else: screen.blit(fly_surface, obstacle_rect)

		# just append to the list if the obstacle position is greater than -100, otherwise delete it
		obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]


		return obstacle_list    
	else: return []

def collisions(player, obstacles):
	if obstacles:
		for obstacles_rect in obstacles:    
			if player.colliderect(obstacles_rect): return False
	return True

def player_animation():
	global player_surface, player_index

	if player_rectangle.bottom < 300:
		#jump - display the jump surface when player is not on floor
		player_surface = player_jump        
	else:
		#walk - play walking animation if the player is on floor
		player_index += 0.1  
		if player_index >= len(player_walk): player_index = 0 
		player_surface = player_walk[int(player_index)]
	

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('PyRunner')
clock = pygame.time.Clock()
text_font = pygame.font.Font('RunnerGame\word\Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('RunnerGame\sounds\music.wav')
bg_music.play(loops= -1)
bg_music.set_volume(0.3)
# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('RunnerGame\graphics\sky.png').convert()
ground_surface = pygame.image.load('RunnerGame\graphics\ground.png').convert()

#Intro Screen
player_stand = pygame.image.load('RunnerGame\graphics\Player\player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rectangle = player_stand.get_rect(center = (400,200))

game_name = text_font.render('PyRunner',False,(111,196,169))
game_name_rectangle = game_name.get_rect(center = (400,80) )

game_message = text_font.render('Press space to run', False,(111,196,169))
game_message_rectangle = game_message.get_rect(center = (400,330) )

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		# Timer
		if game_active: 
			if event.type == obstacle_timer and game_active:
				obstacle_group.add(Obstacle(choice(['fly','snail', 'snail','snail']))) 
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() /1000)

	if game_active == True:
		screen.blit(sky_surface,(0,0))
		screen.blit(ground_surface,(0,300))
		score = display_score() 
		# Player
		player.draw(screen)
		player.update()
		# Obstacle
		obstacle_group.draw(screen)
		obstacle_group.update()
		#collision
		game_active = collision_sprite()
	
	# Game Over Screen
	else:
		screen.fill((94,129,164))
		screen.blit(player_stand, player_stand_rectangle)
		
		player_gravity = 0

		score_message = text_font.render(f'Your score: {score}',False, (111,196,169))
		score_message_rectangle = score_message.get_rect(center = (400,330))
		screen.blit(game_name, game_name_rectangle)

		if score == 0: screen.blit(game_message, game_message_rectangle)
		else: screen.blit(score_message,score_message_rectangle)

	pygame.display.update()
	clock.tick(60)