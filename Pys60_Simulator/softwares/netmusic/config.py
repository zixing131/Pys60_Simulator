# -*- coding: utf-8 -*-
"""
网易云音乐配置文件
兼容 Python 2.2+ 语法
"""

# API 基础地址
API_BASE_URL = "http://music.163.com"

# 屏幕分辨率配置
SCREEN_SIZES = {
    'QVGA_PORTRAIT': (240, 320),   # QVGA 竖屏
    'QVGA_LANDSCAPE': (320, 240),  # QVGA 横屏
    'TOUCH_PORTRAIT': (360, 640),  # 触屏竖屏
    'TOUCH_LANDSCAPE': (640, 360), # 触屏横屏
}

# 颜色配置
COLORS = {
    'PRIMARY': 0xE60026,      # 网易云红色
    'ACCENT': 0xE60026,       # 强调色
    'BACKGROUND': 0xFFFFFF,   # 背景白色
    'TEXT': 0x000000,         # 文字黑色
    'TEXT_GRAY': 0x666666,    # 灰色文字
    'DIVIDER': 0xEEEEEE,      # 分割线
    'PLAYING_BAR': 0xE60026,  # 播放进度条
}

# 字体大小配置
FONT_SIZES = {
    'TITLE': 18,      # 标题
    'SUBTITLE': 14,   # 副标题
    'NORMAL': 12,     # 正常文字
    'SMALL': 10,      # 小字
}

# 播放模式
PLAYBACK_MODE = {
    'ORDER': 0,    # 顺序播放
    'SHUFFLE': 1,  # 随机播放
    'LOOP': 2,     # 单曲循环
}

# 存储键名
STORAGE_KEYS = {
    'PLAYLIST': 'netmusic_playlist',
    'SONG_ID': 'netmusic_songid',
    'PLAYBACK_MODE': 'netmusic_playmode',
    'LOGIN_INFO': 'netmusic_login',
}

# 网络请求超时（秒）
REQUEST_TIMEOUT = 30

# 缓存配置
CACHE_ENABLED = True
CACHE_DIR = 'E:\\netmusic_cache\\'

# 日志配置
DEBUG = True
