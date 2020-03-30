var page_list = 1, page_comments = 1, list_top = 0, ref_page = 'list' ,last_page = 'list'; //当前页码
var isloading = 0;
var info = { //应用属性
	appname: '百度贴吧s60v3客户端',
	version: '0.0.0.1',
	summary: '贴吧即百度贴吧，是百度旗下独立品牌，全球最大的中文社区。贴吧的创意来自于百度首席执行官李彦宏：结合搜索引擎建立一个在线的交流平台，让那些对同一个话题感兴趣的人们聚集在一起，方便地展开交流和互相帮助。贴吧是一种基于关键词的主题交流社区，它与搜索紧密结合，准确把握用户需求，为兴趣而生。',
	thanks: '感谢塞班s60v3吧吧群(群号:140369358)的小伙伴们一直以来的支持~',
	website: 'www.ithome.com'
};
var CMD = { //菜单执行的命令
	refersh : 1, //刷新
	about: 2, //关于
	comment: 3, //评论写 
	login: 5, //登录
	checkVersion : 6, //检查新版本
	logout: 7, //注销
	comments: 8 //查看评论
};
var menu_refersh = new MenuItem('刷新', CMD.refersh),
	  menu_about = new MenuItem('关于', CMD.about), 
	  menu_login = new MenuItem('登录', CMD.login),
	  menu_logout = new MenuItem('注销', CMD.logout),
	  menu_checkVersion = new MenuItem('检查新版本', CMD.checkVersion),
	  menu_comments = new MenuItem('查看评论', CMD.comments),
	  menu_comment = new MenuItem('写评论', CMD.comment);
menu_refersh.onSelect = selectMenu;
menu_about.onSelect = selectMenu;
menu_comments.onSelect = selectMenu;
menu_comment.onSelect = selectMenu; 
menu_login.onSelect = selectMenu;
menu_logout.onSelect = selectMenu;
menu_checkVersion.onSelect = selectMenu;
//-----------------------------------------------
function showPage(id) { //显示id和隐藏其它页面
	var pages = [
		'login_form', 
		'about',
		'list',
		'article',
		'comments',
		'loading'
	];
	pages.myforEach(function(item) { 
	  
		if(id === 'loading')
		{  
			//alert(item);
			getById(id).style.display = 'block';
			//getById(last_page).style.display = 'block';
			isloading = 1;
			
			menu.setRightSoftkeyLabel('取消', function() {isloading = 0;resetLRkey();showPage(last_page); });
			
			menu.setLeftSoftkeyLabel('  ', function(){});  //左键复位
			//alert(111);
			return;
		};
		
		if (id === item) {
			last_page = id;
			getById(id).style.display = 'block';
			isloading = 0;
			if (id === 'list') {
				setTitle();
				setRightSoftkeyLabel('', null); //右键退出
				setLeftSoftkeyLabel('', null); //左键复位
				menu.remove(menu_comment);
				menu.remove(menu_comments);
				menu.append(menu_about);
				menu.append(menu_checkVersion);
				menu.append(menu_refersh);
			} else if (id === 'article') {
				document.body.scrollTop = 0;
				setLeftSoftkeyLabel('', null); //左键复位
				setRightSoftkeyLabel('返回', function() {
					document.body.scrollTop = list_top;
					setTitle();
					showPage('list');
				}); //右键返回
				if (widget.preferenceForKey('userhash')) {menu.append(menu_comment);}
				menu.append(menu_comments);
				menu.remove(menu_about);
				menu.remove(menu_checkVersion);
				menu.remove(menu_refersh);
			} else if (id === 'comments') {
				document.body.scrollTop = 0;
				setLeftSoftkeyLabel('', null); //左键复位
				setRightSoftkeyLabel('返回', function() {
					document.body.scrollTop = list_top;
					showPage('article');
				}); //右键返回
				menu.remove(menu_comments);
			}
		} else {
			getById(item).style.display = 'none';
		}
	}); 
	
}
function setTitle(str) { //设置标题栏
	getById('topic').textContent = str || 'IT之家-新闻资讯';
}

lastnewsTime = '';

