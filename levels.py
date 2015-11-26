import pygame

class block:
	def __init__(self,x,y,width):
		self.x = x
		self.y = y
		self.width = width
		self.height = 30

	def render(self,screen):
		pygame.draw.rect(screen,(0,0,0),(self.x,self.y,self.width,self.height))
