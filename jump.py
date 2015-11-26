import pygame
from ball import *
from levels import *

pygame.init()

display_width = 600
display_height = 600
clock = pygame.time.Clock()

white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
purple = (128,0,128)
yellow = (255,255,0)
black = (0,0,0)
light_blue=(132,112,255)


screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Jump")
home = pygame.image.load('home.png')
pygame.mixer.music.load('sky.wav')

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)

gravity = -0.5
speed = 0
goal = home.get_rect()

def you_win():
	win = True

	while win:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		screen.fill(white)
		message_to_screen("You Won!",red,-100,"medium")
		message_to_screen("You're so Awesome!",green,0,"small")
		screen.blit(home,[280,400])

		buttons("replay",green,70,520,120,50)
		buttons("quit",red,440,520,100,50)

		pygame.display.update()



def game_over():
	pygame.mixer.music.stop()
	over = True

	while over:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		screen.fill(white)

		message_to_screen("Game Over!",red,-100,"medium")
		message_to_screen("Sorry you Lost!",purple,0,"small")


		buttons("replay",green,70,520,120,50)
		buttons("quit",red,440,520,100,50)
		pygame.display.update()


def intro():

	intro = True

	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		screen.fill(white)
		message_to_screen("Laser Jump",red,-100,"medium")
		message_to_screen("Good luck finishing the game!",green,0,"small")

		buttons("play",green,70,520,100,50)
		buttons("controls",yellow,240,520,120,50)
		buttons("quit",red,440,520,100,50)
		pygame.display.update()


def pause():
	pygame.mixer.music.pause()

	paused = True

	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					paused = False
					pygame.mixer.music.unpause()

		message_to_screen("Press SpaceBar to continue",light_blue,0,"small")

		pygame.display.update()



def controls():

	control = True

	while control:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		screen.fill(white)

		message_to_screen("Controls",green,-150,"medium")

		message_to_screen("RIGHT: -->   LEFT: <--",black,-30,"small")

		message_to_screen("JUMP: SpaceBar [------------]",black,20,"small")

		message_to_screen("PAUSE GAME: (P) ",black,80,"small")

		buttons("play",green, 70,500,100,50)
		buttons("quit", red, 430,500,100,50)
		clock.tick(5)

		pygame.display.update()


def text_objects(text,color,size):
	if size == "small":
		textSurface = smallfont.render(text, True, color)
	elif size == "medium":
		textSurface = medfont.render(text, True, color)

	return textSurface, textSurface.get_rect()
 

def message_to_screen(msg,color, y_displace, size):
	textSurf, textRect = text_objects(msg,color,size)
	textRect.center = (display_width /2), (display_height / 2)+y_displace
	screen.blit(textSurf, textRect)


def buttons(text,color,x,y,width,height):
	current = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if x+width > current[0] > x and y+height > current[1] > y:
		pygame.draw.rect(screen, blue, (x,y,width,height))

		if click[0] == 1:

			if text == "play" or text == "replay":
				level_1()
			elif text == "controls":
				controls()
			elif text == "quit":
				pygame.quit()
				quit()

	else:
		pygame.draw.rect(screen, color, (x,y,width,height))
	
	textSurf, textRect = text_objects(text,black,"small")
	textRect.center = x+50, y+20
	screen.blit(textSurf,textRect)


def level_1():

	pygame.mixer.music.play(-1)

	Ball = ball(300,554)

	global gravity
	global speed 
	global goal
	goal.x = 480
	goal.y = 40

	element_1 = block(450,450,120)
	element_2 = block(250,350,120)
	element_3 = block(50,250,120)
	element_4 = block(250,150,120)

	platforms = [element_1,element_2,element_3,element_4]


	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					speed = -7
				elif event.key == pygame.K_RIGHT:
					speed = 7

				elif event.key == pygame.K_SPACE:
					Ball.jump()

				elif event.key == pygame.K_p:
					pause()

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
					speed = 0


		Ball.x += speed

		screen.fill(white)
		screen.blit(home,[goal.x,goal.y])
		Ball.update(gravity)
		Ball.render(screen)

		pygame.draw.rect(screen,green,(0,570,600,30))

		for landing in platforms:
			landing.render(screen)
			if Ball.y < landing.y and Ball.y + 16 > landing.y:
				if Ball.x + 16 > landing.x and Ball.x - 16 < landing.x + landing.width:
					Ball.y = landing.y - 15
					Ball.onGround = True
				else:
					Ball.onGround = False

			elif Ball.y > landing.y and Ball.y - 16 < landing.y + 30:
				if Ball.x + 16 > landing.x and Ball.x - 16 < landing.x + landing.width:
					Ball.y = landing.y + 47
					Ball.onGround = False

		if Ball.y + 16 >= 570:
			Ball.y = 554
			Ball.onGround = True

		if Ball.x + 16 > display_width:
			Ball.x = display_width - 16
		elif Ball.x - 16 < 0:
			Ball.x = 16

		if Ball.x > goal.x and Ball.x < goal.x + 80:
			if Ball.y > goal.y and Ball.y < goal.y + 80:
				screen.fill(white)
				message_to_screen("Level 2",green,0,"medium")
				pygame.display.update()
				pygame.time.delay(1000)
				level_2()
		clock.tick(40)
		pygame.display.update()


