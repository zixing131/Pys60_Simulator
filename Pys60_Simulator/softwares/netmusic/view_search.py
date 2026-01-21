# -*- coding: utf-8 -*-
"""
搜索视图
兼容 Python 2.2+ 语法
"""
import graphics
import appuifw
from ui_components import ListView, ListItem, TextView, Button
from utils import cn, truncate_text
from config import COLORS, FONT_SIZES
from ncmapi import api

class SearchView(object):
    """搜索视图"""
    
    def __init__(self, width, height, on_back=None):
        self.width = width
        self.height = height
        self.on_back = on_back
        
        # 搜索关键词
        self.keyword = u''
        self.search_type = 'song'  # song, playlist
        
        # 组件
        self.title = TextView(0, 5, width, 25, cn('搜索'), COLORS['TEXT'], 16)
        self.title.align = 'center'
        
        # 搜索类型切换
        self.type_tabs = [cn('歌曲'), cn('歌单')]
        self.current_type_tab = 0
        
        # 列表视图
        list_y = 70
        self.list_view = ListView(0, list_y, width, height - list_y - 40)
        self.list_view.background = COLORS['BACKGROUND']
        self.list_view.on_item_click = self._on_item_click
        
        # 数据
        self.results = []
        self.loading = False
    
    def show_search_input(self):
        """显示搜索输入框"""
        try:
            keyword = appuifw.query(cn('请输入搜索关键词:'), 'text', self.keyword)
            if keyword:
                self.keyword = keyword
                self.do_search()
        except:
            pass
    
    def do_search(self):
        """执行搜索"""
        if not self.keyword:
            return
        
        if self.loading:
            return
        
        self.loading = True
        
        try:
            if self.search_type == 'song':
                # 搜索歌曲 type=1
                result = api.cloudsearch(self.keyword, search_type=1, limit=30)
                if result and result.get('code') == 200:
                    songs_data = result.get('result', {})
                    self.results = songs_data.get('songs', [])
                    self._update_list()
            else:
                # 搜索歌单 type=1000
                result = api.cloudsearch(self.keyword, search_type=1000, limit=30)
                if result and result.get('code') == 200:
                    playlist_data = result.get('result', {})
                    self.results = playlist_data.get('playlists', [])
                    self._update_list()
        except Exception, e:
            print('Search error:', str(e))
            import traceback
            traceback.print_exc()
        
        self.loading = False
    
    def _update_list(self):
        """更新列表"""
        items = []
        
        if self.search_type == 'song':
            # 歌曲列表
            for song in self.results:
                item = ListItem(data=song)
                item.title = truncate_text(song.get('name', ''), 20)
                
                # 副标题：艺术家
                artists = song.get('ar', []) or song.get('artists', [])
                if artists:
                    artist_names = [a.get('name', '') for a in artists]
                    item.subtitle = ' / '.join(artist_names)
                
                items.append(item)
        else:
            # 歌单列表
            for playlist in self.results:
                item = ListItem(data=playlist)
                item.title = truncate_text(playlist.get('name', ''), 20)
                
                # 副标题：创建者
                creator = playlist.get('creator', {})
                if creator:
                    item.subtitle = cn('by ') + cn(creator.get('nickname', ''))
                
                items.append(item)
        
        self.list_view.set_items(items)
    
    def _on_item_click(self, data):
        """列表项点击事件"""
        if not data:
            return
        
        if self.search_type == 'song':
            # 播放歌曲
            from player import player
            player.set_playlist([data])
            player.play_song(data)
        else:
            # 打开歌单 - 需要导航到歌单详情页
            # 这里暂时不处理，需要主程序支持页面导航
            pass
    
    def switch_type(self, type_index):
        """切换搜索类型"""
        if 0 <= type_index < len(self.type_tabs):
            self.current_type_tab = type_index
            if type_index == 0:
                self.search_type = 'song'
            else:
                self.search_type = 'playlist'
            self.results = []
            self.list_view.set_items([])
    
    def draw(self, img):
        """绘制视图"""
        # 清空背景
        img.clear(COLORS['BACKGROUND'])
        
        # 绘制标题
        self.title.draw(img)
        
        # 绘制搜索类型标签
        tab_y = 30
        tab_height = 30
        tab_width = self.width / len(self.type_tabs)
        
        for i, tab_name in enumerate(self.type_tabs):
            x = i * tab_width
            if i == self.current_type_tab:
                color = COLORS['PRIMARY']
            else:
                color = COLORS['TEXT_GRAY']
            
            tab_text = TextView(x, tab_y, tab_width, tab_height, tab_name, color, FONT_SIZES['NORMAL'])
            tab_text.align = 'center'
            tab_text.draw(img)
            
            if i == self.current_type_tab:
                indicator_y = tab_y + tab_height - 3
                img.rectangle((x + tab_width/4, indicator_y, x + tab_width*3/4, indicator_y + 3),
                             fill=COLORS['PRIMARY'], outline=COLORS['PRIMARY'])
        
        # 绘制搜索提示
        if not self.results and not self.loading:
            hint_text = TextView(0, tab_y + 50, self.width, 25, 
                               u'按确认键输入搜索关键词', COLORS['TEXT_GRAY'], FONT_SIZES['SMALL'])
            hint_text.align = 'center'
            hint_text.draw(img)
        
        # 绘制列表
        self.list_view.draw(img)
        
        # 绘制加载提示
        if self.loading:
            loading_text = TextView(0, self.height - 40, self.width, 20, 
                                  cn('搜索中...'), COLORS['TEXT_GRAY'], FONT_SIZES['SMALL'])
            loading_text.align = 'center'
            loading_text.draw(img)
    
    def handle_key(self, key):
        """处理按键事件"""
        if key == 'up':
            self.list_view.scroll_up()
        elif key == 'down':
            self.list_view.scroll_down()
        elif key == 'left':
            prev_tab = (self.current_type_tab - 1) % len(self.type_tabs)
            self.switch_type(prev_tab)
        elif key == 'right':
            next_tab = (self.current_type_tab + 1) % len(self.type_tabs)
            self.switch_type(next_tab)
        elif key == 'select' or key == 'enter':
            if self.results:
                self.list_view.on_select()
            else:
                self.show_search_input()
        elif key == 'back':
            if self.on_back:
                self.on_back()
        elif key == 'menu':
            self.show_search_input()
    
    def handle_touch(self, x, y):
        """处理触摸事件"""
        # 检查类型标签点击
        if 30 <= y <= 60:
            tab_width = self.width / len(self.type_tabs)
            tab_index = x / tab_width
            if 0 <= tab_index < len(self.type_tabs):
                self.switch_type(tab_index)
                return True
        
        # 列表点击
        return self.list_view.handle_touch(x, y)
