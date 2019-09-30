# PYGAME-FIRST
#
# (TODO) Make a named/referenciable object system
# (TODO) Finish this all

import pygame
from math import floor
from pathlib import Path
import os

scriptPath = os.path.dirname(os.path.abspath(__file__))

class game:

	def __init__(self, camera, Size=(300,300), framerate=60):
		self.camera = camera
		self.Size = Size
		self.framerate = framerate
		self.clock = pygame.time.Clock()

	def startRuntime(self):
		'''This should be defined by the programmer.'''
		pass

class gameObject:
	def __init__(self, sprite, Pos=(0,0), isScrollAffected=True):
		self.sprite = sprite
		self.Pos = Pos
		self.isScrollAffected = isScrollAffected
	def __repr__(self):
		return 'gameObject({}, {}, {})'.format(self.sprite, self.Pos, self.isScrollAffected)

class camera:

	# Centered Position
	CenteredPos = [0,0]

	# True Position
	TruePos = (0,0)

def iterateCamera(buffer, game):

	game.camera.CenteredPos = [
		min(max(0, game.camera.CenteredPos[0]), buffer.Size[0]),
		min(max(0, game.camera.CenteredPos[1]), buffer.Size[1])
	]

	# Update the "True Position"
	# It is a tuple to prevent changing via code. I'm not sure if it would be stable to update the camera position using this.
	TruePosX = (
		min(
			max(
				0, # The min point on the left/top without overlapping the virtual screeen.
				game.camera.CenteredPos[0] - # The camera centered position, subtracted by ...
				(game.Size[0] / 2) # ... half of the screen size
			),
			buffer.Size[0] - game.Size[0] # The max point on the right/bottom without overlapping the virtual screen
		)
	)
	TruePosY = (
		min(
			max(
				0, # The min point on the left/top without overlapping the virtual screeen.
				game.camera.CenteredPos[1] - # The camera centered position, subtracted by ...
				(game.Size[1] / 2) # ... half of the screen size
			),
			buffer.Size[1] - game.Size[1] # The max point on the right/bottom without overlapping the virtual screen
		)
	)
	game.camera.TruePos = (TruePosX, TruePosY)

def render_object(_object, camera, display):

	# Calculate a new position to render on, because of camera scrolling
	RenderPos = (None, None)
	if _object.isScrollAffected:
		RenderPos = (
			int(floor(_object.Pos[0] - camera.TruePos[0])),
			int(floor(_object.Pos[1] - camera.TruePos[1]))
		)
	else:
		RenderPos = (
			_object.Pos[0],
			_object.Pos[1]
		)

	# Blit the object's sprite and on the display using the new position
	display.blit(_object.sprite, RenderPos)

def render_screen(objectMap, camera, display, filler=(30,30,30), pygame=pygame):

	# Fill the screen background, if needed.
	if (filler != None):
		display.fill(filler)

	# Renders all layers in the object map
	for layer in objectMap:
		for a, entity in enumerate(layer):
			render_object(entity, camera, display)

	pygame.display.flip()

class buffer:

	def __init__(self, game, Size=None, **kwargs):

		# Receive the parent game link for interaction with camera and display.
		self.game = game

		# Set up Object Map
		if ('objMap' in kwargs):
			self.objMap = kwargs['objMap']
		else:
			self.objMap = []

		if (Size == None):
			# By default, set the buffer size to the game screen size.
			self.Size = game.Size
		else:
			# But, if specified, set it to that argument.
			self.Size = Size

	def bufMain(self):
		'''This should be defined by the programmer.'''
		pass

###########
# EXAMPLE #
###########

