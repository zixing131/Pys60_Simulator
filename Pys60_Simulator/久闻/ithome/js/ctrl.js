var page_list = 1, page_comments = 1, list_top = 0, ref_page = 'list'; //当前页码
const info = { //应用属性
	appname: 'IT之家s60v3客户端',
	version: '0.0.1',
	summary: '“IT之家”是业内领先的IT资讯和数码产品类网站。IT之家快速精选泛科技新闻，分享即时的IT业界动态和紧跟潮流的数码产品资讯，提供给力的PC和手机技术文章、丰富的系统应用美化资源，以及享不尽的智能阅读。',
	thanks: '感谢塞班s60v3吧吧群的小伙伴们一直以来的支持~',
	website: 'www.ithome.com'
};
const CMD = { //菜单执行的命令
	refersh : 1, //刷新
	about: 2, //关于
	comment: 3, //评论写
	reg: 4, //注册
	login: 5, //登录
	checkVersion : 6, //检查新版本
	logout: 7, //注销
	comments: 8 //查看评论
};
const menu_refersh = new MenuItem('刷新', CMD.refersh),
	  menu_about = new MenuItem('关于', CMD.about),
	  menu_reg = new MenuItem('注册', CMD.reg),
	  menu_login = new MenuItem('登录', CMD.login),
	  menu_logout = new MenuItem('注销', CMD.logout),
	  menu_checkVersion = new MenuItem('检查新版本', CMD.checkVersion),
	  menu_comments = new MenuItem('查看评论', CMD.comments),
	  menu_comment = new MenuItem('写评论', CMD.comment);
