function postSign(str){
    return Qt.md5(str.replace(/&/g, "")+"tiebaclient!!!").toUpperCase()
}

function stringify(obj){
    var res = ""
    for (var i in obj)
        res += "&"+i+"="+obj[i]
    res += "&sign="+postSign(res)
    return res.replace("&","")
}

function decodeThreadContent(obj){
    var res = ""
    for (var i in obj){
        switch(obj[i].type){
        case 0: res += (obj[i].text || "").replace(/\n/g,"<br/>"); break;
        case 1: res += "<a href=\"link:%1\">%2</a>".arg(obj[i].link).arg(obj[i].text); break
        case 2:
            var _txt = obj[i].text.toLowerCase().replace(/i_f/,"write_face_")
            res += "<img src=\"qrc:/pics/" + _txt + (/(b|t|w)_/.test(_txt)?".gif\"/>":".png\"/>")
            break
        case 3:
            if (settings.showImage)
                res += "<a href=\"img:%1\" ><img src=\"%1\"/></a>".arg(obj[i].src)
            else
                res += "<a href=\"%1\" >点击链接查看图片</a>".arg(obj[i].src)
            break;
        case 4: res += "<a href=\"at:%1\">%2</a>".arg(obj[i].uid).arg(obj[i].text); break
        case 5: res += "<a href=\"video:%1\" >点击链接查看视频</a>".arg(obj[i].text); break
        }
    }
    return res
}
function decodeThreadContentList(obj){
    var res = []
    var len = -1
    for (var i in obj){
        var o = obj[i]
        if (settings.showImage && o.type == 3){
            res.push([false,o.src])
            len ++
        } else {
            if (!res[len] || !res[len][0]){
                res.push([true,"",false])
                len ++
            }
            if (o.type!=0 && !res[len][2])
                res[len][2] = true
            switch(o.type){
            case 0:
                res[len][1] += o.text || ""
                break
            case 1:
                res[len][1] += "<a href=\"link:%1\">%2</a>".arg(o.link).arg(o.text);
                break
            case 2:
                var _txt = o.text.toLowerCase().replace(/i_f/,"write_face_")
                res[len][1] += "<img src=\"qrc:/pics/" + _txt + (/(b|t|w)_/.test(_txt)?".gif\"/>":".png\"/>")
                break;
            case 3:
                res[len][1] += "<a href=\"img:%1\" >点击链接查看图片</a><br/>".arg(o.src)
                break;
            case 4:
                res[len][1] += "<a href=\"at:%1\">%2</a>".arg(o.uid).arg(o.text);
                break
            case 5:
                res[len][1] += "<a href=\"video:%1\" >点击链接查看视频</a>".arg(o.text);
                break
            }
        }
    }
    return res
}

//由时间毫秒数返回日期
function formatDate(milisec){
    var mydate = new Date(milisec)
    if (mydate.toDateString()==new Date().toDateString())
        return Qt.formatTime(mydate, "hh:mm:ss")
    else
        return Qt.formatDate(mydate, "yyyy-MM-dd")
}

//获取用户头像
function getAvatar(portraitId){
    return "http://tb.himg.baidu.com/sys/portraitn/item/"+portraitId
}

//在数字左边补零，number为原数字，length为返回的总长度
function paddingLeft(number, length){
    var n = ""
    for (var i=0;i<length;i++)
        n += "0"
    return String(Number(1+n)+number).slice(1)
}

