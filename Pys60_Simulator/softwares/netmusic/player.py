# -*- coding: utf-8 -*-
"""
音乐播放器模块
兼容 Python 2.2+ 语法
"""
import audio
import e32
from utils import storage, format_time
from config import PLAYBACK_MODE, STORAGE_KEYS
from ncmapi import api

class MusicPlayer(object):
    """音乐播放器"""
    
    def __init__(self):
        self.player = audio.Sound.open('E:\\temp.mp3')  # 占位文件
        self.current_song = None
        self.playlist = []
        self.playlist_index = 0
        self.playing = False
        self.playback_mode = PLAYBACK_MODE['SHUFFLE']
        self.duration = 0
        self.current_time = 0
        self.song_url = None
        
        # 回调函数
        self.on_song_changed = None
        self.on_play_state_changed = None
        self.on_progress_changed = None
        
        # 加载上次播放状态
        self._load_state()
    
    def _load_state(self):
        """加载播放状态"""
        try:
            mode = storage.get(STORAGE_KEYS['PLAYBACK_MODE'])
            if mode is not None:
                self.playback_mode = mode
        except:
            pass
    
    def _save_state(self):
        """保存播放状态"""
        try:
            storage.set(STORAGE_KEYS['PLAYBACK_MODE'], self.playback_mode)
            if self.current_song:
                storage.set(STORAGE_KEYS['SONG_ID'], self.current_song.get('id'))
        except:
            pass
    
    def set_playlist(self, songs):
        """设置播放列表"""
        if songs:
            self.playlist = songs
        else:
            self.playlist = []
        self.playlist_index = 0
    
    def add_to_playlist(self, song):
        """添加到播放列表"""
        if song not in self.playlist:
            self.playlist.append(song)
    
    def play_song(self, song):
        """播放指定歌曲"""
        if not song:
            return False
        
        # 获取歌曲播放地址
        try:
            song_id = song.get('id')
            if not song_id:
                return False
            
            # 获取播放 URL
            url_result = api.song_url(song_id)
            if url_result and url_result.get('code') == 200:
                data = url_result.get('data', [])
                if data and len(data) > 0:
                    url = data[0].get('url')
                    if url:
                        self.song_url = url
                        self.current_song = song
                        self._play_url(url)
                        self._save_state()
                        
                        if self.on_song_changed:
                            self.on_song_changed(song)
                        
                        return True
            
            return False
        except Exception, e:
            print('Play song error:', str(e))
            return False
    
    def _play_url(self, url):
        """播放 URL"""
        try:
            # PyS60 不直接支持流媒体播放
            # 这里需要先下载文件或使用其他方式
            # 简化实现：假设可以直接播放
            self.player.stop()
            # 实际应用中需要下载到本地再播放
            # self.player = audio.Sound.open(local_file_path)
            self.player.play()
            self.playing = True
            
            if self.on_play_state_changed:
                self.on_play_state_changed(True)
        except Exception, e:
            print('Play URL error:', str(e))
    
    def play(self):
        """播放"""
        if not self.playing and self.current_song:
            try:
                self.player.play()
                self.playing = True
                
                if self.on_play_state_changed:
                    self.on_play_state_changed(True)
            except:
                pass
    
    def pause(self):
        """暂停"""
        if self.playing:
            try:
                self.player.stop()
                self.playing = False
                
                if self.on_play_state_changed:
                    self.on_play_state_changed(False)
            except:
                pass
    
    def toggle(self):
        """切换播放/暂停"""
        if self.playing:
            self.pause()
        else:
            self.play()
    
    def play_next(self):
        """播放下一首"""
        if not self.playlist:
            return
        
        if self.playback_mode == PLAYBACK_MODE['LOOP']:
            # 单曲循环
            self.play_song(self.current_song)
        elif self.playback_mode == PLAYBACK_MODE['SHUFFLE']:
            # 随机播放
            import random
            self.playlist_index = random.randint(0, len(self.playlist) - 1)
            self.play_song(self.playlist[self.playlist_index])
        else:
            # 顺序播放
            self.playlist_index += 1
            if self.playlist_index >= len(self.playlist):
                self.playlist_index = 0
            self.play_song(self.playlist[self.playlist_index])
    
    def play_prev(self):
        """播放上一首"""
        if not self.playlist:
            return
        
        if self.playback_mode == PLAYBACK_MODE['LOOP']:
            # 单曲循环
            self.play_song(self.current_song)
        else:
            # 顺序播放
            self.playlist_index -= 1
            if self.playlist_index < 0:
                self.playlist_index = len(self.playlist) - 1
            self.play_song(self.playlist[self.playlist_index])
    
    def seek(self, position):
        """跳转到指定位置（秒）"""
        try:
            # PyS60 的 audio 模块可能不支持 seek
            # 这里是占位实现
            self.current_time = position
        except:
            pass
    
    def set_playback_mode(self, mode):
        """设置播放模式"""
        if mode in [PLAYBACK_MODE['ORDER'], PLAYBACK_MODE['SHUFFLE'], PLAYBACK_MODE['LOOP']]:
            self.playback_mode = mode
            self._save_state()
    
    def get_playback_mode_name(self):
        """获取播放模式名称"""
        if self.playback_mode == PLAYBACK_MODE['ORDER']:
            return u'顺序播放'
        elif self.playback_mode == PLAYBACK_MODE['SHUFFLE']:
            return u'随机播放'
        elif self.playback_mode == PLAYBACK_MODE['LOOP']:
            return u'单曲循环'
        return u'未知'
    
    def get_progress(self):
        """获取播放进度 0.0 ~ 1.0"""
        if self.duration > 0:
            return float(self.current_time) / float(self.duration)
        return 0.0
    
    def get_current_time_str(self):
        """获取当前播放时间字符串"""
        return format_time(self.current_time)
    
    def get_duration_str(self):
        """获取总时长字符串"""
        return format_time(self.duration)
    
    def stop(self):
        """停止播放"""
        try:
            self.player.stop()
            self.playing = False
            self.current_time = 0
            
            if self.on_play_state_changed:
                self.on_play_state_changed(False)
        except:
            pass
    
    def close(self):
        """关闭播放器"""
        self.stop()
        try:
            self.player.close()
        except:
            pass

# 全局播放器实例
player = MusicPlayer()
