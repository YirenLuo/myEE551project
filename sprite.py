import pygame

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

images = pygame.image.load('./resources/images/shoot.png')

# Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./resources/images/bullet.png')
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 5

    def move(self):
        self.rect.top -= self.speed

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


        self.image = images.subsurface(pygame.Rect(0, 99, 102, 126)).convert_alpha()
        self.rect = pygame.Rect(0, 99, 102, 126)
        self.rect.topleft = [500,300]
        self.speed = 8
        self.bullets = pygame.sprite.Group()
        self.is_hited = False
        self.score = 0

    # shoot
    def shoot(self):
        bullet = Bullet(self.rect.midtop)
        self.bullets.add(bullet)

    # Move up and judge the boundary
    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    #  Move down and judge the boundary
    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    # Move left and judge the boundary
    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    #  Move right and judge the boundary
    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed

# Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self,  init_pos):
       pygame.sprite.Sprite.__init__(self)
       self.image = images.subsurface(pygame.Rect(534, 612, 57, 43))
       self.rect = self.image.get_rect()
       self.rect.topleft = init_pos
       self.speed = 2

    def move(self):
        self.rect.top += self.speed
