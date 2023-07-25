const CryptoJS = require("crypto-js");

// 视频的pid(可从视频的网页播放页面获取，自己访问正则获取，就不写了)
// https://www.bdys10.com/guoju/play/23862-0.htm
let pid = "168767";

// 地址模板的参数t
let t = new Date().getTime();

// 地址模板的参数sg
let sg = base64ToHex(
    CryptoJS.AES.encrypt(
        pid + "-" + t,

        CryptoJS.enc.Utf8.parse(
            CryptoJS.MD5(pid + "-" + t)
                .toString()
                .substring(0, 16)
        ),

        { mode: CryptoJS.mode.ECB, padding: CryptoJS.pad.Pkcs7 }
    ) + ""
);

// base64转hex函数
function base64ToHex(base64) {
    var raw = atob(base64);

    var HEX = "";

    for (let i = 0; i < raw.length; i++) {
        var _hex = raw.charCodeAt(i).toString(16);

        HEX += _hex.length == 2 ? _hex : "0" + _hex;
    }
    return HEX.toUpperCase();
}


// 获取视频信息的地址模板
let playUrl = `https://www.bdys10.com/lines?t=${t}&sg=${sg}&pid=${pid}`;

// 打印结果(丢到浏览器测试，注意时效性)
console.log(`BDYS解密信息获取: ${playUrl}`);
