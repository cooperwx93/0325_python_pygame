class GameStats:
    '''跟踪游戏的统计信息'''

    def __init__(self, ai_game):
        '''初始化统计信息'''
        self.settings = ai_game.settings  # 获取设置类的资源
        self.reset_stats()  # 重置系统信息

        # 游戏刚启动时处于活动状态
        self.game_active = False

        # 最高得分
        self.high_score = 0



    def reset_stats(self):
        '''初始化在游戏运行期间可能变化的统计信息'''
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
