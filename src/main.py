# PYGAME:FIRST
# My first prototype using py

# Import some useful modules.
import pygame # Pygame Library
# import time # Built-in Modules
import api.debug as debug, api.scene as scene_api # Game Modules
from math import floor # Math Functions
from pathlib import Path

##################
# USEFUL CLASSES #
##################
class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def __str__(self):
		return 'Point{}'.format((self.x, self.y))
	def tup(self):
		return self.x, self.y

print(Point(10, 20).tup())

# MAIN GAME
def main():

	###################
	# SETUP & CLASSES #
	###################

	# Init Pygame
	pygame.init()
	debug.log('Pygame API Initiated')

	class res:
		# Put all the resources to load here, like images, SFX and music.
		logo = pygame.image.load("img/tile2.png")
		char = pygame.image.load("img/char.png")
		tile1 = pygame.image.load("img/tile1.png")

		# Debug Message
		debug.log('Loaded Game Resources')

	class game:
		clock = pygame.time.Clock() # The game clock (to limit fps)
		timer = -1 # The game timer. Starts at -1 because it is increased on the first frame of the game by one to start on the frame 0.
		exitCode = (0, 'Unknown') # Init Finish Code

	class screen:
		# Screen-related variables
		SizeX = 512 # Screen Size X
		SizeY = 288 # Screen Size Y
		PosX = 0 # Screen Position X; is affected by camera.PosX
		PosY = 0 # Screen Position Y; is affected by camera.PosY

		# Screen Settings
		pygame.display.set_icon(res.logo)
		pygame.display.set_caption('Pygame:First')
		core = pygame.display.set_mode((SizeX, SizeY))

		# Debug Message
		debug.log('Screen Set Up')

	class scenes:
		# Make the Main Scene
		mainScene = scene_api.scene((600, 400), screen.core)

		# Debug Message
		debug.log('Scenes Set Up')

	class camera:
		# Camera Variables and Functions
		PosX = 0 # Camera Position X
		PosY = 0 # Camera Position Y

		# Iterate the screen position based on the camera position.
		@classmethod
		def iterate(cls):
			screen.PosX = min(max(0, cls.PosX - (screen.SizeX / 2)), scenes.mainScene.SizeX - screen.SizeX)
			screen.PosY = min(max(0, cls.PosY - (screen.SizeY / 2)), scenes.mainScene.SizeY - screen.SizeY)
			cls.PosX = screen.PosX + (screen.SizeX / 2)
			cls.PosY = screen.PosY + (screen.SizeY / 2)

		# Debug Message
		debug.log('Camera Set Up')

	# Finish Setup
	debug.log('Game Setup Finished')
	
	#################
	# SCENE MONTAGE #
	#################

	# Layer 00:
	scenes.mainScene.objmap[0] = [] # There isn't any current image file for the background.

	# Layer 01:
	scenes.mainScene.objmap[1]	= [
		scene_api.obj(res.tile1, (32,00)),
		scene_api.obj(res.tile1, (32,32)),
		scene_api.obj(res.tile1, (64,32)),
		scene_api.obj(res.tile1, (64,64)),
		scene_api.obj(res.tile1, (96,64)),
		scene_api.obj(res.tile1, (96,96)),
		scene_api.obj(res.char, (0,0)),
		scene_api.obj(res.char, (scenes.mainScene.SizeX - 32, 0)),
		scene_api.obj(res.char, (0, scenes.mainScene.SizeY - 32)),
		scene_api.obj(res.char, (scenes.mainScene.SizeX - 32, scenes.mainScene.SizeY - 32))
	]

	# Layer 02:
		#obj_player = scene.obj(res.char, (0,0))
		#obj_player.XSpeed = 10
		#obj_player.YSpeed = 5
	scenes.mainScene.objmap[2] = [
		#obj_player
	]

	#############
	# MAIN LOOP #
	#############

	running = True # Create the running variable.

	# The actual main loop.
	while running:
		delta = game.clock.tick(60) # Limit the framerate to 60fps and create a delta variable for the amount of time passed between the frames.
		game.timer += 1 # Add 1 to the timer at every frame. The first frame

		# Create the Input Class (for detecting player Input)
		class Input:
			_keyMap = pygame.key.get_pressed()
			keyUp = _keyMap[pygame.K_UP]
			keyDown = _keyMap[pygame.K_DOWN]
			keyLeft = _keyMap[pygame.K_LEFT]
			keyRight = _keyMap[pygame.K_RIGHT]

		# Process the events sent by the interface.
		for event in pygame.event.get():
			if (event.type == pygame.QUIT): # Quit by pressing the close button on the window.
				running = False # Disable Running Mode
				exitCode = (1, 'Close Button Pressed')

		# Physics Processing (to add later on a separate file)
		#def _physics_processing():
		#	if (player.x > ScreenSizeX - 32) or (player.x < 0):
		#		player.xSpeed *= -1
		#	if (player.y > ScreenSizeY - 32) or (player.y < 0):
		#		player.ySpeed *= -1
		#	player.x += player.xSpeed
		#	player.y += player.ySpeed

		# General Every-Frame Processing
		def _main_processing():
			# Move the Camera Around
			if Input.keyUp:
				camera.PosY -= 5
			elif Input.keyDown:
				camera.PosY+= 5
			if Input.keyLeft:
				camera.PosX -= 5
			elif Input.keyRight:
				camera.PosX += 5
			camera.iterate()

		_main_processing()

		####################
		# SCREEN RENDERING #
		####################

		# Fill the screen with a dark gray background (not layer-related)
		screen.core.fill((30,30,30))

		# Render the layers
		scenes.mainScene.render_screen(screen, screen.core)

		# Update the screen data
		pygame.display.flip()

	return exitCode

if __name__ == '__main__': # Only run if the file is being executed as a program and not a module.
	debug.log('Exit Code: {}'.format(main())) # Log the exit code after running the program.