class myBuffer(buffer):

	def bufMain(self):

		# SETUP
		# (TODO) Fill one layer as a simple test
		# (TODO) Make this more default-y? Not sure if it still needs
		self.objMap = [
			# 00> Background
			[],
			# 01> Title
			[
				gameObject(self.game.gfx.char, (self.Size[0] - 32, 0)),
				gameObject(self.game.gfx.char, (self.Size[0] - 32, self.Size[1] - 32))
			],
			# 02> Main (Player, Enemies, Items etc.)
			[
				gameObject(self.game.gfx.char, self.game.camera.CenteredPos)
			]
		]

		# Populate the left side of the screen with some tiles
		for BaseY in range(self.Size[1] // 32):
			for BaseX in range(3):
				self.objMap[1].append(gameObject(self.game.gfx.char, (BaseY * 32, BaseX * 32)))

		# Hello, World!
		print('Hello, World!')

		# MAIN GAME
		running = True
		timer = 0

		while running:

			# Limit FPS to the specified framerate
			delta = self.game.clock.tick(self.game.framerate)

			class Input:
				'''Stores some input keys from pygame.key.get_pressed()'''
				_keyMap = pygame.key.get_pressed()
				keyUp = _keyMap[pygame.K_UP]
				keyDown = _keyMap[pygame.K_DOWN]
				keyLeft = _keyMap[pygame.K_LEFT]
				keyRight = _keyMap[pygame.K_RIGHT]

			def _process():

				if Input.keyUp:
					self.game.camera.CenteredPos[1] -= 5
				elif Input.keyDown:
					self.game.camera.CenteredPos[1] += 5

				if Input.keyLeft:
					self.game.camera.CenteredPos[0] -= 5
				elif Input.keyRight:
					self.game.camera.CenteredPos[0] += 5

				# Quick update on the object that follows the camera
				self.objMap[2][0].Pos = (self.game.camera.CenteredPos[0]-16, self.game.camera.CenteredPos[1]-16)

			def _finish():
				iterateCamera(self, self.game)
				# (TODO) Make this 'render screen' thing a part of the defaults, not having to be coded manually. Might have to update the 'while running' thing too.
				# (DONE) OH YEA, might move this out of this using the functional paradigm
				render_screen(self.objMap, self.game.camera, self.game.display)

			def _events():
				for event in pygame.event.get():
					if (event.type == pygame.QUIT):
						return False, (-1, 'Exit via pygame.QUIT')
				return True, (-1, None)

			_process()
			_finish()
			running, exitCode = _events()

			timer += 1

		return exitCode

class myGame(game):

	# (DONE) Load graphics (inside a class)
	class gfx:

		def loadImage(filename):
			'''Loads images relative to $project/img/'''
			#rootPath = Path(scriptPath)
			#imagePath = rootPath / 'img'
			return pygame.image.load('img/' + filename)
			# (TODO) Make this with paths relative to the scriptPath - I tried it, but there was some strange error where it couldn't load the file. And I checked, the paths were correct.

		tile1 = loadImage('tile1.png')
		logo = loadImage('tile2.png')
		char = loadImage('char.png')

	def startRuntime(self):

		# Init Pygame
		pygame.init()
		pygame.display.set_icon(self.gfx.logo) # (DONE)
		pygame.display.set_caption('pygame-first | Hello World!')
		self.display = pygame.display.set_mode(self.Size)

		# This 'buffers' tuple is used to make a good API for transferring between buffers, using simply an exit code that points to a tuple.
		buffers = (
			myBuffer(game=self, Size=(600,400)), # (<-) Ah yes, the tuple comma.
		)

		bufferCode = (0, None)
		while True:

			# Update the bufferCode based on the returned code ran on the last frame.
			bufferCode = buffers[bufferCode[0]].bufMain()
			assert type(bufferCode[0]).__name__ == 'int', 'The bufferCode is not an int'
			print(bufferCode) # (+DEBUG)
			if (bufferCode[0] < 0): break

		return 0

try:
	theGame = myGame(
		camera=camera(),
		Size=(512,288),
		framerate=60
	)
	theGame.startRuntime()
except KeyboardInterrupt:
	print('\n<KeyboardInterrupt>')
