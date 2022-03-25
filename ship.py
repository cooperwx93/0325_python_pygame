import pygame
from pygame.sprite import Sprite

class Ship:
    '''管理飞船的类'''

    def __init__(self, ai_game):  #  初始化的时候添加了一个参数，指向AlienInvasion的实例，以便访问其定义的所有资源
        '''初始化飞船并设置其初始位置'''
        super().__init__()
        self.screen = ai_game.screen  #  将屏幕赋值给ship的一个属性
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()  # 获取屏幕的外形，为了将飞船放进正确的位置

        self.image = pygame.image.load('image/ship.bmp')  # 用该方法加载图像并赋予对象
        self.rect = self.image.get_rect()  # 获取飞船图像的外形

        self.rect.midbottom = self.screen_rect.midbottom  # 将飞船放在屏幕底部中央

        self.x = float(self.rect.x)  # 精确飞船的位移

        self.moving_right = False  # 判断飞船是否向右移动
        self.moving_left = False  # 判断飞船是否向左移动

    def blitme(self):
        '''绘制飞船'''
        self.screen.blit(self.image, self.rect)  # 将飞船绘制到指定的位置

    def center_ship(self):
        '''让飞船居中'''
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def update(self):
        '''根据移动标志更新飞船的位置'''
        if self.moving_right and  self.rect.right < self.screen_rect.right:  # 加上范围判断 控制飞船在屏幕内
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:  # # 加上范围判断 控制飞船在屏幕内
            self.x -= self.settings.ship_speed

        self.rect.x = self.x  # 最后更新飞船的位置




