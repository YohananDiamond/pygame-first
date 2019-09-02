# SCENE API
# A module with some components for better scene structuring and organization.
from math import floor # Math Functions

class scene:
	ScreenToBlit = None
	def __init__(self, SizeTuple, ScreenToBlit):
		self.SizeX = SizeTuple[0]
		self.SizeY = SizeTuple[1]
		scene.ScreenToBlit = ScreenToBlit
	objmap = [
		# Layer 00: Background
		[],
		# Layer 01: Tiles
		[],
		# Layer 02: Entities (Player, Enemies, Coins etc.)
		[]
	]

	@classmethod
	def render_screen(cls, screen_class, blit_object):
		for layer in cls.objmap:
			for object in layer:
				object.render(screen_class, blit_object)

class obj:
	def __init__(self, sprite, coord=(0,0), scrollAffected=True):
		self.sprite = sprite
		self.x = coord[0]
		self.y = coord[1]
		self.RenderX = 0
		self.RenderY = 0
		self.scrollAffected = scrollAffected

	@staticmethod
	def cmd_blit(blit_obj, spr, pos):
		blit_obj.blit(spr, pos)

	def render(self, screen_class, blit_object):
		# Update Render Coordinates
		if self.scrollAffected:
			self.RenderX = int(floor(self.x - screen_class.PosX))
			self.RenderY = int(floor(self.y - screen_class.PosY))
		else:
			self.RenderX = self.x
			self.RenderY = self.y
		# Blit the Object on the Screen
		self.cmd_blit(blit_object, self.sprite, (self.RenderX, self.RenderY))