menu_refersh.onSelect = selectMenu;
menu_about.onSelect = selectMenu;
menu_comments.onSelect = selectMenu;
menu_comment.onSelect = selectMenu;
menu_reg.onSelect = selectMenu;
menu_login.onSelect = selectMenu;
menu_logout.onSelect = selectMenu;
menu_checkVersion.onSelect = selectMenu;
//-----------------------------------------------
function showPage(id) { //显示id和隐藏其它页面
	const pages = [
		'login_form',
		'reg_form',
		'about',
		'list',
		'article',
		'comments'
	];
	pages.forEach(function(item) {
		if (id === item) {
			getById(id).style.display = 'block';
			if (id === 'list') {
				setTitle();
				menu.setRightSoftkeyLabel('', null); //右键退出
				menu.setLeftSoftkeyLabel('', null); //左键复位
				menu.remove(menu_comment);
				menu.remove(menu_comments);
				menu.append(menu_about);
				menu.append(menu_checkVersion);
				menu.append(menu_refersh);
			} else if (id === 'article') {
				document.body.scrollTop = 0;
				menu.setLeftSoftkeyLabel('', null); //左键复位
				menu.setRightSoftkeyLabel('返回', function() {
					document.body.scrollTop = list_top;
					setTitle();
					showPage('list');
				}); //右键返回
				if (widget.preferenceForKey('auth')) {menu.append(menu_comment);}
				menu.append(menu_comments);
				menu.remove(menu_about);
				menu.remove(menu_checkVersion);
				menu.remove(menu_refersh);
			} else if (id === 'comments') {
				document.body.scrollTop = 0;
				menu.setLeftSoftkeyLabel('', null); //左键复位
				menu.setRightSoftkeyLabel('返回', function() {
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
function displayList(url) { //显示文章列表
	ref_page = 'list';
	ajax_get('http://api.ithome.com/json/newslist/news?r=0', function(error, data) {
		if (error) {
			alert(error);
		} else {
			const articles = [];
			data.newslist.forEach(function(item) { 
				articles.push('<li><a href="javascript:displayArticle(\''+escape(JSON.stringify(item))+'\')">'+ '<img src="'+item.image+'" alt="截图" />'+'<div><h3>'+item.title+'</h3><p><span>评论('+item.commentcount+')</span><span>人气('+item.hitcount+')</span></p></div></a></li>');
			});
			if (url && /next/.test(url)) { //提供了url说明是下一页
				getById('list').innerHTML += articles.join('');
			} else {
				getById('list').innerHTML = articles.join('');
			}
			//删掉next按钮
			const next_button = getById('next_button');
			if (next_button) { //原来有next按钮
				next_button.parentNode.removeChild(next_button);
			}
			/*
			if (page_list < data.pager.pages) {
				getById('list').innerHTML += '<li id="next_button"><a href="javascript:displayList(\''+data.pager.last_dateline+'/next/'+data.pager.next_page+'\')">加载更多……</a></li>';
				page_list = data.pager.page;
			}
			*/
			showPage('list');
			if (/next/.test(url)) {
				document.body.scrollTop += 20;
			}
		}
	});
}
function displayArticle(item) { //显示文章正文
	item = JSON.parse(unescape(item))
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
			getById('comment_num').textContent = '评论('+item.commentcount+')';
			getById('content').innerHTML = UBB(data.detail);
			getById('content').className = item.newsid;
			showPage('article');
		}
	});
}
function displayComments(url) { //显示评论列表TODO
	ref_page = 'comments';
	ajax_get('http://api2.9smart.cn/comments/'+getById('content').className+ (url?'/'+url:''), function(error, data) {
		if (error) {
			alert(error);
		} else {
			const comments = [];
			data.comments.forEach(function(item) {
				comments.push('<li><img src="'+item.user.avatar+'" alt="头像" /><div><h3>'+item.user.nickname+'</h3><p><span>'+dateline(item.dateline)+'</span><span>'+item.model+'</span></p><p>'+item.content+'</p></div></li>');
			});
			if (url && /next/.test(url)) { //提供了url说明是下一页
				getById('comments').innerHTML += comments.join('');
			} else {
				getById('comments').innerHTML = comments.join('');
			}
			//删掉next按钮
			const next_button_comments = getById('next_button_comments');
			if (next_button_comments) { //原来有next按钮
				next_button_comments.parentNode.removeChild(next_button_comments);
			}
			if (page_comments < data.pager.pages) {
				getById('comments').innerHTML += '<li id="next_button_comments"><a href="javascript:displayComments(\'/'+data.pager.last_dateline+'/next/'+data.pager.next_page+'\')">加载更多……</a></li>';
				page_comments = data.pager.page;
			}
			showPage('comments');
		}
	});
}

function selectMenu(id) { //选择了菜单项
	if (id === CMD.refersh) { //点击刷新
		displayList('?_='+new Date().getTime());
	} else if (id === CMD.about) { //点击关于
		showPage('about');
		menu.setRightSoftkeyLabel('返回', function() {
			showPage('list');
		}); //右键返回
		menu.setLeftSoftkeyLabel('隐藏', function() {
			showPage('list');
		});
	} else if (id === CMD.checkVersion) {
		if (!widget.preferenceForKey('auth')) {
			alert('请先登录。');
			return false;
		}
		ajax_get('http://api2.9smart.cn/app/585c784e7e60ff70cc99e7ab?_='+new Date().getTime(), function(error, data) {
			if (error) {
				alert(error);
			} else if (data.app.version !== info.version) {
				//有新版本
				alert('有新版本，版本号：'+data.app.version);
				widget.openURL('http://api2.9smart.cn/clients/9news/s60v3fp2.wgz');
			} else {
				alert('您的版本已经是最新版本。');
			}
		});
	} else if (id === CMD.comment) { //发布评论
		const content = prompt('评论内容：');
		if (content) {
			const so = device.getServiceObject('Service.SysInfo', 'ISysInfo');
			const result = so.ISysInfo.GetInfo({Entity: 'Device', Key: 'PhoneModel'});
			var model = '网页';
			if (result.ErrorCode == 0) {
				model = result.ReturnValue.StringData;
			}
			ajax_post('http://api2.9smart.cn/comments/'+getById('content').className+'?auth='+widget.preferenceForKey('auth'), {
				type: 'news',
				content: content,
				model: model
			}, function(error, data) {
				if (error) {
					alert(error);
				} else {
					alert('评论成功。');
					displayComments('?_='+new Date().getTime());
				}
			});
		}
	} else if (id === CMD.reg) { //选择注册
		showPage('reg_form');
		getByName('reg_email')[0].focus();
		menu.setLeftSoftkeyLabel('提交', function() {
			const email = getByName('reg_email')[0].value,
				  password = getByName('reg_password')[0].value,
				  repassword = getByName('reg_repassword')[0].value,
				  nickname = getByName('reg_nickname')[0].value;
			if (!email || !password || !repassword || !nickname) {
				alert('请填写完整！');
				return false;
			}
			ajax_post('http://api2.9smart.cn/users', {
				email: email,
				password: password,
				repassword: repassword,
				nickname: nickname
			}, function(error, data) {
				if (error) {
					alert(error);
				} else {
					alert('注册成功！');
					widget.setPreferenceForKey(data.auth, 'auth');
					menu.append(menu_logout);
					menu.remove(menu_login);
					menu.remove(menu_reg);
					showPage(ref_page);
				}
			});
		});
		menu.setRightSoftkeyLabel('返回', function() { //右键返回上一页
			showPage(ref_page);
		});
	} else if (id === CMD.login) { //选择登录
		showPage('login_form');
		getByName('login_email')[0].focus();
		menu.setLeftSoftkeyLabel('提交', function() {
			const email = getByName('login_email')[0].value,
				  password = getByName('login_password')[0].value;
			if (!email || !password) {
				alert('请填写用户名和密码。');
				return false;
			}
			ajax_post('http://api2.9smart.cn/user?_='+(new Date().getTime()), {email: email, password: password}, function(error, data) {
				if (error) {
					alert(error);
				} else {
					alert('登录成功！');
					widget.setPreferenceForKey(data.auth, 'auth');
					menu.append(menu_logout);
					menu.remove(menu_login);
					menu.remove(menu_reg);
					showPage(ref_page);
				}
			});
		});
		menu.setRightSoftkeyLabel('返回', function() {
			showPage(ref_page);
		});
	} else if (id === CMD.logout) {
		menu.remove(menu_logout);
		menu.append(menu_reg);
		menu.append(menu_login);
		widget.setPreferenceForKey(null, 'auth');
		alert('注销成功！');
	} else if (id === CMD.comments) { //查看评论页面
		displayComments('?_='+new Date().getTime());
	}
}
window.onload = function() { //应用载入之后开始执行。
	getById('about').innerHTML = '<h3>'+info.appname+'</h3><p>版本：'+info.version+'</p><p>简介：'+info.summary+'</p><p>感谢：'+info.thanks+'</p><p>官方网站：'+info.website+'</p>';
	widget.setNavigationEnabled(false); //设置成按键控制
	menu.append(menu_refersh);
	if (widget.preferenceForKey('auth')) {
		menu.append(menu_logout);
	} else {
		menu.append(menu_reg);
		menu.append(menu_login);
	}
	menu.append(menu_about);
	menu.append(menu_checkVersion);
	
	var timer = setTimeout(function() {
		document.body.removeChild(getById('wellcome')); //关闭欢迎界面
		displayList();
		menu.showSoftkeys();
		clearTimeout(timer);
	}, 0);
};