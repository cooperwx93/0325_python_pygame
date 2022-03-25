import pygame.font  # 导入font模块可以将文本渲染到屏幕上

class Button:
    '''创建按钮的类'''

    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen  # 赋值游戏屏幕
        self.screen_rect = self.screen.get_rect()  # 获取屏幕外形

        # 设置按钮尺寸和其他属性
        self.width ,self.height = 200,50
        self.button_color = (0,255,0)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None, 48)

        # 创建按钮并居中
        self.rect = pygame.Rect(0,0,self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 将文字渲染出来
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        '''将文字渲染为图像并居中'''
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color) # 将文字渲染为图像
        self.msg_image_rect = self.msg_image.get_rect()  # 获取文字的外形
        self.msg_image_rect.center = self.rect.center  # 将文字和按钮对齐

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)  # 在屏幕上绘制按钮
        self.screen.blit(self.msg_image, self.msg_image_rect)  # 绘制文字  略有疑问是如何使用self.msg_image?








