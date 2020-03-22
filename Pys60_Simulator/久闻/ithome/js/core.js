 
Array.prototype.myforEach = function myforEach(val,i){
	  for(var i=0;i<this.length;i++){
		  val.call(window,this[i],i,this);
	  }
  };

function setLeftSoftkeyLabel(v,k)
{
	if(typeof menu.setLeftSoftkeyLabel != "function"){
		   
	}
	else{
		menu.setLeftSoftkeyLabel(v,k);
	}
}
function bind(target, type, callback) {
	if (target.length && target.tagName !== 'FORM') {
		for(var i = 0, len = target.length; i < len; i ++) {
			target[i].addEventListener(type, function (event) {
				if (!callback(event)) {
					event.preventDefault();
				}
			}, false);
		}
	} else {
		target.addEventListener(type, function (event) {
			if (!callback(event)) {
				event.preventDefault();
			}
		}, false);
	}
}
 
 
function PrefixInteger(num, n) {
	return (Array(n).join(0) + num).slice(-n);
}

function getViewPortWidth() {
    return document.documentElement.clientWidth || document.body.clientWidth;
}

function getViewPortHeight() {
    return document.documentElement.clientHeight || document.body.clientHeight;
}

function getById(id) {
	return document.getElementById(id);
}
function getByName(name) {
	return document.getElementsByName(name);
}
function ajax(method, url, data, callback, progress, type) {
	method = method.toUpperCase();
	type = type || 'json';
	var xhr = new XMLHttpRequest(); 
	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4) {
			if (xhr.status === 200) {
				if (type === 'xml') {
					callback(false, xhr.responseXML);
				} else if (type === 'json') {
					try {
						var text = eval('(' + xhr.responseText + ')');
						if (text.error) {
							callback(text.error);
						} else {
							callback(false, text);
						}
					} catch(e) {
						callback(e.message);
					}
				} else {
					callback(false, xhr.responseText);
				}
			} else {
				callback(xhr.status + xhr.responseText);
			}
		}
	};
	if (data) {
		var urlstr = [];
		for(var i in data) {
			urlstr.push(i + '=' + encodeURIComponent(data[i]));
		}

		data = urlstr.join('&');
		if ((method === 'GET' || method === 'DELETE') && data) {
			url += /\?/.test(url) ? '&' + data : '?' + data; 
		}
	}
	xhr.open(method, url, true);
	if (method === 'POST') {
		xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	}
	xhr.send(data);
}
function ajax_delete(url, callback) {
	ajax('DELETE', url, {}, callback, null, 'json');
}
function ajax_get(url, callback, type) {
	ajax('GET', url, {}, callback, null, type);
}
function ajax_post(url, data, callback, progress) {
	ajax('POST', url, data, callback, progress, 'json');
}
function ajax_put(url, data, callback) {
	ajax('PUT', url, data, callback, null, 'json');
}

function UBB(str) { 
	str = str.replace(/\[flash=(\d{2,3}),(\d{2,3})\](.+?)\[\/flash\]/mg,'<embed src="$3" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" wmode="opaque" width="$1" height="$2"></embed>');
	str = str.replace(/\[img\](.+?)\[\/img\]/mg,'<img src="$1" alt="图片" />');
	str = str.replace(/\[img=(.+)\](.+?)\[\/img\]/mg,'<figure><img src="$2" alt="图片" /><figcaption>$1</figcaption></figure>');
	str = str.replace(/\[p\]((.|\n)+?)\[\/p\]/mg,'<p>$1</p>');
	str = str.replace(/\[h2\](.+?)\[\/h2\]/mg,'<h2>$1</h2>');
	str = str.replace(/\[center\](.+?)\[\/center\]/mg,'<span class="UBB_center">$1</span>');
	str = str.replace(/\[b\](.+?)\[\/b\]/mg,'<strong>$1</strong>');
	str = str.replace(/\[a=(.+?)\](.+?)\[\/a\]/mg,'<a href="$2">$1</a>');
	str = str.replace(/\[a\](.+?)\[\/a\]/mg,'<a href="$1">$1</a>');
	str = str.replace(/\[download=(.+)\](.+?)\[\/download\]/mg,'<a href="/download?url=$2">$1</a>');
	str = str.replace(/https/mg,'http');
	return str;
}
 
function dateline(datetime) {
	return datetime.split('.')[0].replace('T',' ');
}

function humanedate(datetime) {
	datetime = datetime.split('.')[0];
	datetime = datetime.replace(/-/g,'/');
	datetime = datetime.replace('T',' ');  
	var nowtime = new Date();
	var timestamp = new Date(datetime);
	var cha = (nowtime - timestamp)/1000
	 if(cha<180){
        return "刚刚";
    }else if(cha<3600){
        return Math.floor(cha/60)+" 分钟前";
    }else if(cha<86400){
        return Math.floor(cha/3600)+" 小时前";
    }else if(cha<172800){
        return "昨天 "+PrefixInteger(timestamp.getHours(),2)+':'+PrefixInteger(timestamp.getMinutes(),2);
    }else if(cha<259200){
        return "前天 "+PrefixInteger(timestamp.getHours(),2)+':'+PrefixInteger(timestamp.getMinutes(),2);
    }else if(cha<345600){
        return Math.floor(cha/86400)+" 天前";
    }else{
        return timestamp.getFullYear()+'-'+(timestamp.getMonth()+1)+'-'+timestamp.getDate();
    }
}


function myalert(type, str) {
	var alert_div = getById('alert_div');
	if (!alert_div) {
		alert_div = document.createElement('div');
		alert_div.id = 'alert_div';
	}
	alert_div.textContent = str;
	alert_div.style.display = 'block';
	alert_div.className = type;
	var timer = setTimeout(function(){
		alert_div.style.display = 'none';
		timer = null;
	}, 2000);
}

