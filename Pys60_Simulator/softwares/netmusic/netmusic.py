# -*- coding: utf-8 -*-
"""
网易云音乐 PyS60 版
主程序入口
兼容 Python 2.2+ 语法
"""
import appuifw
import appuifw as ui
import graphics as ph
import e32
import key_codes

cn = lambda x: x.decode('utf-8')

from config import COLORS, SCREEN_SIZES
from utils import get_screen_layout

# 导入视图
from view_home import HomeView
from view_player import PlayerView
from view_search import SearchView
from view_playlist import PlaylistView

class NetMusicApp(object):
    """网易云音乐应用主类"""
    
    def __init__(self):
        # 运行标志
        self.running = 1
        self.loading = 0
        
        # 设置退出处理
        ui.app.exit_key_handler = self.exit
        ui.app.screen = 'full'
        ui.app.title = cn('网易云音乐')
        
        # 获取屏幕尺寸
        self.screen = ui.app.layout(ui.EScreen)[0]
        self.width, self.height = self.screen
        
        # 屏幕布局参数
        self.layout = get_screen_layout(self.screen)
        
        # 创建画布
        self.__canvas = ui.Canvas(self.__redraw, self.key)
        ui.app.body = self.__canvas
        
        # 创建绘图对象
        self.img = ph.Image.new(self.screen)
        self.background = ph.Image.new(self.screen)
        self.background.clear(COLORS['BACKGROUND'])
        
        # 视图管理
        self.views = []
        self.current_view = None
        
        # 底部菜单栏
        self.menu_items = []
        self.setup_menu()
        
        # 初始化主页
        self._show_home()
        
        # 首次绘制
        self.redraw()
    
    def setup_menu(self):
        """设置菜单"""
        from utils import cn as decode_text
        self.menu_items = [
            (decode_text('主页'), self._show_home),
            (decode_text('搜索'), self._show_search),
            (decode_text('播放器'), self._show_player),
            (decode_text('退出'), self.exit),
        ]
        appuifw.app.menu = self.menu_items
    
    def _show_home(self):
        """显示主页"""
        home_view = HomeView(
            self.width, 
            self.height,
            on_playlist_click=self._on_playlist_click,
            on_search_click=self._show_search
        )
        # 不在初始化时加载数据，让用户手动触发
        # home_view.load_data()
        self.current_view = home_view
        self.redraw()
    
    def _show_player(self):
        """显示播放器"""
        player_view = PlayerView(
            self.width,
            self.height,
            on_back=self._back_to_previous
        )
        self._push_view(player_view)
    
    def _show_search(self):
        """显示搜索"""
        search_view = SearchView(
            self.width,
            self.height,
            on_back=self._back_to_previous
        )
        self._push_view(search_view)
    
    def _show_playlist(self, playlist_id):
        """显示歌单详情"""
        playlist_view = PlaylistView(
            self.width,
            self.height,
            playlist_id=playlist_id,
            on_back=self._back_to_previous
        )
        self._push_view(playlist_view)
    
    def _on_playlist_click(self, playlist_id):
        """歌单点击事件"""
        self._show_playlist(playlist_id)
    
    def _push_view(self, view):
        """推入新视图"""
        if self.current_view:
            self.views.append(self.current_view)
        self.current_view = view
        self.redraw()
    
    def _back_to_previous(self):
        """返回上一个视图"""
        if self.views:
            self.current_view = self.views.pop()
            self.redraw()
        else:
            # 没有上一页，返回主页
            self._show_home()
    
    def __redraw(self, rect=None):
        """Canvas 回调重绘"""
        self.__canvas.blit(self.img)
    
    def redraw(self):
        """重绘界面"""
        if self.loading == 1:
            return
        
        self.loading = 1
        
        if not self.current_view:
            self.loading = 0
            return
        
        try:
            # 清空背景
            self.img.clear(COLORS['BACKGROUND'])
            
            # 绘制当前视图
            self.current_view.draw(self.img)
            
            # 绘制底部播放条（如果有歌曲正在播放）
            from player import player
            if player.current_song and self.current_view.__class__.__name__ != 'PlayerView':
                self._draw_mini_player(self.img)
            
            # 刷新画布
            self.__redraw()
        except Exception, e:
            print('Redraw error:', str(e))
        
        self.loading = 0
    
    def _draw_mini_player(self, img):
        """绘制迷你播放器条"""
        from player import player
        from ui_components import TextView, ProgressBar
        
        bar_height = 40
        bar_y = self.height - bar_height
        
        # 绘制背景
        img.rectangle((0, bar_y, self.width, self.height),
                     fill=0xF5F5F5, outline=0xF5F5F5)
        
        # 绘制歌曲信息
        song = player.current_song
        if song:
            song_name = song.get('name', u'')
            artists = song.get('ar', []) or song.get('artists', [])
            artist_name = ''
            if artists:
                artist_name = artists[0].get('name', '')
            
            # 歌曲名
            name_text = TextView(10, bar_y + 5, self.width - 80, 15, 
                               song_name, COLORS['TEXT'], 12)
            name_text.draw(img)
            
            # 艺术家
            artist_text = TextView(10, bar_y + 22, self.width - 80, 13,
                                 artist_name, COLORS['TEXT_GRAY'], 10)
            artist_text.draw(img)
        
        # 播放/暂停图标
        icon_x = self.width - 35
        icon_y = bar_y + 10
        icon_size = 20
        
        if player.playing:
            # 暂停图标（两条竖线）
            img.rectangle((icon_x, icon_y, icon_x + 6, icon_y + icon_size),
                         fill=COLORS['PRIMARY'], outline=COLORS['PRIMARY'])
            img.rectangle((icon_x + 10, icon_y, icon_x + 16, icon_y + icon_size),
                         fill=COLORS['PRIMARY'], outline=COLORS['PRIMARY'])
        else:
            # 播放图标（三角形）
            img.polygon([(icon_x, icon_y), 
                        (icon_x, icon_y + icon_size),
                        (icon_x + icon_size, icon_y + icon_size/2)],
                       fill=COLORS['PRIMARY'], outline=COLORS['PRIMARY'])
        
        # 绘制进度条
        progress = player.get_progress()
        if progress > 0:
            progress_width = int(self.width * progress)
            img.line((0, bar_y, progress_width, bar_y), COLORS['PLAYING_BAR'], width=3)
    
    def key(self, event):
        """处理按键事件"""
        if self.loading == 1:
            return
        
        if not self.current_view:
            return
        
        try:
            keycode = event.get('keycode', 0)
            scancode = event.get('scancode', 0)
            event_type = event.get('type', 0)
            
            # 映射按键
            key = None
            
            # 方向键
            if keycode == 63497 or keycode == 0x32:  # 上
                key = 'up'
            elif keycode == 63498 or keycode == 0x38:  # 下
                key = 'down'
            elif keycode == 63495 or keycode == 0x34:  # 左
                key = 'left'
            elif keycode == 63496 or keycode == 0x36:  # 右
                key = 'right'
            elif keycode == 63557 or keycode == key_codes.EKeySelect:  # 确认键
                key = 'select'
            elif keycode == key_codes.EKeyBackspace or scancode == 1:  # 退格键
                key = 'back'
            elif keycode == 0x23:  # # 键
                self._show_player()
                return
            
            # 左软键 - 打开菜单
            if scancode == 164 and event_type == 3:
                key = 'menu'
            
            # 传递给视图处理
            if key and hasattr(self.current_view, 'handle_key'):
                self.current_view.handle_key(key)
                self.redraw()
        
        except Exception, e:
            print('Key event error:', str(e))
    
    def handle_touch(self, x, y):
        """处理触摸事件"""
        if not self.current_view:
            return
        
        # 检查是否点击迷你播放器
        from player import player
        if player.current_song and self.current_view.__class__.__name__ != 'PlayerView':
            bar_height = 40
            bar_y = self.height - bar_height
            if y >= bar_y:
                self._show_player()
                self.redraw()
                return
        
        # 传递给视图处理
        if hasattr(self.current_view, 'handle_touch'):
            if self.current_view.handle_touch(x, y):
                self.redraw()
    
    def main(self):
        """主函数"""
        # 定时刷新（用于更新播放进度）
        self.refresh_timer = e32.Ao_timer()
        self.refresh_timer.after(1, self.timer_refresh)
    
    def timer_refresh(self):
        """定时刷新回调"""
        if self.running:
            self.redraw()
            e32.ao_yield()
            self.refresh_timer.after(1, self.timer_refresh)
    
    def exit(self):
        """退出应用"""
        from utils import cn as decode_cn
        if ui.query(decode_cn("要退出吗？"), "query"):
            self.running = 0
            # 清理
            try:
                from player import player
                player.close()
            except:
                pass
            import os
            os.abort()

# 创建应用实例
try:
    app = NetMusicApp()
    app.main()
    # 保持运行
    lock = e32.Ao_lock()
    lock.wait()
except Exception, e:
    print('Error:', str(e))
    import traceback
    traceback.print_exc()
