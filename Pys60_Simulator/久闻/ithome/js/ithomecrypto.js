
 
//DES加密
function encryptByDES(message, key){
    var keyHex = CryptoJS.enc.Utf8.parse(key);
    var encrypted = CryptoJS.DES.encrypt(message, keyHex, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.NoPadding
    });
    return encrypted.ciphertext.toString();
}
//DES加密
function decryptByDES(ciphertext, key){
    var keyHex = CryptoJS.enc.Utf8.parse(key);
    var decrypted = CryptoJS.DES.decrypt({
        ciphertext: CryptoJS.enc.Hex.parse(ciphertext)
    }, keyHex, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    });
    var result_value = decrypted.toString(CryptoJS.enc.Utf8);
    return result_value;
}


function getCommentSn(newsid)
{
	return m49921c(newsid.toString());
}

 function PrefixInteger(num, n) {
		return (Array(n).join(0) + num).slice(-n);
	}
		
function getHeadUrl(Ui)
{
	var url1 = 'http://avatar.ithome.com/avatars/';
	var url2='_60.jpg'; 
	var ret = '';
	Ui = PrefixInteger(Ui,9); 
	ret = Ui[0]+Ui[1]+Ui[2]+'/'+Ui[3]+Ui[4]+'/'+Ui[5]+Ui[6]+'/'+Ui[7]+Ui[8];	
	//alert(url1+ret+url2);
	return url1+ret+url2;
}

function m49921c(str)
{
    var bArr2 = '(#i@x*l%'; 
	return m49912a(str,bArr2);
}

function m49912a(str,str2)
{
	return m49914a(str,str2,false);
}

function m49914a(str,str2,z)
{
	length = str.length;
	if (length < 8) {
		i = 8 - length;
	} else {
		var i2 = length % 8;
		i = i2 != 0 ? 8 - i2 : 0;
	}
	
	var str3 = str;
	for (var i3 = 0; i3 < i; i3++) {
		str3 = str3 + "\u0000";
	}
	return encryptByDES(str3,str2);
}

function m49914a2(str,str2,z)
{
	length = str.length;
	if (length < 8) {
		i = 8 - length;
	} else {
		var i2 = length % 8;
		i = i2 != 0 ? 8 - i2 : 0;
	}
	
	var str3 = str;
	for (var i3 = 0; i3 < i; i3++) {
		str3 = str3 + "\u0000";
	}
	return encryptByDES2(str3,str2);
}
 

function encryptByDES2(message, key) {
    var keyHex = CryptoJS.enc.Utf8.parse(key);
    var encrypted = CryptoJS.DES.encrypt(message, keyHex, {
        iv: keyHex,
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.NoPadding
    });   
    return encrypted.toString();
}

function get_next(time_str) {
    if(time_str.indexOf('.')>=0)
	{
		time_str = time_str.split('.')[0];
	}
	time_str = time_str.replace(/-/g,'/');
	time_str = time_str.replace('T',' ');  
	//console.log(time_str);
	
	var timestamp = Date.parse(time_str); 
	var bArr2 = 'w^s(1#a@'; 
    var encryptd = m49914a2(timestamp.toString(),bArr2);
	var hash = fmtBytes(str2UTF8(hexCharCodeToStr(CryptoJS.enc.Base64.parse(encryptd).toString())));
	// console.log(hash);
    return hash;
}

function hexCharCodeToStr(hex) { 
    var arr = hex.split("");
    var out = "";
    for (var i = 0; i < arr.length / 2; i++) {
      var tmp = "0x" + arr[i * 2] + arr[i * 2 + 1];
      var charValue = String.fromCharCode(tmp);
      out += charValue;
    }
    return out;
}

function fmtBytes(arg5) {
    var v1 = "";
    for (var v0 = 0; v0 < arg5.length; ++v0) {
        var v2 = (arg5[v0] & 255).toString(16);
        if (v2.length == 1) {
            v1 = v1 + "0" + v2;
        } else {
            v1 = v1 + v2;
        }
    }
    return v1;
}

function str2UTF8(str){
    var bytes = new Array(); 
    var len,c; 
    len = 16;
    for(var i = 0; i < len; i++){
        c = str.charCodeAt(i);
        var s = parseInt(c).toString(2); 
        bytes.push(c & 0xFF);
    }
    return bytes;
}

