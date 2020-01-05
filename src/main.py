# Welcome! {{{

# To-do:
# -> Implement type annotations
# -> Implement (kind of) pure functions, in most cases
# -> Use a low amount of classes

# }}}
# Importing {{{

import pygame # type: ignore
from math import floor
from pathlib import Path
from typing import (
    Tuple, Callable, NamedTuple,
    Union,
)
from enum import Enum

# }}}
# Typing Aliases {{{

Int2D = Tuple[int, int]
Float2D = Tuple[float, float]
ColorRGB = Tuple[int, int, int]
ExitCode = int # For now it's an int but I plan to change this later on.
Surface = pygame.Surface

# }}}
# Classes {{{

class Game: # {{{
    def __init__(self, screen_size: Int2D, current_scene: Scene):
        self.screen_size = screen_size
        self.current_scene = current_scene

    def link_camera(self, camera: Camera):
        self.camera = camera

    def runtime_function(self, f: Callable[[Game, Camera, Int2D], ExitCode]) -> ExitCode:
        """Runs the function with the game parameters and returns the function's exit code."""
        return f(self, self.camera, self.screen_size)
# }}}
class Object: # {{{
    def __init__(self, initial_position: Float2D, sprite: pygame.Surface, parallax_coefficient: Float2D = (1.0, 1.0)):
        self.pos = Vector2D.from_Float2D(initial_position)
        self.sprite = sprite
        self.parallax_coefficient = parallax_coefficient
# }}}
class Camera: # {{{
    def __init__(self, g: Game, initial_position: Float2D = (0.0, 0.0)):
        self.true_pos = Vector2D.from_Float2D(initial_position)
        self.g = g

    @property # type: ignore
    def center(self) -> Vector2D:
        # min/max is not needed here because it is already handled in the true pos updating
        r = Vector2D()
        r.x = self.true_pos.x + g.screen_size[0] / 2
        r.y = self.true_pos.y + g.screen_size[1] / 2
        return r

    @center.setter # type: ignore
    def center(self, location: Float2D):
        self.true_pos.x = min(max(0, location[0] - g.screen_size[0] / 2), g.current_scene.size[0])
        self.true_pos.y = min(max(0, location[1] - g.screen_size[1] / 2), g.current_scene.size[1])
# }}}
class Vector2D: # {{{
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    @staticmethod
    def from_Int2D(base: Int2D) -> Vector2D:
        return Vector2D(float(base[0]), float(base[1]))

    @staticmethod
    def from_Float2D(base: Float2D) -> Vector2D:
        return Vector2D(*base)
# }}}
class Scene: # {{{
    def __init__(self, size: Int2D):
        self.size = size
# }}}

# }}}
# Functions {{{

def render(obj: Object, display: pygame.Surface, camera: Camera): # {{{
    render_pos = (
        int((obj.pos.x - camera.true_pos.x) * obj.parallax_coefficient[0]),
        int((obj.pos.y - camera.true_pos.y) * obj.parallax_coefficient[1]),
    )

    # TODO: check if the object is completely out of screen and, if true, don't even blit it.
    display.blit(obj.sprite, render_pos)
# }}}

# }}}
# Applying Concepts {{{

def main_game(g: Game, camera: Camera, screen_size: Int2D) -> ExitCode: # {{{
    FRAMERATE = 30

    pygame.init()
    # pygame.display.set_icon(???)
    pygame.display.set_caption('&str')
    display = pygame.display.set_mode(screen_size)

    clock = pygame.time.Clock()

    layers = []
    layers.append([Object((0, 0), pygame.image.load("img/char.png"), (1.0, 1.0))])

    running = True
    while running:

        clock.tick(FRAMERATE)

        # Screen blitting
        display.fill((30, 30, 30))
        for layer in layers:
            for obj in layer:
                render(obj, display, camera)

        pygame.display.flip()

    return 0
# }}}

if __name__ == "__main__": # {{{
    g = Game((640, 360), Scene((700, 700)))
    g.link_camera(Camera(g, (0.0, 0.0)))
    g.runtime_function(main_game)
# }}}

# }}}

# def iterateCamera(buffer, game): # {{{

# 	game.camera.CenteredPos = [
# 		min(max(0, game.camera.CenteredPos[0]), buffer.Size[0]),
# 		min(max(0, game.camera.CenteredPos[1]), buffer.Size[1])
# 	]

