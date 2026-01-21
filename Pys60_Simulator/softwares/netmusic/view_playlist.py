# -*- coding: utf-8 -*-
"""
歌单详情视图
兼容 Python 2.2+ 语法
"""
import graphics
from ui_components import ListView, ListItem, TextView, ImageView
from utils import cn, truncate_text, format_count
from config import COLORS, FONT_SIZES
from ncmapi import api

class PlaylistView(object):
    """歌单详情视图"""
    
    def __init__(self, width, height, playlist_id=None, on_back=None):
        self.width = width
        self.height = height
        self.playlist_id = playlist_id
        self.on_back = on_back
        
        # 歌单数据
        self.playlist_info = None
        self.songs = []
        self.loading = False
        
        # 组件
        # 标题栏
        self.title = TextView(0, 5, width, 25, u'歌单详情', COLORS['TEXT'], 16)
        self.title.align = 'center'
        
        # 歌单信息区域
        info_height = 100
        self.playlist_name = TextView(10, 35, width - 20, 20, '', COLORS['TEXT'], 14)
        self.playlist_creator = TextView(10, 55, width - 20, 18, '', COLORS['TEXT_GRAY'], 10)
        self.playlist_count = TextView(10, 73, width - 20, 18, '', COLORS['TEXT_GRAY'], 10)
        
        # 列表视图
        list_y = info_height
        self.list_view = ListView(0, list_y, width, height - list_y - 40)
        self.list_view.background = COLORS['BACKGROUND']
        self.list_view.on_item_click = self._on_item_click
        
        # 加载数据
        if playlist_id:
            self.load_playlist(playlist_id)
    
    def load_playlist(self, playlist_id):
        """加载歌单详情"""
        if self.loading:
            return
        
        self.loading = True
        self.playlist_id = playlist_id
        
        try:
            result = api.playlist_detail(playlist_id)
            if result and result.get('code') == 200:
                playlist = result.get('playlist', {})
                self.playlist_info = playlist
                
                # 更新歌单信息
                self.playlist_name.text = truncate_text(playlist.get('name', ''), 25)
                
                creator = playlist.get('creator', {})
                if creator:
                    self.playlist_creator.text = u'创建者: ' + creator.get('nickname', '')
                
                track_count = playlist.get('trackCount', 0)
                play_count = playlist.get('playCount', 0)
                self.playlist_count.text = u'歌曲数: %d  播放: %s' % (track_count, format_count(play_count))
                
                # 获取歌曲列表
                track_ids = playlist.get('trackIds', [])
                if track_ids:
                    # 只获取前100首
                    ids = [str(t.get('id')) for t in track_ids[:100] if t.get('id')]
                    if ids:
                        self._load_songs(ids)
        except Exception, e:
            print('Load playlist error:', str(e))
            import traceback
            traceback.print_exc()
        
        self.loading = False
    
    def _load_songs(self, song_ids):
        """加载歌曲详情"""
        try:
            # 分批加载（每次最多50首）
            batch_size = 50
            all_songs = []
            
            for i in range(0, len(song_ids), batch_size):
                batch_ids = song_ids[i:i+batch_size]
                
                result = api.song_detail(batch_ids)
                if result and result.get('code') == 200:
                    songs = result.get('songs', [])
                    all_songs.extend(songs)
            
            self.songs = all_songs
            self._update_list()
        except Exception, e:
            print('Load songs error:', str(e))
            import traceback
            traceback.print_exc()
    
    def _update_list(self):
        """更新列表"""
        items = []
        
        for i, song in enumerate(self.songs):
            item = ListItem(data=song)
            
            # 显示序号和歌名
            song_name = song.get('name', '')
            item.title = '%d. %s' % (i + 1, truncate_text(song_name, 18))
            
            # 副标题：艺术家 - 专辑
            artists = song.get('ar', []) or song.get('artists', [])
            album = song.get('al', {}) or song.get('album', {})
            
            subtitle_parts = []
            if artists:
                artist_names = [a.get('name', '') for a in artists]
                subtitle_parts.append(' / '.join(artist_names))
            if album and album.get('name'):
                subtitle_parts.append(album.get('name'))
            
            item.subtitle = ' - '.join(subtitle_parts)
            
            items.append(item)
        
        self.list_view.set_items(items)
    
    def _on_item_click(self, data):
        """列表项点击事件"""
        if not data:
            return
        
        # 设置播放列表并播放
        from player import player
        player.set_playlist(self.songs)
        player.play_song(data)
    
    def play_all(self):
        """播放全部"""
        if self.songs:
            from player import player
            player.set_playlist(self.songs)
            player.play_song(self.songs[0])
    
    def draw(self, img):
        """绘制视图"""
        # 清空背景
        img.clear(COLORS['BACKGROUND'])
        
        # 绘制标题
        self.title.draw(img)
        
        # 绘制歌单信息
        self.playlist_name.draw(img)
        self.playlist_creator.draw(img)
        self.playlist_count.draw(img)
        
        # 绘制分隔线
        img.line((0, 95, self.width, 95), COLORS['DIVIDER'], width=1)
        
        # 绘制列表
        self.list_view.draw(img)
        
        # 绘制加载提示
        if self.loading:
            loading_text = TextView(0, self.height - 40, self.width, 20, 
                                  u'加载中...', COLORS['TEXT_GRAY'], FONT_SIZES['SMALL'])
            loading_text.align = 'center'
            loading_text.draw(img)
    
    def handle_key(self, key):
        """处理按键事件"""
        if key == 'up':
            self.list_view.scroll_up()
        elif key == 'down':
            self.list_view.scroll_down()
        elif key == 'select' or key == 'enter':
            self.list_view.on_select()
        elif key == 'back':
            if self.on_back:
                self.on_back()
        elif key == 'menu':
            # 显示菜单：播放全部等
            self.play_all()
    
    def handle_touch(self, x, y):
        """处理触摸事件"""
        return self.list_view.handle_touch(x, y)
