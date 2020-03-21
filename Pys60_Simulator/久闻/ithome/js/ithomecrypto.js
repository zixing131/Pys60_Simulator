 
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
