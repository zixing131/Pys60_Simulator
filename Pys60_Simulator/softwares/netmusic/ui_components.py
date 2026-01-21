# -*- coding: utf-8 -*-
"""
UI 组件库
兼容 Python 2.2+ 语法
"""
import graphics
from utils import cn, truncate_text, get_screen_layout
from config import COLORS, FONT_SIZES

class UIComponent(object):
    """UI 组件基类"""
    
    def __init__(self, x=0, y=0, width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True
        self.enabled = True
        self.background = None
        self.parent = None
    
    def draw(self, img):
        """绘制组件"""
        if not self.visible:
            return
    
    def contains(self, px, py):
        """判断点是否在组件内"""
        return (self.x <= px <= self.x + self.width and
                self.y <= py <= self.y + self.height)

class TextView(UIComponent):
    """文本显示组件"""
    
    def __init__(self, x=0, y=0, width=0, height=0, text='', color=None, font_size=None):
        UIComponent.__init__(self, x, y, width, height)
        self.text = text
        # 设置颜色
        if color is not None:
            self.color = color
        else:
            self.color = COLORS['TEXT']
        # 设置字体大小
        if font_size is not None:
            self.font_size = font_size
        else:
            self.font_size = FONT_SIZES['NORMAL']
        self.align = 'left'  # left, center, right
    
    def draw(self, img):
        if not self.visible or not self.text:
            return
        
        try:
            text = cn(self.text)
            font = ('dense', self.font_size)
            
            # 计算文本位置
            if self.align == 'center':
                text_width = img.measure_text(text, font)[0][2]
                x = self.x + (self.width - text_width) / 2
            elif self.align == 'right':
                text_width = img.measure_text(text, font)[0][2]
                x = self.x + self.width - text_width
            else:
                x = self.x
            
            y = self.y + self.height - 5
            img.text((x, y), text, self.color, font=font)
        except Exception, e:
            print('TextView draw error:', str(e))
            print('Text:', self.text)

class ImageView(UIComponent):
    """图片显示组件"""
    
    def __init__(self, x=0, y=0, width=0, height=0, image=None):
        UIComponent.__init__(self, x, y, width, height)
        self.image = image
        self.scale_type = 'fit'  # fit, fill, center
    
    def set_image(self, image):
        """设置图片"""
        self.image = image
    
    def draw(self, img):
        if not self.visible or not self.image:
            return
        
        try:
            # 调整图片大小
            if self.image.size != (self.width, self.height):
                resized = self.image.resize((self.width, self.height))
                img.blit(resized, target=(self.x, self.y))
            else:
                img.blit(self.image, target=(self.x, self.y))
        except:
            pass

class Button(UIComponent):
    """按钮组件"""
    
    def __init__(self, x=0, y=0, width=0, height=0, text='', callback=None):
        UIComponent.__init__(self, x, y, width, height)
        self.text = text
        self.callback = callback
        self.background = COLORS['PRIMARY']
        self.text_color = 0xFFFFFF
        self.font_size = FONT_SIZES['NORMAL']
        self.focused = False
    
    def draw(self, img):
        if not self.visible:
            return
        
        # 绘制背景
        if self.enabled:
            bg_color = self.background
        else:
            bg_color = COLORS['TEXT_GRAY']
        img.rectangle((self.x, self.y, self.x + self.width, self.y + self.height),
                     fill=bg_color, outline=bg_color)
        
        # 绘制焦点边框
        if self.focused:
            img.rectangle((self.x, self.y, self.x + self.width, self.y + self.height),
                         outline=COLORS['ACCENT'], width=2)
        
        # 绘制文本
        if self.text:
            text = cn(self.text)
            font = ('dense', self.font_size)
            text_width = img.measure_text(text, font)[0][2]
            text_x = self.x + (self.width - text_width) / 2
            text_y = self.y + self.height - 5
            img.text((text_x, text_y), text, self.text_color, font=font)
    
    def on_click(self):
        """点击事件"""
        if self.enabled and self.callback:
            self.callback()

class ListItem(UIComponent):
    """列表项组件"""
    
    def __init__(self, x=0, y=0, width=0, height=0, data=None):
        UIComponent.__init__(self, x, y, width, height)
        self.data = data
        self.selected = False
        self.title = ''
        self.subtitle = ''
        self.image = None
        self.callback = None
    
    def draw(self, img):
        if not self.visible:
            return
        
        # 绘制背景
        if self.selected:
            img.rectangle((self.x, self.y, self.x + self.width, self.y + self.height),
                         fill=COLORS['PRIMARY'], outline=COLORS['PRIMARY'])
        
        padding = 5
        x_offset = self.x + padding
        
        # 绘制图片
        if self.image:
            img_size = min(self.height - padding * 2, 50)
            try:
                resized = self.image.resize((img_size, img_size))
                img.blit(resized, target=(x_offset, self.y + padding))
            except:
                pass
            x_offset += img_size + padding
        
        # 绘制文本
        if self.selected:
            text_color = 0xFFFFFF
            subtitle_color = 0xFFFFFF
        else:
            text_color = COLORS['TEXT']
            subtitle_color = COLORS['TEXT_GRAY']
        
        # 标题
        if self.title:
            title_text = cn(self.title)
            font = ('dense', FONT_SIZES['NORMAL'])
            max_width = self.width - (x_offset - self.x) - padding
            img.text((x_offset, self.y + 20), title_text, text_color, font=font)
        
        # 副标题
        if self.subtitle:
            subtitle_text = cn(self.subtitle)
            font = ('dense', FONT_SIZES['SMALL'])
            img.text((x_offset, self.y + self.height - 10), subtitle_text, subtitle_color, font=font)
    
    def on_click(self):
        """点击事件"""
        if self.callback:
            self.callback(self.data)

class ListView(UIComponent):
    """列表视图组件"""
    
    def __init__(self, x=0, y=0, width=0, height=0):
        UIComponent.__init__(self, x, y, width, height)
        self.items = []
        self.item_height = 60
        self.selected_index = 0
        self.scroll_offset = 0
        self.on_item_click = None
    
    def set_items(self, items):
        """设置列表项"""
        self.items = items
        self.selected_index = 0
        self.scroll_offset = 0
    
    def draw(self, img):
        """绘制视图"""
        if not self.visible:
            return
        
        try:
            # 绘制背景
            if self.background:
                img.rectangle((self.x, self.y, self.x + self.width, self.y + self.height),
                             fill=self.background, outline=self.background)
            
            # 计算可见项
            if len(self.items) == 0:
                return
            
            visible_count = self.height / self.item_height
            start_index = self.scroll_offset
            end_index = min(start_index + visible_count + 1, len(self.items))
            
            # 绘制列表项
            y_offset = self.y - (self.scroll_offset % self.item_height)
            for i in range(start_index, end_index):
                if i >= len(self.items):
                    break
                
                item = self.items[i]
                item.x = self.x
                item.y = y_offset
                item.width = self.width
                item.height = self.item_height
                item.selected = (i == self.selected_index)
                item.draw(img)
                
                y_offset += self.item_height
        except Exception, e:
            print('ListView draw error:', str(e))
    
    def scroll_up(self):
        """向上滚动"""
        if self.selected_index > 0:
            self.selected_index -= 1
            if self.selected_index < self.scroll_offset:
                self.scroll_offset = self.selected_index
    
    def scroll_down(self):
        """向下滚动"""
        if self.selected_index < len(self.items) - 1:
            self.selected_index += 1
            visible_count = self.height / self.item_height
            if self.selected_index >= self.scroll_offset + visible_count:
                self.scroll_offset = self.selected_index - visible_count + 1
    
    def on_select(self):
        """选择当前项"""
        if 0 <= self.selected_index < len(self.items):
            item = self.items[self.selected_index]
            if self.on_item_click:
                self.on_item_click(item.data)
    
    def handle_touch(self, x, y):
        """处理触摸事件"""
        if not self.contains(x, y):
            return False
        
        # 计算点击的是哪一项
        relative_y = y - self.y
        item_index = self.scroll_offset + (relative_y / self.item_height)
        
        if 0 <= item_index < len(self.items):
            self.selected_index = item_index
            self.on_select()
            return True
        
        return False

class ProgressBar(UIComponent):
    """进度条组件"""
    
    def __init__(self, x=0, y=0, width=0, height=0):
        UIComponent.__init__(self, x, y, width, height)
        self.progress = 0.0  # 0.0 ~ 1.0
        self.color = COLORS['PLAYING_BAR']
        self.bg_color = COLORS['DIVIDER']
    
    def set_progress(self, value):
        """设置进度 0.0 ~ 1.0"""
        self.progress = max(0.0, min(1.0, value))
    
    def draw(self, img):
        if not self.visible:
            return
        
        # 绘制背景
        img.rectangle((self.x, self.y, self.x + self.width, self.y + self.height),
                     fill=self.bg_color, outline=self.bg_color)
        
        # 绘制进度
        if self.progress > 0:
            progress_width = int(self.width * self.progress)
            if progress_width > 0:
                img.rectangle((self.x, self.y, self.x + progress_width, self.y + self.height),
                             fill=self.color, outline=self.color)