//获取文件名后缀
function getFileSuffix(url){
    return url.split("\.").pop()
}
//解析链接
function linkActivated(link){
    var t = link.split(":")[0]
    switch (t){
    case "at": var u = link.split(":")[1]; if(u!="0")app.enterProfilePage(u); break;
    case "link": loadLink(link.slice(link.indexOf(":")+1)); break
    case "img": loadImage(link.slice(link.indexOf(":")+1)); break
    case "video": loadVideo(link.slice(link.indexOf(":")+1)); break;
    }
}
//解析并打开视频
function loadVideo(url){
    console.log(url)
    var youku = url.match(/youku.*\/sid\/(.+)\//)
    if (youku) {
        getYoukuSource(youku[1], "3gphd")
        return;
    }
    var video56 = url.match(/56\.com\/v_(.+)\.swf/)
    if (video56) {
        getVideoSource("http://vxml.56.com/json/%1/?src=out".arg(video56[1])
                       ,function(resp){
                           var fs = JSON.parse(resp).info.rfiles
                           for (var i in fs){
                               if (getFileSuffix(fs[i].url) == "mp4"){
                                   appLauncher.launchPlayer(fs[i].url)
                                   return
                               }
                           }
                           if (fs)
                               appLauncher.openURLDefault(url)
                       })
        return
    }
    var yinyuetai = url.match(/yinyuetai.*\/player\/(.+)\//)
    if (yinyuetai){
        getVideoSource("http://www.yinyuetai.com/explayer/get-video-info?videoId="+yinyuetai[1]+"&flex=true&platform=null"
                       ,function(resp){
                           var src = resp.match(/http:\/\/[^:]*\.(flv|mp4|f4v|hlv)\?t=[a-z0-9]*/g)
                           if (src){
                               appLauncher.openURLDefault(src[0])
                           } else {
                               appLauncher.openURLDefault(url)
                           }
                       })
        return
    }
    /*
    var qq = url.match(/video\.qq.*vid=([0-9a-zA-Z]*)/)
    if (qq){
        //vhot2.qqvideo.tc.qq.com/D0010uNAcdP.mp4
        //http://static.video.qq.com/TPout.swf?vid=D0010uNAcdP&auto=1
        return
    }
    */
    var sina = url.match(/video\.sina\..*vid=(\d+)_\d+/)
    if (sina){
        getVideoSource("http://video.sina.com.cn/interface/video_ids/video_ids.php?v="+sina[1]
                       ,function(resp){
                           var ipid = JSON.parse(resp).ipad_vid
                           if (ipid != 0)
                               appLauncher.launchPlayer("http://v.iask.com/v_play_ipad.php?vid="+ipid)
                           else
                               appLauncher.openURLDefault(url)
                       })
        return
    }

    appLauncher.openURLDefault(url)
}
function getVideoSource(url, callback){
    app.showMessage("正在解析视频源...")
    var doc = new XMLHttpRequest()
    doc.onreadystatechange = function(){
                switch (doc.readyState){
                case doc.HEADERS_RECEIVED: if (doc.status!=200) app.showMessage("无法打开视频...> <"); break;
                case doc.DONE: {
                    if (doc.status == 200){
                        try {
                            callback(doc.responseText)
                        } catch (e){
                            app.showMessage("无法打开视频...> <")
                        }
                    }
                    break;
                }
                }
            }
    doc.open("GET", url)
    doc.send()
}

function getYoukuSource(sid, type){
    app.showMessage("正在解析视频源...")
    var doc = new XMLHttpRequest()
    doc.onreadystatechange = function(){
                if (doc.readyState == doc.HEADERS_RECEIVED) {
                    if (doc.status != 200)
                        app.showMessage("无法打开视频...> <")
                }
                if (doc.readyState == doc.LOADING){
                    if (doc.status == 200){
                        if (!/text/.test(doc.getResponseHeader("content-type"))){
                            doc.abort()
                            appLauncher.launchPlayer("http://m.youku.com/pvs?id="+sid+"&format="+type)
                        }
                    }
                }
                if (doc.readyState == doc.DONE){
                    if (doc.status == 200){
                        if (type == "3gphd")
                            getYoukuSource(sid, "3gp")
                        else
                            app.showMessage(doc.responseText)
                    }
                }
            }
    doc.open("GET", "http://m.youku.com/pvs?id="+sid+"&format="+type)
    doc.send()
}
//解析并打开图片
function loadImage(url){
    if (settings.openWithSystem){
        manager.abortDownload()
        var saveFile = settings.imagePath+"/"+Qt.md5(url)+"."+getFileSuffix(url)
        if (manager.existsFile(saveFile))
            appLauncher.openFileDefault("file:///"+saveFile)
        else {
            Qt.createComponent("Component/ImageShower.qml").createObject(app)
            manager.appendDownload(url, saveFile)
        }
    } else
        app.pageStack.push(Qt.resolvedUrl("ImagePage.qml"),{ imgUrl: url })
}

//解析并打开链接
function loadLink(url){
    var m = url.match(/tieba.baidu.com\/(p\/|f\?.*z=)(\d+)/)
    if (m) return app.enterThread(m[2])

    var n = url.match(/tieba.baidu.com\/f\?.*kw=(.+?)[&#]/)
    if (n) return app.enterForum(decodeForumName(n[1]))

    var o = url.match(/tieba.baidu.com\/f\?.*kw=(.+)/)
    if (o) return app.enterForum(decodeForumName(o[1]))

    appLauncher.openURLDefault(url)
}
//解析吧名
function decodeForumName(oristring){
    var i = 0, res = ""
    while (i<oristring.length){
        if ( oristring.charAt(i)!="%" || i+2>oristring.length ){
            res += oristring.charCodeAt(i).toString(16)
            i ++
        } else {
            res += oristring.charAt(i+1) + oristring.charAt(i+2)
            i += 3
        }
    }
    return appLauncher.decodeGBKHex(res)
}
