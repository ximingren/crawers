"use strict";
!function (e) {
    function c(e, c) {
        // g
        310 === e.type ? (t(c.urlSlideCss), n(c.urlSlideJs, function () {
            new CaptchaSlide(e).bootstrap()
        })) : (t(c.urlClickCss), n(c.urlClickJs, function () {
            new CaptchaClick(e).bootstrap()
        })), navigator.userAgent.indexOf("MSIE") >= 0 && navigator.userAgent.indexOf("Opera") < 0 && t(c.urlCaptchaIECss)
    }

    function t(c) {
        for (var t = !1, n = document.getElementsByTagName("link"), r = 0; r < n.length; r++) n[r].href === e.location.protocol + c && (t = !0);
        if (!t) {
            var a = document.createElement("link");
            a.rel = "stylesheet", a.type = "text/css", a.href = c;
            var s = document.getElementsByTagName("script")[0];
            s.parentNode.insertBefore(a, s)
        }
    }

    function n(c, t) {
        for (var n = !1, r = null, a = document.getElementsByTagName("script"), s = 0; s < a.length; s++) a[s].src === e.location.protocol + c && (r = a[s], n = !0);
        var o = document.createElement("script");
        o.src = c;
        var l = document.getElementsByTagName("script"), i = l[l.length - 1];
        i.parentNode.insertBefore(o, i), o.onload = o.onreadystatechange = function () {
            o.readyState && !/complete|loaded/.test(o.readyState) || (t(),
                o.onload = null, o.onreadystatechange = null)
        }, n && i.parentNode.removeChild(r)
    }

    var r = function (t) {
        return new function () {
            var r = {
                scriptCount: 0,
                urlClickJs: "//j1.58cdn.com.cn/resource/xxzl/captcha/js/click.js?v=20180711171605",
                urlClickCss: "//c.58cdn.com.cn/resource/xxzl/captcha/css/click.css?v=105",
                urlSlideJs: "//j1.58cdn.com.cn/resource/xxzl/captcha/js/slide.js?v=20180726165831",
                urlSlideCss: "//sc.58cdn.com.cn/resource/xxzl/captcha/css/slide.css?v=105",
                urlCaptchaIECss: "//c.58cdn.com.cn/resource/xxzl/captcha/css/dvc_captcha_for_ie.css?v=99",
                urlJquery: "//j1.58cdn.com.cn/resource/xxzl/captcha/js/captcha.jquery.min.1.9.1.js?v=33"
            };
            this.init = function () {
                e.jQuery ? c(t, r) : n(r.urlJquery, function () {
                    c(t, r)
                })
            }
        }
    };
    e.ISDCaptcha = e.ISDCaptcha = r
}(window);