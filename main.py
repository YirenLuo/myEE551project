import sys
import random

import pygame
from pygame.locals import *

from sprite import *

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

class PlaneWars:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('PlaneWars')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load('./resources/images/bg.png')
        self.player = Player()
        self.player_score = 0
        self.enemies = pygame.sprite.Group()
        self.enemies_down = pygame.sprite.Group()
        self.enemy_frequency = 0
        self.running = True

    def make_button(self, position, text):
        button_width = 400
        button_height = 70
        left, top = position
        pygame.draw.line(self.screen, (150, 150, 150), (left, top), (left+button_width, top), 5)
        pygame.draw.line(self.screen, (150, 150, 150), (left, top-2), (left, top+button_height), 5)
        pygame.draw.line(self.screen, (50, 50, 50), (left, top+button_height), (left+button_width, top+button_height), 5)
        pygame.draw.line(self.screen, (50, 50, 50), (left+button_width, top+button_height), [left+button_width, top], 5)
        pygame.draw.rect(self.screen, (100, 100, 150), (left, top, button_width, button_height))
        font = pygame.font.Font('./resources/font/simkai.ttf', 50)
        button_text = font.render(text, 1, (255,0,0))
        return self.screen.blit(button_text, (left+65, top+10))

    def end(self):
        while True:
            self.set()
            button_restart = self.make_button((330, 190), 'Restart')
            button_exit = self.make_button((330, 305) ,'Exit')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_restart.collidepoint(pygame.mouse.get_pos()):
                        self.running = True
                        self.player = Player()
                        return 
                    elif button_exit.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit()
                        sys.exit()
            self.clock.tick(60)
            pygame.display.update()
            

    def start(self):
        while True:
            self.set()
            button_start = self.make_button((330,105),'Start Game')
            button_exit = self.make_button((330,190),'Exit')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_start.collidepoint(pygame.mouse.get_pos()):
                        while True:
                            self.run()
                            self.end()
                        return 
                    elif button_exit.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit()
                        sys.exit()
            self.clock.tick(60)
            pygame.display.update()

    def enemy_generate(self, num):
        if self.enemy_frequency % num == 0:
            enemy_postion = [random.randint(0, SCREEN_WIDTH - 20), 0]
            enemy = Enemy(enemy_postion)
            self.enemies.add(enemy)
        if self.enemy_frequency >= num:
            self.enemy_frequency = 0

    def set(self):
        self.screen.fill(0)
        self.screen.blit(self.bg, (0,0))
        self.clock.tick(60)


    def run(self):
        while True:
            if self.running:
                self.set()
                self.enemy_frequency += 1

                player_socre_text = 'Player Score: %s' % self.player_score
                font = pygame.font.Font('./resources/font/simkai.ttf', 35)
                text = font.render(player_socre_text, True, (0,0,255))
                self.screen.blit(text, (2,5))


                if  self.player.is_hited:
                    self.running = False
                else:
                    self.screen.blit(self.player.image, self.player.rect)
                    
                for enemy in self.enemies:
                    enemy.move()
                    if pygame.sprite.collide_circle(enemy, self.player):
                        self.enemies_down.add(enemy)
                        self.enemies.remove(enemy)
                        self.player.is_hited = True
                        break
                    if enemy.rect.top < 0:
                        self.enemies.remove(enemy)

                for bullet in self.player.bullets:
                    bullet.move()
                    if bullet.rect.bottom < 0 :
                        self.player.bullets.remove(bullet)

                destory_enemies = pygame.sprite.groupcollide(self.enemies, self.player.bullets, 1, 1)

                for enemy in destory_enemies:
                    self.enemies_down.add(enemy)
                    self.player.score += 1

                self.player.bullets.draw(self.screen)

                self.player_score = self.player.score
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                key_pressed = pygame.key.get_pressed()
                if key_pressed[K_UP]:
                    self.player.moveUp()
                if key_pressed[K_DOWN]:
                    self.player.moveDown()
                if key_pressed[K_LEFT]:
                    self.player.moveLeft()
                if key_pressed[K_RIGHT]:
                    self.player.moveRight()
                if key_pressed[K_SPACE]:
                    self.player.shoot()
                    
                self.enemy_generate(100)
                self.enemies.draw(self.screen)
                pygame.display.update()
            
            else:
                break

if __name__ == '__main__':
    game = PlaneWars()
    game.start()
