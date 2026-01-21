# -*- coding: utf-8 -*-
"""
播放器视图
兼容 Python 2.2+ 语法
"""
import graphics
from ui_components import TextView, ProgressBar, Button, ImageView
from utils import cn
from config import COLORS, FONT_SIZES
from player import player
from ncmapi import api

class PlayerView(object):
    """播放器视图"""
    
    def __init__(self, width, height, on_back=None):
        self.width = width
        self.height = height
        self.on_back = on_back
        
        # 当前歌曲信息
        self.song = None
        self.lyric_lines = []
        self.current_lyric_index = 0
        self.show_lyric = False
        
        # 组件
        # 标题
        self.title = TextView(0, 10, width, 25, u'播放器', COLORS['TEXT'], 16)
        self.title.align = 'center'
        
        # 歌曲封面（居中）
        cover_size = min(width - 40, 150)
        cover_x = (width - cover_size) / 2
        self.cover = ImageView(cover_x, 50, cover_size, cover_size)
        
        # 歌曲名
        self.song_name = TextView(10, 210, width - 20, 25, '', COLORS['TEXT'], 16)
        self.song_name.align = 'center'
        
        # 艺术家
        self.artist_name = TextView(10, 235, width - 20, 20, '', COLORS['TEXT_GRAY'], 12)
        self.artist_name.align = 'center'
        
        # 进度条
        self.progress_bar = ProgressBar(20, 270, width - 40, 4)
        
        # 时间显示
        self.time_current = TextView(20, 280, 60, 20, '00:00', COLORS['TEXT_GRAY'], 10)
        self.time_total = TextView(width - 80, 280, 60, 20, '00:00', COLORS['TEXT_GRAY'], 10)
        self.time_total.align = 'right'
        
        # 控制按钮
        btn_y = height - 60
        btn_width = 60
        btn_height = 40
        
        # 上一曲
        self.btn_prev = Button((width - btn_width * 3 - 40) / 2, btn_y, btn_width, btn_height, 
                               u'上一曲', self._on_prev)
        
        # 播放/暂停
        self.btn_play = Button((width - btn_width) / 2, btn_y, btn_width, btn_height,
                              u'播放', self._on_toggle)
        
        # 下一曲
        self.btn_next = Button((width + btn_width + 20) / 2, btn_y, btn_width, btn_height,
                              u'下一曲', self._on_next)
        
        # 设置播放器回调
        player.on_song_changed = self._on_song_changed
        player.on_play_state_changed = self._on_play_state_changed
        
        # 加载当前歌曲
        self.song = player.current_song
        self._update_song_info()
    
    def _on_song_changed(self, song):
        """歌曲改变回调"""
        self.song = song
        self._update_song_info()
        self._load_lyric()
    
    def _on_play_state_changed(self, playing):
        """播放状态改变回调"""
        if playing:
            self.btn_play.text = u'暂停'
        else:
            self.btn_play.text = u'播放'
    
    def _update_song_info(self):
        """更新歌曲信息"""
        if not self.song:
            self.song_name.text = u'暂无歌曲'
            self.artist_name.text = ''
            return
        
        # 歌曲名
        self.song_name.text = self.song.get('name', u'未知歌曲')
        
        # 艺术家
        artists = self.song.get('ar', []) or self.song.get('artists', [])
        if artists:
            artist_names = [a.get('name', '') for a in artists]
            self.artist_name.text = ' / '.join(artist_names)
        else:
            self.artist_name.text = u'未知艺术家'
        
        # TODO: 加载封面图片
    
    def _load_lyric(self):
        """加载歌词"""
        if not self.song:
            return
        
        try:
            song_id = self.song.get('id')
            result = api.get_lyric(song_id)
            if result and result.get('code') == 200:
                lrc = result.get('lrc', {})
                lyric_text = lrc.get('lyric', '')
                self.lyric_lines = self._parse_lyric(lyric_text)
        except:
            pass
    
    def _parse_lyric(self, lyric_text):
        """解析歌词"""
        from utils import parse_lyric
        return parse_lyric(lyric_text)
    
    def _on_prev(self):
        """上一曲"""
        player.play_prev()
    
    def _on_toggle(self):
        """播放/暂停"""
        player.toggle()
    
    def _on_next(self):
        """下一曲"""
        player.play_next()
    
    def draw(self, img):
        """绘制视图"""
        # 清空背景
        img.clear(COLORS['BACKGROUND'])
        
        # 绘制标题
        self.title.draw(img)
        
        if self.show_lyric and self.lyric_lines:
            # 显示歌词
            self._draw_lyric(img)
        else:
            # 显示封面
            self.cover.draw(img)
        
        # 绘制歌曲信息
        self.song_name.draw(img)
        self.artist_name.draw(img)
        
        # 更新并绘制进度
        self.progress_bar.set_progress(player.get_progress())
        self.progress_bar.draw(img)
        
        # 更新时间显示
        self.time_current.text = player.get_current_time_str()
        self.time_total.text = player.get_duration_str()
        self.time_current.draw(img)
        self.time_total.draw(img)
        
        # 绘制控制按钮
        self.btn_prev.draw(img)
        self.btn_play.draw(img)
        self.btn_next.draw(img)
    
    def _draw_lyric(self, img):
        """绘制歌词"""
        if not self.lyric_lines:
            return
        
        # 获取当前歌词
        current_time = player.current_time
        current_index = 0
        for i, line in enumerate(self.lyric_lines):
            if line['time'] <= current_time:
                current_index = i
            else:
                break
        
        # 绘制多行歌词
        lyric_y = 60
        line_height = 25
        visible_lines = 5
        
        start_index = max(0, current_index - 2)
        end_index = min(len(self.lyric_lines), start_index + visible_lines)
        
        for i in range(start_index, end_index):
            line = self.lyric_lines[i]
            if i == current_index:
                color = COLORS['PRIMARY']
                font_size = FONT_SIZES['NORMAL']
            else:
                color = COLORS['TEXT_GRAY']
                font_size = FONT_SIZES['SMALL']
            
            lyric_text = TextView(10, lyric_y, self.width - 20, line_height, 
                                 line['text'], color, font_size)
            lyric_text.align = 'center'
            lyric_text.draw(img)
            
            lyric_y += line_height
    
    def handle_key(self, key):
        """处理按键事件"""
        if key == 'left':
            self._on_prev()
        elif key == 'right':
            self._on_next()
        elif key == 'select' or key == 'enter':
            self._on_toggle()
        elif key == 'back':
            if self.on_back:
                self.on_back()
        elif key == 'menu':
            # 切换歌词显示
            self.show_lyric = not self.show_lyric
    
    def handle_touch(self, x, y):
        """处理触摸事件"""
        # 检查按钮点击
        if self.btn_prev.contains(x, y):
            self.btn_prev.on_click()
            return True
        elif self.btn_play.contains(x, y):
            self.btn_play.on_click()
            return True
        elif self.btn_next.contains(x, y):
            self.btn_next.on_click()
            return True
        
        # 点击封面区域切换歌词显示
        if 50 <= y <= 200:
            self.show_lyric = not self.show_lyric
            return True
        
        return False
