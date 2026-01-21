# -*- coding: utf-8 -*-
"""
网易云音乐 API 模块
基于 NeteaseCloudMusic.ts 的 API 定义
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
    
    def _send_request(self, path, method='GET', data=None, headers=None):
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
            
            # 移除路径部分
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
            
            # 准备请求头
            req_headers = {
                'User-Agent': 'Mozilla/5.0 (Symbian/3; Series60/5.0)',
                'Accept': 'application/json',
            }
            if headers:
                req_headers.update(headers)
            
            # 准备请求体
            if method == 'POST' and data:
                req_headers['Content-Type'] = 'application/x-www-form-urlencoded'
                if isinstance(data, dict):
                    body = urllib.urlencode(data)
                else:
                    body = data
            else:
                body = None
            
            # 发送请求
            conn.request(method, path, body, req_headers)
            response = conn.getresponse()
            result = response.read()
            conn.close()
            
            return result
        except Exception, e:
            print('Request error:', str(e))
            import traceback
            traceback.print_exc()
            return None
    
    def _get(self, path, headers=None):
        """GET 请求"""
        return self._send_request(path, 'GET', None, headers)
    
    def _post(self, path, data=None, headers=None):
        """POST 请求"""
        return self._send_request(path, 'POST', data, headers)
    
    def _parse_json(self, text):
        """解析 JSON"""
        if not text:
            return None
        try:
            return json.loads(text)
        except Exception, e:
            print('Parse JSON error:', str(e))
            return None
    
    # ==================== PlayList API ====================
    def playlist_detail(self, playlist_id, s=8, n=100000):
        """
        获取歌单详情
        POST /api/v6/playlist/detail
        """
        data = {
            'id': str(playlist_id),
            's': str(s),
            'n': str(n),
        }
        result = self._post('/api/v6/playlist/detail', data)
        return self._parse_json(result)
    
    # ==================== Song API ====================
    def song_detail(self, song_ids):
        """
        获取歌曲详情
        POST /api/v3/song/detail
        c: JSON数组字符串，如 [{"id":123},{"id":456}]
        """
        if isinstance(song_ids, list):
            c_list = [{'id': int(sid)} for sid in song_ids]
        else:
            c_list = [{'id': int(song_ids)}]
        
        c_str = json.dumps(c_list)
        data = {'c': c_str}
        result = self._post('/api/v3/song/detail', data)
        return self._parse_json(result)
    
    def song_url(self, song_id):
        """
        获取歌曲播放地址
        GET /api/v3/song/url
        """
        path = '/api/v3/song/url?id=%s' % str(song_id)
        result = self._get(path)
        return self._parse_json(result)
    
    def song_enhance_player_url(self, song_ids, level='standard', encode_type='mp3'):
        """
        获取增强播放地址（更高音质）
        POST /api/song/enhance/player/url/v1
        level: standard, exhigh, lossless, hires
        encodeType: flac, aac, mp3
        """
        if isinstance(song_ids, list):
            ids_str = json.dumps(song_ids)
        else:
            ids_str = '[%s]' % str(song_ids)
        
        data = {
            'ids': ids_str,
            'level': level,
            'encodeType': encode_type,
        }
        result = self._post('/api/song/enhance/player/url/v1', data)
        return self._parse_json(result)
    
    def song_lyric(self, song_id):
        """
        获取歌词
        POST /api/song/lyric
        """
        data = {
            'id': str(song_id),
            'tv': '-1',
            'lv': '-1',
            'rv': '-1',
            'kv': '-1',
        }
        headers = {'Cookie': 'os=ios'}
        result = self._post('/api/song/lyric?_nmclfl=1', data, headers)
        return self._parse_json(result)
    
    # ==================== Banner API ====================
    def banner_get(self, client_type='pc'):
        """
        获取轮播图
        POST /api/v2/banner/get
        """
        data = {'clientType': client_type}
        result = self._post('/api/v2/banner/get', data)
        return self._parse_json(result)
    
    # ==================== Personalized API ====================
    def personalized_playlist(self, limit=20, offset=0):
        """
        获取推荐歌单
        POST /api/personalized/playlist
        """
        data = {
            'limit': str(limit),
        }
        if offset > 0:
            data['offset'] = str(offset)
        result = self._post('/api/personalized/playlist', data)
        return self._parse_json(result)
    
    def personalized_newsong(self, limit=20, area_id=0):
        """
        获取推荐新歌
        POST /api/personalized/newsong
        """
        data = {
            'type': 'recommend',
            'limit': str(limit),
        }
        if area_id > 0:
            data['areaId'] = str(area_id)
        result = self._post('/api/personalized/newsong', data)
        return self._parse_json(result)
    
    # ==================== CloudSearch API ====================
    def cloudsearch(self, keyword, search_type=1, limit=20, offset=0):
        """
        云搜索
        POST /api/cloudsearch/pc
        type: 1-单曲, 10-专辑, 100-歌手, 1000-歌单, 1002-用户, 1004-MV, 1006-歌词, 1009-电台, 1014-视频
        """
        data = {
            's': keyword,
            'type': str(search_type),
            'limit': str(limit),
            'offset': str(offset),
        }
        result = self._post('/api/cloudsearch/pc', data)
        return self._parse_json(result)
    
    # ==================== Top API ====================
    def top_playlist(self, order='hot', cat='全部', limit=20, offset=0):
        """
        获取热门歌单
        GET /playlist
        """
        path = '/playlist?order=%s&cat=%s&limit=%d&offset=%d' % (
            order,
            urllib.quote(cat.encode('utf-8')),
            limit,
            offset
        )
        result = self._get(path)
        return self._parse_json(result)
    
    def top_song(self, limit=100, area_id=0):
        """
        获取新歌榜
        POST /weapi/v1/discovery/new/songs
        """
        data = {}
        if limit > 0:
            data['limit'] = str(limit)
        if area_id > 0:
            data['areaId'] = str(area_id)
        result = self._post('/weapi/v1/discovery/new/songs', data)
        return self._parse_json(result)
    
    def top_album(self, album_type='new', area='ALL', limit=50, offset=0):
        """
        获取新碟榜
        POST /api/discovery/new/albums/area
        """
        data = {
            'type': album_type,
            'area': area,
            'limit': str(limit),
            'offset': str(offset),
        }
        result = self._post('/api/discovery/new/albums/area', data)
        return self._parse_json(result)
    
    # ==================== Login API ====================
    def login_cellphone(self, phone, password, countrycode='86'):
        """
        手机号登录
        POST /api/login/cellphone
        """
        data = {
            'phone': phone,
            'password': password,
            'countrycode': countrycode,
            'rememberLogin': 'true',
        }
        headers = {'Cookie': 'os=ios; appver=8.7.01'}
        result = self._post('/api/login/cellphone', data, headers)
        return self._parse_json(result)
    
    def login_qrcode_unikey(self):
        """
        获取二维码登录key
        POST /api/login/qrcode/unikey
        """
        data = {'type': '1'}
        headers = {'Cookie': 'os=ios; appver=8.7.01'}
        result = self._post('/api/login/qrcode/unikey', data, headers)
        return self._parse_json(result)
    
    def login_qrcode_client(self, key):
        """
        二维码登录
        POST /api/login/qrcode/client/login
        """
        data = {
            'type': '1',
            'key': key,
        }
        headers = {'Cookie': 'os=ios; appver=8.7.01'}
        result = self._post('/api/login/qrcode/client/login', data, headers)
        return self._parse_json(result)
    
    # ==================== User API ====================
    def user_playlist(self, uid, limit=30, offset=0, include_video=True):
        """
        获取用户歌单
        POST /api/user/playlist
        """
        data = {
            'uid': str(uid),
            'limit': str(limit),
            'offset': str(offset),
            'includeVideo': 'true' if include_video else 'false',
        }
        result = self._post('/api/user/playlist', data)
        return self._parse_json(result)
    
    def user_account(self):
        """
        获取用户账号信息
        POST /api/nuser/account/get
        """
        result = self._post('/api/nuser/account/get', {})
        return self._parse_json(result)
    
    # ==================== Resource API ====================
    def resource_comments(self, thread_id, page_no=1, page_size=20, cursor=0, sort_type=99):
        """
        获取评论
        POST /api/v2/resource/comments
        sortType: 99-推荐, 2-热度, 3-时间
        """
        data = {
            'threadId': thread_id,
            'pageNo': str(page_no),
            'pageSize': str(page_size),
            'cursor': str(cursor),
            'sortType': str(sort_type),
            'showInner': 'true',
        }
        headers = {'Cookie': 'os=pc'}
        result = self._post('/api/v2/resource/comments', data, headers)
        return self._parse_json(result)

# 全局 API 实例
api = NCMApi()
