# PYGAME:FIRST
# My first prototype using pygame.

# Imports
import pygame, time
from math import floor

# Useful Functions
def timestr():
	return time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime())
def log(arg, log_end='\n'):
	print('* {} * {};'.format(timestr(), arg))

# Main Game
def main():
	
	class data:
		logo = pygame.image.load("img/char.png")
		char = pygame.image.load("img/char.png")

	class play:
		ScreenSizeX = 512
		ScreenSizeY = 288
		CameraPosX = 0
		CameraPosY = 0
		ScreenPosX = 0 # Inherits CameraPosX
		ScreenPosY = 0 # Inherits CameraPosY
		SceneSizeX = 600 # Level Size (X)
		SceneSizeY = 400 # Level Size (Y)

	class game:	
		clock = pygame.time.Clock()
		exitCode = (0, 'Unknown')

	# Init pygame and display
	pygame.init()
	pygame.display.set_icon(data.logo)
	pygame.display.set_caption("Hello, World!")
	screen = pygame.display.set_mode((play.ScreenSizeX, play.ScreenSizeY))
	#screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
	log('Pygame Initiated!')

	# Create the obj type
	class obj:
		def __init__(self, sprite, coord=(0,0)):
			self.sprite = sprite
			self.x = coord[0]
			self.y = coord[1]
			self.RenderX = 0
			self.RenderY = 0
		def render(self):
			self.RenderX = int(floor(self.x - play.ScreenPosX))
			self.RenderY = int(floor(self.y - play.ScreenPosY))
			screen.blit(self.sprite, (self.RenderX, self.RenderY))

	# Object: Player
	#player = obj(data.char)
	#player.x = 0
	#player.y = 0
	#player.xSpeed = 10
	#player.ySpeed = 5

	# Objects: Extra
	o0 = obj(data.char, (0,0))
	o1 = obj(data.char, (play.SceneSizeX - 32, 0))
	o2 = obj(data.char, (0, play.SceneSizeY - 32))
	o3 = obj(data.char, (play.SceneSizeX - 32, play.SceneSizeY - 32))

	# Objects: Tiles (Simpler to Add)
	tiles = [
		obj(data.char, (32,00)),
		obj(data.char, (32,32)),
		obj(data.char, (64,32)),
		obj(data.char, (64,64)),
		obj(data.char, (96,64)),
		obj(data.char, (96,96))
	]

	# Render all objects on the scene.
	def _render():
		for o in tiles:
			o.render()
		o0.render()
		o1.render()
		o2.render()
		o3.render()

	def calculate():
		play.ScreenPosX = play.CameraPosX - (play.ScreenSizeX / 2)
		play.ScreenPosY = play.CameraPosY - (play.ScreenSizeY / 2)
		play.ScreenPosX = min(max(0, play.ScreenPosX), play.SceneSizeX - play.ScreenSizeX)
		play.ScreenPosY = min(max(0, play.ScreenPosY), play.SceneSizeY - play.ScreenSizeY)
		play.CameraPosX = play.ScreenPosX + (play.ScreenSizeX / 2)
		play.CameraPosY = play.ScreenPosY + (play.ScreenSizeY / 2)

	# Main Loop
	running = True
	counter = 0
	while running:
		counter += 1
		delta = game.clock.tick(60)

		# Render Images
		screen.fill((30,30,30)) # Background
		_render()

		# Update the Screen
		pygame.display.flip()

		# Input Class
		class input:
			_keyMap = pygame.key.get_pressed()
			keyUp = _keyMap[pygame.K_UP]
			keyDown = _keyMap[pygame.K_DOWN]
			keyLeft = _keyMap[pygame.K_LEFT]
			keyRight = _keyMap[pygame.K_RIGHT]

		# Physics Processing
		#def _physics_processing():
		#	if (player.x > game.ScreenSizeX - 32) or (player.x < 0):
		#		player.xSpeed *= -1
		#	if (player.y > game.ScreenSizeY - 32) or (player.y < 0):
		#		player.ySpeed *= -1
		#	player.x += player.xSpeed
		#	player.y += player.ySpeed

		# Main Processing
		def _main_processing():
			if input.keyUp:
				play.CameraPosY -= 5
			elif input.keyDown:
				play.CameraPosY += 5
			if input.keyLeft:
				play.CameraPosX -= 5
			elif input.keyRight:
				play.CameraPosX += 5
			calculate()

		# Event Processing
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				running = False
				game.exitCode = (1, 'Close Button Pressed')

		# Call the functions defined before
		#_physics_processing()
		_main_processing()

	return game.exitCode

if __name__ == '__main__':
	print('Execution ended with exit code = {}'.format(main()))