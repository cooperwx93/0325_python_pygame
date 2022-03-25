import pygame
from pygame.sprite import Sprite  # 使用精灵类可将相关的元素编组

class Bullet(Sprite):
    '''管理子弹的类'''

    def __init__(self, ai_game):  # 和Ship类相似，添加的参数使得子弹类可以使用AlienInvasion的资源
        '''在飞船当前位置创建子弹'''
        super().__init__()  # 继承父类Sprite的属性和方法
        self.screen = ai_game.screen  # 赋值屏幕的尺寸
        self.settings = ai_game.settings  # 获取设置属性
        self.color = self.settings.bullet_color  # 获取设置中子弹的颜色
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)  # 将子弹放在左上角
        self.rect.midtop = ai_game.ship.rect.midtop   # 定义子弹的位置，将它和飞船进行绑定

        self.y = float(self.rect.y)  # 精确子弹的位置

    def update(self):
        '''更新子弹的位置'''
        self.y -= self.settings.bullet_speed  # 更新子弹的位置
        self.rect.y = self.y  # 子弹当前的位置

    def draw_bullet(self):
        '''在屏幕上绘制子弹'''
        pygame.draw.rect(self.screen, self.color, self.rect)