function displayList(hash) { //显示文章列表 
	showPage('loading');//显示加载动画 
	ref_page = 'list';  
	var option = function(){};
	option.isphone =1;
	option.un ='123456789';
	option.passwd= '123456789';
	login(option,function(data){alert(data)},function(data){alert(data)});
	/*ajax_get('http://api.ithome.com/json/listpage/news/'+hash, function(error, data) {
		if (error) {
			alert(error);
		} else {
			
			var articles = [];
			if(data.toplist)
			{
				data.toplist.myforEach(function(item) { 
					articles.push('<li><a href="javascript:displayArticle(\''+escape(JSON.stringify(item))+'\')">'+ '<img  src="'+item.image+'" alt="图片" />'+'<div><h3 style="color:red">[置顶]'+item.title+'</h3><p><span>'+humanedate(item.postdate)+'</span><span>评论('+item.commentcount+')</span></p></div></a></li>');
				});
			}
			
			data.newslist.myforEach(function(item) { 
				articles.push('<li><a href="javascript:displayArticle(\''+escape(JSON.stringify(item))+'\')">'+ '<img  src="'+item.image+'" alt="图片" />'+'<div><h3>'+item.title+'</h3><p><span>'+humanedate(item.postdate)+'</span><span>评论('+item.commentcount+')</span></p></div></a></li>');
				lastnewsTime = item.orderdate; 
			});
			if (hash!=0) { //提供了url说明是下一页
				getById('list').innerHTML += articles.join('');
			} else {
				getById('list').innerHTML = articles.join('');
			}
			//删掉next按钮
			var next_button = getById('next_button');
			if (next_button) { //原来有next按钮
				next_button.parentNode.removeChild(next_button);
			}
			
			if(data.newslist.length>0)
			{
				getById('list').innerHTML += '<li id="next_button"><a href="javascript:displayList(\''+get_next(lastnewsTime)+'\')">加载更多……</a></li>';
			}
			else
			{
				getById('list').innerHTML += '<div class="bottom">我们是有底线的</div>';
				
			} 
			
			showPage('list');
			//showPage('loading');//显示加载动画
			if (hash!=0) {
				document.body.scrollTop += 20;
			}
		}
		
	});*/	
}

function displayArticle(item) { //显示文章正文
	showPage('loading');//显示加载动画
	item = JSON.parse(unescape(item))
	//getById('content').className = item.newsid;
	//displayComments('0')
	//return; // http://dyn.ithome.com/api/comment/getnewscomment?sn=4c70d4f5c7bdb61f&cid=48966977 
	
	ref_page = 'article';
	url='http://api.ithome.com/json/newscontent/'+item.newsid
	list_top = document.body.scrollTop;
	ajax_get(url, function(error, data) {
		if (error) {
			alert(error);
		} else {
			setTitle(item.title);
			getById('dateline').textContent = dateline(item.postdate);
			getById('author').textContent = data.newssource+'('+data.newsauthor+')'; 
			getById('comment_num').innerHTML = '<a href="javascript:displayComments(0)">评论('+item.commentcount+')</a>';
			getById('content').innerHTML = UBB(data.detail);
			getById('content').className = item.newsid;
			showPage('article');
		}
	});
}

lastCommentCi = ''

function displayComments(Ci) { //显示评论列表TODO 
	showPage('loading');//显示加载动画
	ref_page = 'comments';
	url =  'http://dyn.ithome.com/api/comment/getnewscomment?sn='+getCommentSn(getById('content').className);
	 
	if(Ci!=0)
	{
		url=url+'&cid='+Ci;
	}
	ajax_get(url, function(error, data) {
		if (error) {
			alert(error);
		} else {
			var comments = [];
			data.clist.myforEach(function(item) {
				item = item.M;
				comments.push('<li><img src="'+getHeadUrl(item.Ui)+'" alt="头像" onerror=\"onerror=null;src=\'img/avatar_default_rect.png\'\" />  <div><h3>'+item.N+' ('+item.SF+')</h3><p><span>'+dateline(item.T)+'</span><span>'+item.Ta+'</span></p><p>'+item.C+'</p></div></li>');
				lastCommentCi = item.Ci;
			});
			if(Ci!=0) { //提供了url说明是下一页
				getById('comments').innerHTML += comments.join('');
			} else {
				getById('comments').innerHTML = comments.join('');
			}
			//删掉next按钮
			var next_button_comments = getById('next_button_comments');
			if (next_button_comments) { //原来有next按钮
				next_button_comments.parentNode.removeChild(next_button_comments);
			}
			 
			if (data.clist.length>0) {
				getById('comments').innerHTML += '<li id="next_button_comments"><a href="javascript:displayComments(\''+lastCommentCi+'\')">加载更多……</a></li>'; 
			} 
			else
			{
				getById('comments').innerHTML += '<div class="bottom">我们是有底线的</div>';
				
			} 
			
			showPage('comments');
		}
	});
}

