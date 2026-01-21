# -*- coding: utf-8 -*-
"""
网易云音乐 API 模块
兼容 Python 2.2+ 语法
"""
import httplib
import urllib
import time
try:
    import json
except:
    import simplejson as json

from config import API_BASE_URL
from utils import get_timestamp, cn

class NCMApi(object):
    """网易云音乐 API 封装"""
    
    def __init__(self, base_url=None):
        if base_url:
            self.base_url = base_url
        else:
            self.base_url = API_BASE_URL
    
    def _send_request(self, path, method='GET', data=None):
        """发送 HTTP 请求"""
        try:
            # 解析 URL
            if self.base_url.startswith('https://'):
                host = self.base_url[8:]
                use_https = True
            else:
                if self.base_url.startswith('http://'):
                    host = self.base_url[7:]
                else:
                    host = self.base_url
                use_https = False
            
            # 移除端口号中的路径
            if '/' in host:
                host = host[:host.index('/')]
            
            # 处理端口
            if ':' in host:
                host_parts = host.split(':')
                hostname = host_parts[0]
                port = int(host_parts[1])
            else:
                hostname = host
                if use_https:
                    port = 443
                else:
                    port = 80
            
            # 创建连接
            if use_https:
                conn = httplib.HTTPSConnection(hostname, port)
            else:
                conn = httplib.HTTPConnection(hostname, port)
            
            # 准备请求
            url = path
            headers = {
                'User-Agent': 'Mozilla/5.0 (Symbian/3; Series60/5.0)',
            }
            
            if method == 'POST' and data:
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                if isinstance(data, dict):
                    body = urllib.urlencode(data)
                else:
                    body = data
            else:
                body = None
            
            # 发送请求
            conn.request(method, url, body, headers)
            response = conn.getresponse()
            result = response.read()
            conn.close()
            
            return result
        except Exception, e:
            print('Request error:', str(e))
            return None
    
    def _get(self, path):
        """GET 请求"""
        return self._send_request(path, 'GET')
    
    def _post(self, path, data=None):
        """POST 请求"""
        return self._send_request(path, 'POST', data)
    
    def _parse_json(self, text):
        """解析 JSON"""
        if not text:
            return None
        try:
            return json.loads(text)
        except:
            return None
    
    # 搜索相关接口
    def search_song(self, keyword, limit=20, offset=0):
        """搜索歌曲"""
        path = '/cloudsearch?keywords=%s&type=1&limit=%d&offset=%d' % (
            urllib.quote(keyword.encode('utf-8')), limit, offset
        )
        result = self._get(path)
        return self._parse_json(result)
    
    def search_playlist(self, keyword, limit=20, offset=0):
        """搜索歌单"""
        path = '/cloudsearch?keywords=%s&type=1000&limit=%d&offset=%d' % (
            urllib.quote(keyword.encode('utf-8')), limit, offset
        )
        result = self._get(path)
        return self._parse_json(result)
    
    # 歌单相关接口
    def get_playlist_detail(self, playlist_id):
        """获取歌单详情"""
        path = '/playlist/detail?id=%s' % playlist_id
        result = self._get(path)
        return self._parse_json(result)
    
    def get_personalized_playlist(self, limit=20):
        """获取推荐歌单"""
        path = '/personalized?limit=%d' % limit
        result = self._get(path)
        return self._parse_json(result)
    
    def get_top_playlist(self, limit=20, offset=0, cat='全部'):
        """获取热门歌单"""
        path = '/top/playlist?limit=%d&offset=%d&cat=%s' % (
            limit, offset, urllib.quote(cat.encode('utf-8'))
        )
        result = self._get(path)
        return self._parse_json(result)
    
    # 歌曲相关接口
    def get_song_detail(self, song_ids):
        """获取歌曲详情"""
        if isinstance(song_ids, list):
            ids_str = ','.join([str(i) for i in song_ids])
        else:
            ids_str = str(song_ids)
        path = '/song/detail?ids=%s' % ids_str
        result = self._get(path)
        return self._parse_json(result)
    
    def get_song_url(self, song_id, br=128000):
        """获取歌曲播放地址"""
        path = '/song/url?id=%s&br=%d' % (song_id, br)
        result = self._get(path)
        return self._parse_json(result)
    
    def get_lyric(self, song_id):
        """获取歌词"""
        path = '/lyric?id=%s' % song_id
        result = self._get(path)
        return self._parse_json(result)
    
    # 推荐相关接口
    def get_personalized_newsong(self, limit=20):
        """获取推荐新歌"""
        path = '/personalized/newsong?limit=%d' % limit
        result = self._get(path)
        return self._parse_json(result)
    
    def get_banner(self):
        """获取首页轮播图"""
        path = '/banner?type=1'
        result = self._get(path)
        return self._parse_json(result)
    
    # 登录相关接口
    def login_qr_key(self):
        """获取二维码登录 key"""
        path = '/login/qr/key?timestamp=%s' % get_timestamp()
        result = self._get(path)
        return self._parse_json(result)
    
    def login_qr_create(self, key):
        """生成二维码"""
        path = '/login/qr/create?key=%s&qrimg=1&timestamp=%s' % (key, get_timestamp())
        result = self._get(path)
        return self._parse_json(result)
    
    def login_qr_check(self, key):
        """检查二维码登录状态"""
        path = '/login/qr/check?key=%s&timestamp=%s' % (key, get_timestamp())
        result = self._get(path)
        return self._parse_json(result)
    
    def login_status(self):
        """获取登录状态"""
        path = '/login/status?timestamp=%s' % get_timestamp()
        result = self._get(path)
        return self._parse_json(result)
    
    # 用户相关接口
    def get_user_playlist(self, uid, limit=30, offset=0):
        """获取用户歌单"""
        path = '/user/playlist?uid=%s&limit=%d&offset=%d' % (uid, limit, offset)
        result = self._get(path)
        return self._parse_json(result)

# 全局 API 实例
api = NCMApi()
