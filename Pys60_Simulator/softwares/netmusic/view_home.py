# -*- coding: utf-8 -*-
"""
主页视图
兼容 Python 2.2+ 语法
"""
import graphics
from ui_components import ListView, ListItem, TextView, Button
from utils import cn, truncate_text
from config import COLORS, FONT_SIZES
from ncmapi import api

class HomeView(object):
    """主页视图"""
    
    def __init__(self, width, height, on_playlist_click=None, on_search_click=None):
        self.width = width
        self.height = height
        self.on_playlist_click = on_playlist_click
        self.on_search_click = on_search_click
        
        # 标签页
        self.tabs = [u'推荐歌单', u'最新歌曲', u'热门歌单']
        self.current_tab = 0
        
        # 组件
        self.title_bar = TextView(0, 0, width, 30, u'网易云音乐', COLORS['TEXT'], 16)
        self.title_bar.align = 'center'
        
        # 列表视图
        list_y = 60
        self.list_view = ListView(0, list_y, width, height - list_y - 40)
        self.list_view.background = COLORS['BACKGROUND']
        self.list_view.on_item_click = self._on_item_click
        
        # 数据
        self.playlists = []
        self.songs = []
        self.loading = False
    
    def load_data(self):
        """加载数据"""
        if self.loading:
            return
        
        self.loading = True
        
        try:
            if self.current_tab == 0:
                # 推荐歌单
                result = api.personalized_playlist(limit=20)
                if result and result.get('code') == 200:
                    self.playlists = result.get('result', [])
                    self._update_list()
            elif self.current_tab == 1:
                # 最新歌曲
                result = api.personalized_newsong(limit=20)
                if result and result.get('code') == 200:
                    songs_data = result.get('result', [])
                    self.songs = [item.get('song', {}) for item in songs_data if item.get('song')]
                    self._update_list()
            elif self.current_tab == 2:
                # 热门歌单
                result = api.top_playlist(limit=20)
                if result and result.get('code') == 200:
                    self.playlists = result.get('playlists', [])
                    self._update_list()
        except Exception, e:
            print('Load data error:', str(e))
            import traceback
            traceback.print_exc()
        
        self.loading = False
    
    def _update_list(self):
        """更新列表"""
        items = []
        
        if self.current_tab == 0 or self.current_tab == 2:
            # 歌单列表
            for playlist in self.playlists:
                item = ListItem(data=playlist)
                item.title = truncate_text(playlist.get('name', ''), 20)
                
                # 副标题
                play_count = playlist.get('playCount', 0)
                if play_count > 0:
                    if play_count >= 100000000:
                        count_str = '%.1f亿' % (play_count / 100000000.0)
                    elif play_count >= 10000:
                        count_str = '%.1f万' % (play_count / 10000.0)
                    else:
                        count_str = str(play_count)
                    item.subtitle = u'播放量: ' + count_str
                
                items.append(item)
        
        elif self.current_tab == 1:
            # 歌曲列表
            for song in self.songs:
                item = ListItem(data=song)
                item.title = truncate_text(song.get('name', ''), 20)
                
                # 副标题：艺术家
                artists = song.get('artists', [])
                if artists:
                    artist_names = [a.get('name', '') for a in artists]
                    item.subtitle = ' / '.join(artist_names)
                
                items.append(item)
        
        self.list_view.set_items(items)
    
    def _on_item_click(self, data):
        """列表项点击事件"""
        if not data:
            return
        
        if self.current_tab == 0 or self.current_tab == 2:
            # 歌单
            if self.on_playlist_click:
                playlist_id = data.get('id')
                if playlist_id:
                    self.on_playlist_click(playlist_id)
        
        elif self.current_tab == 1:
            # 歌曲 - 直接播放
            from player import player
            player.set_playlist([data])
            player.play_song(data)
    
    def switch_tab(self, tab_index):
        """切换标签页"""
        if 0 <= tab_index < len(self.tabs):
            self.current_tab = tab_index
            self.load_data()
    
    def next_tab(self):
        """下一个标签页"""
        self.current_tab = (self.current_tab + 1) % len(self.tabs)
        self.load_data()
    
    def prev_tab(self):
        """上一个标签页"""
        self.current_tab = (self.current_tab - 1) % len(self.tabs)
        self.load_data()
    
    def draw(self, img):
        """绘制视图"""
        try:
            # 清空背景
            img.clear(COLORS['BACKGROUND'])
            
            # 绘制标题栏
            self.title_bar.draw(img)
            
            # 绘制标签栏
            tab_y = 30
            tab_height = 30
            tab_width = self.width / len(self.tabs)
            
            for i, tab_name in enumerate(self.tabs):
                x = i * tab_width
                if i == self.current_tab:
                    color = COLORS['PRIMARY']
                else:
                    color = COLORS['TEXT_GRAY']
                
                # 标签文本
                tab_text = TextView(x, tab_y, tab_width, tab_height, tab_name, color, FONT_SIZES['NORMAL'])
                tab_text.align = 'center'
                tab_text.draw(img)
                
                # 选中指示器
                if i == self.current_tab:
                    indicator_y = tab_y + tab_height - 3
                    img.rectangle((x + tab_width/4, indicator_y, x + tab_width*3/4, indicator_y + 3),
                                 fill=COLORS['PRIMARY'], outline=COLORS['PRIMARY'])
            
            # 绘制列表
            self.list_view.draw(img)
            
            # 如果没有数据且不在加载中，显示提示
            if not self.loading and len(self.list_view.items) == 0:
                hint_y = self.height / 2
                hint_text = TextView(0, hint_y, self.width, 25, 
                                   u'按确认键加载数据', COLORS['TEXT_GRAY'], FONT_SIZES['NORMAL'])
                hint_text.align = 'center'
                hint_text.draw(img)
            
            # 绘制加载提示
            if self.loading:
                loading_y = self.height - 40
                loading_text = TextView(0, loading_y, self.width, 20, u'加载中...', 
                                       COLORS['TEXT_GRAY'], FONT_SIZES['SMALL'])
                loading_text.align = 'center'
                loading_text.draw(img)
        except Exception, e:
            print('HomeView draw error:', str(e))
            import traceback
            traceback.print_exc()
    
    def handle_key(self, key):
        """处理按键事件"""
        # 如果没有数据，按确认键加载
        if key == 'select' and len(self.list_view.items) == 0:
            self.load_data()
            return
        
        if key == 'up':
            self.list_view.scroll_up()
        elif key == 'down':
            self.list_view.scroll_down()
        elif key == 'left':
            self.prev_tab()
        elif key == 'right':
            self.next_tab()
        elif key == 'select' or key == 'enter':
            self.list_view.on_select()
        elif key == 'menu':
            # 打开菜单
            pass
    
    def handle_touch(self, x, y):
        """处理触摸事件"""
        # 检查标签栏点击
        if 30 <= y <= 60:
            tab_width = self.width / len(self.tabs)
            tab_index = x / tab_width
            if 0 <= tab_index < len(self.tabs):
                self.switch_tab(tab_index)
                return True
        
        # 列表点击
        return self.list_view.handle_touch(x, y)
