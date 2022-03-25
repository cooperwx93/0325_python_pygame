import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''外星人类'''

    def __init__(self, ai_game):
        '''初始化外星人并设置其位置'''
        super().__init__()  # 继承Sprite的属性和方法
        self.screen = ai_game.screen  #  赋值屏幕的属性

        self.image = pygame.image.load('image/alien.bmp')  # 加载外星人的图像
        self.rect = self.image.get_rect()  # 获取外星人的外形

        self.rect.x = self.rect.width   # 外星人的初始位置
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)  # 精确外星人的位置

        self.settings = ai_game.settings  # 获取设置类的属性和方法

    def check_edge(self):
        '''检测是否和边沿发生了碰撞'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        '''外星人右移'''
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)   # 右移
        self.rect.x = self.x  # 更新位置


