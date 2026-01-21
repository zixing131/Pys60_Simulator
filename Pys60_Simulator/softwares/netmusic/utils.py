# -*- coding: utf-8 -*-
"""
工具函数模块
兼容 Python 2.2+ 语法
"""
import time
import os

def cn(text):
    """转换UTF-8字符串为Unicode"""
    try:
        if isinstance(text, unicode):
            return text
        return text.decode('utf-8')
    except:
        return text

def to_str(text):
    """转换Unicode为UTF-8字符串"""
    try:
        if isinstance(text, unicode):
            return text.encode('utf-8')
        return text
    except:
        return str(text)

def get_timestamp():
    """获取当前时间戳（毫秒）"""
    return str(int(time.time() * 1000))

def format_time(seconds):
    """格式化时间显示（秒转为 MM:SS）"""
    if not seconds or seconds < 0:
        return '00:00'
    minutes = int(seconds / 60)
    secs = int(seconds % 60)
    return '%02d:%02d' % (minutes, secs)

def format_count(count):
    """格式化播放数量"""
    try:
        count = int(count)
        if count >= 100000000:
            return '%.1f亿' % (count / 100000000.0)
        elif count >= 10000:
            return '%.1f万' % (count / 10000.0)
        else:
            return str(count)
    except:
        return '0'

def truncate_text(text, max_len):
    """截断文本"""
    if not text:
        return ''
    text = cn(text)
    if len(text) <= max_len:
        return text
    return text[:max_len] + '...'

def ensure_dir(path):
    """确保目录存在"""
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        return True
    except:
        return False

def parse_lyric(lyric_text):
    """解析歌词文本"""
    if not lyric_text:
        return []
    
    lines = []
    try:
        for line in lyric_text.split('\n'):
            line = line.strip()
            if not line or line.startswith('[by:') or line.startswith('[ar:') or line.startswith('[ti:'):
                continue
            
            # 解析时间标签 [mm:ss.xx]
            if line.startswith('[') and ']' in line:
                time_end = line.index(']')
                time_str = line[1:time_end]
                text = line[time_end + 1:].strip()
                
                if ':' in time_str:
                    parts = time_str.split(':')
                    if len(parts) == 2:
                        try:
                            minutes = int(parts[0])
                            seconds = float(parts[1])
                            total_seconds = minutes * 60 + seconds
                            lines.append({
                                'time': total_seconds,
                                'text': cn(text)
                            })
                        except:
                            pass
    except:
        pass
    
    return lines

def get_screen_layout(screen_size):
    """根据屏幕尺寸获取布局参数"""
    width, height = screen_size
    
    # 判断横竖屏
    is_landscape = width > height
    
    # 判断是否触屏设备（基于分辨率）
    is_touch = width >= 360 or height >= 360
    
    # 根据是否触屏设置参数
    if is_touch:
        title_height = 30
        item_height = 60
        image_size = 50
        padding = 10
        font_scale = 1.2
    else:
        title_height = 20
        item_height = 40
        image_size = 35
        padding = 5
        font_scale = 1.0
    
    layout = {
        'width': width,
        'height': height,
        'is_landscape': is_landscape,
        'is_touch': is_touch,
        'title_height': title_height,
        'item_height': item_height,
        'image_size': image_size,
        'padding': padding,
        'font_scale': font_scale,
    }
    
    return layout

class SimpleStorage(object):
    """简单的键值存储（模拟）"""
    def __init__(self):
        self.data = {}
    
    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def set(self, key, value):
        self.data[key] = value
    
    def remove(self, key):
        if key in self.data:
            del self.data[key]

# 全局存储实例
storage = SimpleStorage()
