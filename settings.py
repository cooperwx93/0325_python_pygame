class Settings:
    '''管理游戏中所有的设置'''

    def __init__(self):
        ''' 初始化游戏的设置 '''

        # 对屏幕进行设置
        self.screen_width = 1200  # 屏幕的宽度
        self.screen_height = 800  # 屏幕的高度
        self.bg_color = (230,230,230)  # 屏幕的背景色

        # 飞船设置
        self.ship_limit = 3

        # 子弹设置
        self.bullet_width = 3000
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 3

        # 外星人设置
        self.alien_drop_speed = 10  # 垂直移动速度
        self.alien_point = 50
        self.score_scale = 1.5


        self.speedup_scale = 1.1  # 加快游戏的节奏

        self.initialize_dynamic_settings() # 初始化随着游戏进行而变化的属性

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 5.0
        self.alien_speed = 1.0  # 水平移动速度

        self.fleet_direction = 1  # 移动的方向，1 表示向右移， -1 表示向左移

    def increase_speed(self):
        '''提高速度设置'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_point = int(self.alien_point * self.score_scale)