# 	# Update the "True Position"
# 	# It is a tuple to prevent changing via code. I'm not sure if it would be stable to update the camera position using this.
# 	TruePosX = (
# 		min(
# 			max(
# 				0, # The min point on the left/top without overlapping the virtual screeen.
# 				game.camera.CenteredPos[0] - # The camera centered position, subtracted by ...
# 				(game.Size[0] / 2) # ... half of the screen size
# 			),
# 			buffer.Size[0] - game.Size[0] # The max point on the right/bottom without overlapping the virtual screen
# 		)
# 	)
# 	TruePosY = (
# 		min(
# 			max(
# 				0, # The min point on the left/top without overlapping the virtual screeen.
# 				game.camera.CenteredPos[1] - # The camera centered position, subtracted by ...
# 				(game.Size[1] / 2) # ... half of the screen size
# 			),
# 			buffer.Size[1] - game.Size[1] # The max point on the right/bottom without overlapping the virtual screen
# 		)
# 	)
# 	game.camera.TruePos = (TruePosX, TruePosY) # }}}

###########
# EXAMPLE #
###########

#class myScene(buffer): # {{{

#	def bufMain(self):

#		# SETUP
#		# (TODO) Fill one layer as a simple test
#		# (TODO) Make this more default-y? Not sure if it still needs
#		self.objMap = [
#			# 00> Background
#			[],
#			# 01> Title
#			[
#				gameObject(self.game.gfx.char, (self.Size[0] - 32, 0)),
#				gameObject(self.game.gfx.char, (self.Size[0] - 32, self.Size[1] - 32))
#			],
#			# 02> Main (Player, Enemies, Items etc.)
#			[
#				gameObject(self.game.gfx.char, self.game.camera.CenteredPos)
#			]
#		]

#		# Populate the left side of the screen with some tiles
#		for BaseY in range(self.Size[1] // 32):
#			for BaseX in range(3):
#				self.objMap[1].append(gameObject(self.game.gfx.char, (BaseY * 32, BaseX * 32)))

#		# Hello, World!
#		print('Hello, World!')

#		# MAIN GAME
#		running = True
#		timer = 0

#		while running:

#			# Limit FPS to the specified framerate
#			delta = self.game.clock.tick(self.game.framerate)

#			class Input:
#				'''Stores some input keys from pygame.key.get_pressed()'''
#				_keyMap = pygame.key.get_pressed()
#				keyUp = _keyMap[pygame.K_UP]
#				keyDown = _keyMap[pygame.K_DOWN]
#				keyLeft = _keyMap[pygame.K_LEFT]
#				keyRight = _keyMap[pygame.K_RIGHT]

#			def _process():

#				if Input.keyUp:
#					self.game.camera.CenteredPos[1] -= 5
#				elif Input.keyDown:
#					self.game.camera.CenteredPos[1] += 5

#				if Input.keyLeft:
#					self.game.camera.CenteredPos[0] -= 5
#				elif Input.keyRight:
#					self.game.camera.CenteredPos[0] += 5

#				# Quick update on the object that follows the camera
#				self.objMap[2][0].Pos = (self.game.camera.CenteredPos[0]-16, self.game.camera.CenteredPos[1]-16)

#			def _finish():
#				iterateCamera(self, self.game)
#				# (TODO) Make this 'render screen' thing a part of the defaults, not having to be coded manually. Might have to update the 'while running' thing too.
#				# (DONE) OH YEA, might move this out of this using the functional paradigm
#				render_screen(self.objMap, self.game.camera, self.game.display)

#			def _events():
#				for event in pygame.event.get():
#					if (event.type == pygame.QUIT):
#						return False, (-1, 'Exit via pygame.QUIT')
#				return True, (-1, None)

#			_process()
#			_finish()
#			running, exitCode = _events()

#			timer += 1

#		return exitCode
#    # }}}

#class myGame(game): # {{{

#	# (DONE) Load graphics (inside a class)
#	class gfx:

#		def loadImage(filename):
#			'''Loads images relative to $project/img/'''
#			#rootPath = Path(scriptPath)
#			#imagePath = rootPath / 'img'
#			return pygame.image.load('img/' + filename)
#			# (TODO) Make this with paths relative to the scriptPath - I tried it, but there was some strange error where it couldn't load the file. And I checked, the paths were correct.

#		tile1 = loadImage('tile1.png')
#		logo = loadImage('tile2.png')
#		char = loadImage('char.png')

#	def startRuntime(self):

#		# Init Pygame
#		pygame.init()
#		pygame.display.set_icon(self.gfx.logo) # (DONE)
#		pygame.display.set_caption('pygame-first | Hello World!')
#		self.display = pygame.display.set_mode(self.Size)

#		# This 'buffers' tuple is used to make a good API for transferring between buffers, using simply an exit code that points to a tuple.
#		buffers = (
#			myScene(game=self, Size=(600,400)), # (<-) Ah yes, the tuple comma.
#		)

#		bufferCode = (0, None)
#		while True:

#			# Update the bufferCode based on the returned code ran on the last frame.
#			bufferCode = buffers[bufferCode[0]].bufMain()
#			assert type(bufferCode[0]).__name__ == 'int', 'The bufferCode is not an int'
#			print(bufferCode) # (+DEBUG)
#			if (bufferCode[0] < 0): break

#		return 0
#    # }}}