function compareVer(oldver,newver)
{
	var a = oldver.split('.');
	var b = newver.split('.');
	
	for(var i = 0;i<a.length;i++)
	{
		if(b[i]>a[i])
		{
			return true;
		}
		else if(b[i]===a[i])
		{
			continue;
		}
		else if(b[i]<a[i])
		{
			return false;
		}
	}
	return false;
}

function checkUpdate()
{ 
	showPage('loading');
	url='http://sss.wmm521.cn/symbian/ithome_ver.json?_='+(new Date().getTime());
	 
	ajax_get(url, function(error, data) {
			 
			if (error) {
				alert(error);
			} else if (compareVer(info.version,data.version)) {
				//有新版本
				alert('有新版本，版本号：'+data.version);
				widget.openURL(data.downloadUrl);
			} else {
				alert('您的版本已经是最新版本。');
			}
			showPage(ref_page);
		});
}
//checkUpdate();
function selectMenu(id) { //选择了菜单项
	if (id === CMD.refersh) { //点击刷新
		displayList(0);
	} else if (id === CMD.about) { //点击关于
		showPage('about');
		setRightSoftkeyLabel('返回', function() {
			showPage('list');
		}); //右键返回
		setLeftSoftkeyLabel('隐藏', function() {
			showPage('list');
		});
	} else if (id === CMD.checkVersion) { 
		checkUpdate();
	} else if (id === CMD.comment) { //发布评论
		var content = prompt('评论内容：');
		if (content) {
			//var so = device.getServiceObject('Service.SysInfo', 'ISysInfo');
			//var result = so.ISysInfo.GetInfo({Entity: 'Device', Key: 'PhoneModel'});
			//var model = '网页';
			showPage('loading');
			ajax_post2('http://dyn.ithome.com/ithome/postcomment.aspx', getCommentParam(getById('content').className,content),function(error, data) {
				if (error) {
					alert(error);
					showPage(ref_page);
				} else { 
					alert(data);
					displayComments('0');
				}
			});
		}
	}  else if (id === CMD.login) { //选择登录
		showPage('login_form');
		getByName('login_email')[0].focus();
		setLeftSoftkeyLabel('提交', function() {
			var email = getByName('login_email')[0].value,  password = getByName('login_password')[0].value;
			if (!email || !password) {
				alert('请填写用户名和密码。');
				return false;
			}
			var userhash = getUserHash(email,password);
			var url = getUserDataUrl(userhash);
			showPage('loading');
			ajax_get( url,function(error, data) {
				if (error) {
					alert(error);
				} else {
					if(data.ok === 1)
					{ 
						alert("登陆成功");
						widget.setPreferenceForKey(userhash, 'userhash');
						widget.setPreferenceForKey(data.userinfo.username, 'email');
						widget.setPreferenceForKey(getMd5(password), 'password'); 
						widget.setPreferenceForKey(data.userinfo.nickname, 'nickname');
						menu.append(menu_logout);
						menu.remove(menu_login); 
						showPage(ref_page);
					}
					else
					{
						alert(data.msg);
						showPage(ref_page);
					} 
				}
			});
		});
		setRightSoftkeyLabel('返回', function() {
			showPage(ref_page);
		});
	} else if (id === CMD.logout) {
		menu.remove(menu_logout); 
		menu.append(menu_login);
		widget.setPreferenceForKey(null, 'userhash');
		widget.setPreferenceForKey(null, 'email');
		widget.setPreferenceForKey(null, 'password');
		widget.setPreferenceForKey(null, 'nickname');
		alert('注销成功！');
	} else if (id === CMD.comments) { //查看评论页面
		displayComments('0');
	}
}

window.onload = function() { //应用载入之后开始执行。
	getById('about').innerHTML = '<h3>'+info.appname+'</h3><p>版本：'+info.version+'</p><p>简介：'+info.summary+'</p><p>感谢：'+info.thanks+'</p><p>官方网站：'+info.website+'</p>';
	widget.setNavigationEnabled(false); //设置成按键控制
	menu.append(menu_refersh);
	if (widget.preferenceForKey('userhash')) {
		menu.append(menu_logout);
	} else { 
		menu.append(menu_login);
	}
	menu.append(menu_about);
	menu.append(menu_checkVersion); 
	 
	var timer = setTimeout(function() {
		document.body.removeChild(getById('wellcome')); //关闭欢迎界面
		displayList(0); 
		menu.showSoftkeys(); 
		clearTimeout(timer);
	}, 0);
};