# -*- coding: utf-8 -*-
import mypath
mypath = mypath.getmypath("\\python\\pysoft\\pyqq\\")
cachePath = mypath + "cache\\"
cn = lambda x: x.decode("u8")
#qq开放sdk，封装qq协议基本操作
class QQSDK:
    def __init__(self):
        self.qq=''
        self.pwd = ''

        #初始化状态
        self.status_init = 0
        #登录中
        self.status_logining = 1
        #登陆成功
        self.status_loginsuccess = 2
        #登陆失败
        self.status_loginfail = 3
        #需要验证码
        self.status_needvcode = 4
        #需要设备验证
        self.status_needdeviceverify = 5

        self.status = self.status_init

    def init(self,qq,pwd):
        print('初始化qq')
        self.qq = qq
        self.pwd = pwd
    def logout(self):
        print('退出登录')
        self.status = self.status_init

    #登陆，返回状态码
    def login(self,vcode = ''):
        print('登录qq：'+self.qq)
        self.status =  self.status_loginsuccess
        return self.status

    #上线
    def online(self):
        pass
    #下线
    def offline(self):
        pass
    #获取验证码
    def getVcode(self):
        pass

    def getHeadImgPath(self):
        return mypath+"qqheadimg.jpg"

    def getNickName(self):
        return '小小星'

    #获取好友列表
    def getFriendList(self):
        if(self.status != self.status_loginsuccess):
            print('请先登录')
            return '请先登录'
        friendlist = {
            '分组1':
                {
                    'mems':[
                        {
                            'uin':'1311817771',
                            'name':'紫星'
                        },
                        {
                            'uin': '10001',
                            'name': 'pony'
                        }
                    ]
                }
            ,
            '分组2':
                {
                    'mems': [
                        {
                            'uin': '123456',
                            'name': 'babyQ'
                        },
                        {
                            'uin': '304150791',
                            'name': '小小星'
                        }
                    ]
                }
            ,
            '分组3':
                {
                    'mems': [
                        {
                            'uin': '123456',
                            'name': 'babyQ'
                        },
                        {
                            'uin': '304150791',
                            'name': '小小星'
                        }
                    ]
                }
            ,
            '分组4':
                {
                    'mems': [
                        {
                            'uin': '123456',
                            'name': 'babyQ'
                        },
                        {
                            'uin': '304150791',
                            'name': '小小星'
                        }
                    ]
                }
            ,
            '分组5':
                {
                    'mems': [
                        {
                            'uin': '123456',
                            'name': 'babyQ'
                        },
                        {
                            'uin': '304150791',
                            'name': '小小星'
                        }
                    ]
                }
            ,
            '分组6':
                {
                    'mems': [
                        {
                            'uin': '123456',
                            'name': 'babyQ'
                        },
                        {
                            'uin': '304150791',
                            'name': '小小星'
                        }
                    ]
                }
            ,
            '分组7':
                {
                    'mems': [
                        {
                            'uin': '123456',
                            'name': 'babyQ'
                        },
                        {
                            'uin': '304150791',
                            'name': '小小星'
                        }
                    ]
                }
        }
        return friendlist

    #获取群列表
    def getGroupList(self):
        pass

    #发送好友消息
    def sendFriendMsg(self,qq,msg):
        pass

    #发送群消息
    def sendGroupMsg(self,group,msg):
        pass
    #刷新好友列表
    def refreshFriendList(self):
        pass
    #刷新群列表
    def refreshGroupList(self):
        pass







