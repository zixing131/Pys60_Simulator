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
function getById(id) {
	return document.getElementById(id);
}
function getByName(name) {
	return document.getElementsByName(name);
}
function ajax(method, url, data, callback, progress, type) {
	method = method.toUpperCase();
	type = type || 'json';
	const xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4) {
			if (xhr.status === 200) {
				if (type === 'xml') {
					callback(false, xhr.responseXML);
				} else if (type === 'json') {
					try {
						const text = eval('(' + xhr.responseText + ')');
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
		const urlstr = [];
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
	return str;
}

function dateline(datetime) {
	var date = new Date(datetime);
	return date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate();
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