def level_2():

	global gravity
	global speed
	global goal
	Ball = ball(80,435)
	goal.x = 50
	goal.y = 40

	element_1 = block(50,450,120)
	element_2 = block(270,350,60)
	element_3 = block(450,250,120)
	element_4 = block(210,150,60)

	platforms = [element_1,element_2,element_3,element_4]


	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					speed = -7
				elif event.key == pygame.K_RIGHT:
					speed = 7

				elif event.key == pygame.K_SPACE:
					Ball.jump()

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
					speed = 0

		Ball.x += speed

		screen.fill(white)
		screen.blit(home,[goal.x,goal.y])
		pygame.draw.rect(screen,red,(0,540,600,50))

		Ball.update(gravity)
		Ball.render(screen)

		for landing in platforms:
			landing.render(screen)
			if Ball.y < landing.y and Ball.y + 16 > landing.y:
				if Ball.x + 16 > landing.x and Ball.x - 16 < landing.x + landing.width:
					Ball.y = landing.y - 15
					Ball.onGround = True
				else:
					Ball.onGround = False

			elif Ball.y > landing.y and Ball.y - 16 < landing.y + 30:
				if Ball.x + 16 > landing.x and Ball.x - 16 < landing.x + landing.width:
					Ball.y = landing.y + 47
					Ball.onGround = False

		if Ball.x > goal.x and Ball.x < goal.x + 80:
			if Ball.y > goal.y and Ball.y < goal.y + 80:
				screen.fill(black)
				message_to_screen("Level 3",white,0,"medium")
				pygame.display.update()
				pygame.time.delay(1000)
				level_3()

		if Ball.y + 15 > 540:
			game_over()

		if Ball.x + 16 > display_width:
			Ball.x = display_width - 16
		elif Ball.x - 16 < 0:
			Ball.x = 16

		clock.tick(40)
		pygame.display.update()



def level_3():
	global gravity
	global speed
	global goal
	goal.x = 260
	goal.y = 40

	Ball = ball(320,435)

	element_1 = block(50,320,60)
	element_2 = block(270,450,60)
	element_3 = block(350,250,60)

	platforms = [element_1,element_2,element_3]

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					speed = -7
				elif event.key == pygame.K_RIGHT:
					speed = 7

				elif event.key == pygame.K_SPACE:
					Ball.jump()

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
					speed = 0

		Ball.x += speed

		screen.fill(white)

		Ball.update(gravity)
		Ball.render(screen)

		pygame.draw.rect(screen,red,(0,500,600,100))
		screen.blit(home,[goal.x,goal.y])

		for landing in platforms:
			landing.render(screen)
			if Ball.y < landing.y and Ball.y + 16 > landing.y:
				if Ball.x + 16 > landing.x and Ball.x - 16 < landing.x + landing.width:
					Ball.y = landing.y - 15
					Ball.onGround = True
				else:
					Ball.onGround = False

			elif Ball.y > landing.y and Ball.y - 16 < landing.y + 30:
				if Ball.x + 16 > landing.x and Ball.x - 16 < landing.x + landing.width:
					Ball.y = landing.y + 47
					Ball.onGround = False

		if Ball.x > goal.x and Ball.x < goal.x + 80:
			if Ball.y > goal.y and Ball.y < goal.y + 80:
				screen.fill(blue)
				message_to_screen("Level 4",red,0,"medium")
				pygame.display.update()
				pygame.time.delay(1000)
				level_4()

		if Ball.y + 15 > 500:
			game_over()

		if Ball.x + 16 > display_width:
			Ball.x = display_width - 16
		elif Ball.x - 16 < 0:
			Ball.x = 16

		clock.tick(40)
		pygame.display.update()


def level_4():
	global gravity
	global speed
	global goal
	goal.x = 320
	goal.y = 0

	element_1 = block(50,320,40)
	element_2 = block(250,450,40)
	element_3 = block(540,250,40)
	element_4 = block(200,200,40)

	Ball = ball(550,235)

	platforms = [element_1,element_2,element_3,element_4]

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					speed = -7
				elif event.key == pygame.K_RIGHT:
					speed = 7

				elif event.key == pygame.K_SPACE:
					Ball.jump()

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
					speed = 0


		Ball.x += speed

		screen.fill(white)
		screen.blit(home,[goal.x,goal.y])

		Ball.update(gravity)
		Ball.render(screen)

		pygame.draw.rect(screen,red,(0,470,600,100))

		for landing in platforms:
			landing.render(screen)
			if Ball.y < landing.y and Ball.y + 16 > landing.y:
				if Ball.x + 16 > landing.x and Ball.x - 16 < landing.x + landing.width:
					Ball.y = landing.y - 15
					Ball.onGround = True
				else:
					Ball.onGround = False

			elif Ball.y > landing.y and Ball.y - 16 < landing.y + 30:
				if Ball.x + 16 > landing.x and Ball.x - 16 < landing.x + landing.width:
					Ball.y = landing.y + 47
					Ball.onGround = False


		if Ball.x > goal.x and Ball.x < goal.x + 80:
			if Ball.y > goal.y and Ball.y < goal.y + 80:
				you_win()


		if Ball.y > 470:
			game_over()


		if Ball.x + 16 > display_width:
			Ball.x = display_width - 16
		elif Ball.x - 16 < 0:
			Ball.x = 16

		clock.tick(40)
		pygame.display.update()


intro()

