import pygame, random

# Constantes
WIDTH = 800
HEIGTH = 600
negro = (0,0,0)
blanco = (255,255,255)
rojo = (255,0,0)
verde = (0,255,0)

pygame.init()
pygame.mixer.init()
ventana = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("Proyecto Final")
clock = pygame.time.Clock()

# Funciones
def texto(superficie, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_superficie = font.render(text, True, rojo)
	text_rect = text_superficie.get_rect()
	text_rect.midtop = (x, y)
	superficie.blit(text_superficie, text_rect)

def BarraDeVida(superficie, x, y, porcentaje):
	BARRA_LENGHT = 100
	BARRA_HEIGHT = 10
	fill = (porcentaje / 90) * BARRA_LENGHT
	borde = pygame.Rect(x, y, BARRA_LENGHT, BARRA_HEIGHT)
	fill = pygame.Rect(x, y, fill, BARRA_HEIGHT)
	pygame.draw.rect(superficie, verde, fill)
	pygame.draw.rect(superficie, blanco, borde, 2)

# Jugador
class Sujeto(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("ProyectoF/player1.png").convert()
		self.image.set_colorkey(blanco)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH // 2
		self.rect.bottom = HEIGTH - 10
		self.life = 90
	
	def update(self):
		self.speed_x = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speed_x = -7
		if keystate[pygame.K_RIGHT]:
			self.speed_x = 7
		self.rect.x += self.speed_x
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

# Obstaculos
class Obstaculo(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = random.choice(obstaculos_images)
		self.image.set_colorkey(blanco)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-100, -40)
		self.speedy = random.randrange(1, 10)
		
	def update(self):
		self.rect.y += self.speedy
		if self.rect.top > HEIGTH + 10:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-140, -100)
			self.speedy = random.randrange(1, 10)

# Animacion de los golpes
class Golpe(pygame.sprite.Sprite):
	def __init__(self, center):
		super().__init__()
		self.image = golpe_anim[0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 30

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(golpe_anim):
				self.kill()
			else:
				center = self.rect.center
				self.image = golpe_anim[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center 			

# Funciones de las ventanas
def Ventanas():
	ventana.blit(background, [0,0])
	texto(ventana, "DODGE IT!", 65, WIDTH // 2, HEIGTH // 8)
	texto(ventana, "Un juego de Agilidad y Concentracion", 27, WIDTH // 2, HEIGTH // 3)
	texto(ventana, "Presione una Tecla para Comenzar", 20, WIDTH // 2, HEIGTH // 1.25)
	pygame.display.flip()
	espera = True
	while espera:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.KEYUP:
				espera = False

def Ventanas1():
	ventana.blit(background, [0,0])
	texto(ventana, "EL JUEGO TERMINO", 65, WIDTH // 2, HEIGTH // 8)
	texto(ventana, "Su Record es: " + str(score), 40, WIDTH // 2, HEIGTH // 1.85)
	texto(ventana, "Presione una volver a Empezar", 20, WIDTH // 2, HEIGTH // 1.25)
	pygame.display.flip()
	espera = True
	while espera:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.KEYUP:
				espera = False

#Lista de Obstaculos
obstaculos_images = []
obstaculos_list = ["ProyectoF/ladrillo1.png", "ProyectoF/ladrillo2.png", "ProyectoF/ladrillo3.png"]
for img in obstaculos_list:
	obstaculos_images.append(pygame.image.load(img).convert())

#Lista de Animacion
golpe_anim = []
for i in range(9):
	file = "ProyectoF/golpe0{}.png".format(i)
	img = pygame.image.load(file).convert()
	img.set_colorkey(negro)
	img_scale = pygame.transform.scale(img, (70,70))
	golpe_anim.append(img_scale)

#Imagen de fondo
background = pygame.image.load("ProyectoF/fondo1.png").convert()

#Sonidos
explosion = pygame.mixer.Sound("ProyectoF/golpe.mp3")
pygame.mixer.music.load("ProyectoF/fondo.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)

# Ventana principal
score = 0
gameOver = True
running = True
while running:
	if gameOver:

		Ventanas()

		gameOver = False
		all_sprites = pygame.sprite.Group()
		obstaculos_list = pygame.sprite.Group()

		sujeto = Sujeto()
		all_sprites.add(sujeto)
		
		for i in range(8):
			obstaculo = Obstaculo()
			all_sprites.add(obstaculo)
			obstaculos_list.add(obstaculo)
		
	clock.tick(60) 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
	all_sprites.update()
    
	#Colision
	explo = pygame.sprite.spritecollide(sujeto, obstaculos_list, True)
	for vida in explo:
		sujeto.life -= 30
		explosion.play()
		golpe = Golpe(vida.rect.center)
		all_sprites.add(golpe)
		obstaculo = Obstaculo()
		all_sprites.add(obstaculo)
		obstaculos_list.add(obstaculo)
		if sujeto.life <= 0:
			score
			Ventanas1()
			score = 0
			gameOver = True
			 

	ventana.blit(background, [0, 0])
    
	#Record
	record = pygame.time.get_ticks() / 1000
	if record >= 1000 or 2000 or 3000:
		score += 10
	texto(ventana,"Record: " + str(score), 25, WIDTH // 10, 10)

	#Barra de vida
	BarraDeVida(ventana, 650, 21, sujeto.life)
	texto(ventana, "Vida: ", 25, WIDTH // 1.3, 10)

	all_sprites.draw(ventana)

	pygame.display.flip()
pygame.quit()