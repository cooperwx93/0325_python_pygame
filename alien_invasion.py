import sys  # 使用这个模块退出游戏
import pygame  # 开发游戏所需的功能
from settings import Settings  # 导入设置类
from ship import Ship  # 导入飞船类
from bullet import Bullet  # 导入子弹类
from alien import Alien  # 导入外星人类
from time import  sleep  # 导入sleep方法用来暂停游戏
from game_stats import GameStats  # 导入统计信息的类
from button import Button  # 导入按钮类
from scoreboard import Scoreboard  # 导入得分牌

class AlienInvasion:
    '''管理游戏资源和行为'''

    def __init__(self):
        '''初始化游戏并创建游戏资源'''
        pygame.init()  # 初始化背景设置
        self.settings = Settings()
        self.stats = GameStats(self)  # 创建统计信息的实例
        # 使用pygame.display.set_mode方法创建一个显示窗口,该方法返回一个列表，所有键盘和鼠标的事件都会引起for循环的运行
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width  # 全屏下更新设置类中屏幕的宽度
        self.settings.screen_height = self.screen.get_rect().height  # 全屏下更新设置类中屏幕的高度
        pygame.display.set_caption("Alien Invasion")  # 设置游戏标题
        self.ship = Ship(self)  # 这个设置有点特别，创建一个飞船的类，参数self指向AlienInvasion的实例，让ship能够访问游戏资源
        self.bullets = pygame.sprite.Group()  # 创建一个精灵编组，存储有效的子弹，类似于列表，作用是绘制子弹并存储子弹的位置
        self.aliens = pygame.sprite.Group()  # 创建一个精灵编组，存储有效的外星人，类似于列表，作用是绘制外星人并存储外星人的位置
        self._create_fleet()  # 创建外星人舰队
        self.play_button = Button(self, 'Play Game')
        self.sb = Scoreboard(self)


    def run_game(self):
        '''通过循环控制游戏的运行'''
        while True:  # 通过事件循环监控用户的操作，管理屏幕更新
            self._check_event()  #  管理事件循环
            if self.stats.game_active:
                self.ship.update()  # 根据右移标志判断是否移动
                self.bullets.update()  # 精灵的update，将对编组的每个精灵调用update,即调用子弹编写的update
                self._update_bullets()  # 更新子弹的位置并删除消失的子弹
                self._update_aliens()  # 更新外星人的位置
            self._update_screen()  #  管理屏幕更新

    def _ship_hit(self):
        '''飞船被外星人撞击'''
        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1  # 飞船数量减少1
            self.sb.prep_ship()

            self.aliens.empty()  # 清空外星人
            self.bullets.empty()  # 清空子弹

            self._create_fleet()  # 创建新的外星人群
            self.ship.center_ship() # 将飞船重新放回屏幕底部中央

            sleep(0.5)  # 暂停0.5秒
        else:
            self.stats.game_active = False

    def _create_fleet(self):
        '''创建外星人群'''

        # 先创建一个外星人
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size  # 获取外星人的宽度
        available_space_x = self.settings.screen_width - (2 * alien_width)   #  可容纳外星人的水平空间
        number_aliiens_x = available_space_x // (2*alien_width)  # 水平空间可容纳外星人的数量

        # 计算能够容纳多少行外星人
        available_space_y = self.settings.screen_height - 3 * alien_height - self.ship.rect.height
        number_rows = available_space_y // (2 * alien_height)

        for raw_numbers in range(number_rows):
            for alien_number in range(number_aliiens_x):  # 一排展示的外星人数量
                self._create_alien(alien_number, raw_numbers)

    def _create_alien(self,alien_number,raw_numbers):
        '''创建一个外星人'''
        alien = Alien(self)  # 每次循环都创建一个外星人
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number  # 外星人的横坐标
        alien.rect.x = alien.x  # 更新外星人的位置
        alien.y = alien_height + 2 * alien_height * raw_numbers  # 外星人的纵坐标
        alien.rect.y = alien.y  # 更新位置
        self.aliens.add(alien)  # 添加到编组

    def _check_fleet_edges(self):
        '''外星人到达边沿采取措施'''
        for alien in self.aliens.sprites():  # 循环编组中的外星人元素
            if alien.check_edge():  # 检测是否发生了碰撞
                self._check_fleet_direction()  # 改变移动的方向并向下移动
                break  # 这里的break是暂停整个循环吗？

    def _check_fleet_direction(self):
        '''外星人下移并改变方向'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.alien_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        '''更新外星人的位置'''
        self._check_fleet_edges()
        self.aliens.update()  # 精灵的update，将对编组的每个精灵调用update,即调用外星人编写的update
        # 检测外星人和飞船是否发生碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查是否有外星人到达屏幕底端
        self._check_alien_bottom()

    def _update_bullets(self):
        '''更新子弹的位置并删除消失的子弹'''
        self.bullets.update()

        for bullet in self.bullets.copy():  # 使用循环删除屏幕外的子弹
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()  # 检测子弹是否击中了外星人, True 和False控制是否消失

    def _check_alien_bottom(self):
        '''检查外星人是否到达底端'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom > screen_rect.bottom:
                self._ship_hit()
                break

    def _check_bullet_alien_collision(self):
            # 检测子弹是否击中了外星人, True 和False控制是否消失
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False,True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_point * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()

    def _check_event(self):  #  管理事件循环
        for event in pygame.event.get():  #  创建事件循环，监控用户的行为
            if event.type == pygame.QUIT :  #  如果事件类型是quit，就退出游戏
                sys.exit()
            elif event.type == pygame.KEYDOWN:  #  判断事件类型是否是按下键盘
                self._check_keydown_event(event)  # 检查按下键
            elif event.type == pygame.KEYUP:  # 判断事件类型是否是按上键盘
                self._check_keyup_event(event)  # 检查按上键
            elif event.type == pygame.MOUSEBUTTONDOWN: # 相应鼠标按下
                mouse_pos = pygame.mouse.get_pos()  # 获取鼠标点击的坐标
                self._check_play_button(mouse_pos)  # 将坐标和按钮匹配

    def _check_play_button(self,mouse_pos):  # 检测鼠标是否点击了按钮
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:  # 检测鼠标是否在按钮内点击
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()  # 重置游戏信息
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ship()

            # 清空外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)  # 隐藏光标

    def _check_keydown_event(self,event):
        '''相应按下键盘'''
        if event.key == pygame.K_RIGHT:  # 判断按下的建是不是右移键
            self.ship.moving_right = True  # 右移标志打开
        elif event.key == pygame.K_LEFT:  # 判断按下的建是不是左移键
            self.ship.moving_left = True  # 左移标志打开
        elif event.key == pygame.K_q:  #  按下q结束游戏
            sys.exit()
        elif event.key == pygame.K_SPACE and len(self.bullets) < self.settings.bullet_allowed:  # 如果按下的是空格键
            self._fire_bullets()  # 就开火
        elif event.key == pygame.K_p:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()  # 重置游戏信息
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ship()

            # 清空外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)  # 隐藏光标

    def _check_keyup_event(self, event):
        '''相应按上键'''
        if event.key == pygame.K_RIGHT:  # 判断按上的键盘是否是右移键
            self.ship.moving_right = False  # 如果是关闭右移标志
        elif event.key == pygame.K_LEFT:  # 判断按上的键盘是否是左移键
            self.ship.moving_left = False  # 如果是关闭左移标志

    def _fire_bullets(self):
        '''创建子弹并加入在编组中'''
        new_bullet = Bullet(self)  # 这个设置有点特别，创建一个子弹的类，参数self指向AlienInvasion的实例，让子弹能够访问游戏资源
        self.bullets.add(new_bullet)  # 将子弹添加到编组中

    def _update_screen(self):  #  管理屏幕更新
         self.screen.fill(self.settings.bg_color)  # 给屏幕填充颜色，fill方法也可以给其他的surface填充颜色
         self.ship.blitme()
         self.sb.show_score()
         for bullet in self.bullets.sprites():
             bullet.draw_bullet()
         self.aliens.draw(self.screen)  # 将外星人绘制到屏幕上
         if not self.stats.game_active:
             self.play_button.draw_button()

         pygame.display.flip()  # 每执行一次循环，都会创建一个空屏幕并擦去旧屏幕



if __name__ == '__main__': #  仅当直接运行该文件时，程序才会执行
    ai = AlienInvasion()
    ai.run_game()




