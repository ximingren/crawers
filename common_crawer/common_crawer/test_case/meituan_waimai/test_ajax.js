new_element=document.createElement("script");
　　new_element.setAttribute("type","text/javascript");
　　new_element.setAttribute("src","http://libs.baidu.com/jquery/1.9.0/jquery.js");// 在这里引入了a.js
new_element=document.createElement("script");
　　new_element.setAttribute("type","text/javascript");
　　new_element.setAttribute("src","http://s0.meituan.net/mx/rohr/rohr.min.js");// 在这里引入了a.js
var PARAM = {
    'classify_type': 'cate_all',
    'sort_type': 0,
    'price_type': 0,
    'support_online_pay': 0,
    'support_invoice': 0,
    'support_logistic': 0,
    'page_offset': 21,
    'page_size': 20,
    'mtsi_font_css_version': 'dd53a913',
    'uuid': 'zDzgfvpaDrj6ywDDwhFlvYM11eVH2hZxSNYgUkmFcRy6yKCxCoU1Eb3rovTrGfXJ',
    'platform': 1,
    'partner': 4,
    'originUrl': 'http%3A%2F%2Fwaimai.meituan.com%2Fhome%2Fws0dvfv4hm53'
};


// var CLASSIFY = ['cate_all'];
// PARAM.classify_type = CLASSIFY.join('|');

// PARAM.platform = 1;
// PARAM.partner = 4;
// PARAM.originUrl = encodeURIComponent(window.location.href);

var toCaledParams = '', index = 0;
for (var i in PARAM) {
    toCaledParams += ((index == 0) ? '' : '&') + i + '=' + PARAM[i];
    index++;
}

