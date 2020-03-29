var info = { //应用属性
   appname: '百度贴吧客户端',
   version: '0.0.1',
   summary: '专门为简化登录百度贴吧而诞生。',
   thanks: '塞班S60V3吧的有福了，',
   website: 'http://tieba.baidu.com/mo/m?kw=%E5%A1%9E%E7%8F%ADs60v3'
};
var CMD = { //菜单执行的命令
   aaa : 1, //登录
   aab: 2, //贴吧首页
   aac: 3, //我的i贴吧
   aad: 4, //退出
};
var menu_aaa = new MenuItem('登录', CMD.aaa),
     menu_aab = new MenuItem('贴吧首页', CMD.aab),
     menu_aac = new MenuItem('我的i贴吧', CMD.aac),
     menu_aad = new MenuItem('退出', CMD.aad);
menu_aaa.onSelect = selectMenu;
menu_aab.onSelect = selectMenu;
menu_aac.onSelect = selectMenu;
menu_aad.onSelect = selectMenu;
//-----------------------------------------------
