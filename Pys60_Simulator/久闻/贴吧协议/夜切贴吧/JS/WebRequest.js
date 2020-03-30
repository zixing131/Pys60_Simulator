var xmlhttp = new XMLHttpRequest()

xmlhttp.onreadystatechange = function(){
            switch (xmlhttp.readyState)
            {
            case xmlhttp.OPENED: loadStart(); break;
            case xmlhttp.HEADERS_RECEIVED:
                if (xmlhttp.status!=200 && xmlhttp.status!=201)
                    app.showMessage("网络连接错误！代码:"+xmlhttp.status+"  "+xmlhttp.statusText)
                break;
            case xmlhttp.LOADING: break;
            case xmlhttp.DONE: {
                if (xmlhttp.status ==200 || xmlhttp.status == 201 ) {
                    try {
                        xmlhttp.callback(xmlhttp.responseText.replace(/id\":(\d+)/g,'id":"$1"'),
                                         xmlhttp.param)
                    }
                    catch (e){
                        console.log(JSON.stringify(e))
                    }
                }
                loadStop()
                break;
            }
            }
        }

function sendWebRequest(method, url, callback, postText, param){
    abortRequest()
    xmlhttp.callback = callback
    xmlhttp.param = param

    xmlhttp.open(method, url, true)
    if (method=="POST"){
        xmlhttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded")
        xmlhttp.setRequestHeader("Content-Length",postText.length)
        xmlhttp.send(postText.replace(/\+/g,"%2B"))
    } else {
        xmlhttp.send()
    }
}

function abortRequest(){
    if (xmlhttp.readyState != xmlhttp.UNSENT && xmlhttp.readyState != xmlhttp.DONE)
        xmlhttp.abort()
}
