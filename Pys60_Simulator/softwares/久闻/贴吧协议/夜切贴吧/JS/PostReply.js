//回贴
function getReplyResult(content, forumId, forumName, tbs, threadId, floorNum, quoteId, callback, vcode, vcodeMd5){
    var obj = {
        BDUSS: app.currentBDUSS, _client_type: settings.clientType, _client_version: settings.clientVersion,
        _phone_imei: settings.imei, anonymous: 0, content: content, fid: forumId,
        floor_num: floorNum||0, from: settings.from, kw: forumName, net_type: settings.netType,
        quote_id: quoteId||0, tbs: tbs, tid: threadId
    }
    if (vcode){
        obj.vcode = vcode
        obj.vcode_md5 = vcodeMd5
    }
    Web.sendWebRequest("POST", settings.host+"/c/c/post/add", callback, app.getScript().stringify(obj))
}
