import pygame

class ball:

	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.height = 16
		self.velocity = 0

		self.onGround = False

	def update(self,gravity):
		if not self.onGround:
			self.velocity += gravity
			self.y -= self.velocity
			self.y = int (self.y)


	def jump(self):
		if not self.onGround:
			return

		self.velocity = 11
		self.onGround = False

	def render(self,screen):
		return pygame.draw.circle(screen,(128,0,128),(self.x,self.y),self.height)

