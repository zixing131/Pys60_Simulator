function login(option, onSuccess, onFailed){
    var req = new BaiduRequest(BaiduApi.C_S_LOGIN);
    var isp = option.isphone?1:0;
    var param = {
        token: BaiduApi.TOKEN,
        isphone: isp,
        m_api: "/c/s/sync",
        passwd: toBase64(option.passwd),
        un: option.un
    }
    if (option.vcode){
        param.vcode = option.vcode;
        param.vcode_md5 = option.vcode_md5;
    }
    req.signForm(param);
    var s = function(obj){
        tbs = obj.anti.tbs;
        var user = obj.user;
        tbsettings.currentUid = user.id;
        DBHelper.storeAuthData(user.id, user.name, user.BDUSS, user.passwd, user.portrait);
        __name = user.name;
        __bduss = user.BDUSS;
        __portrait = user.portrait;
        BaiduConst.BDUSS = user.BDUSS;
        signalCenter.clearLocalCache();
        // Required after changing/adding an account
        BaiduRequest.intercomm();
        signalCenter.userChanged();
        onSuccess();
    }
    req.sendRequest(s, onFailed);
}
