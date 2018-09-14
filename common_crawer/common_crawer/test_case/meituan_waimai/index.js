(function (i, s, o, g, r, a, m) {
        i['GoogleAnalyticsObject'] = r;
        i[r] = i[r] || function () {
            (i[r].q = i[r].q || []).push(arguments)
        }
            ,
            i[r].l = 1 * new Date();
        a = s.createElement(o),
            m = s.getElementsByTagName(o)[0];
        a.async = 1;
        a.src = g;
        m.parentNode.insertBefore(a, m)
    }
)(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');
ga('create', 'UA-45741865-1', {
    'cookieDomain': 'waimai.meituan.com'
});
ga('send', 'pageview');

!function (t, e, n) {
    function i() {
        var t = e.createElement("script");
        t.async = !0,
            t.src = "//s0.meituan." + (-1 === e.location.protocol.indexOf("https") ? "net" : "com") + "/bs/js/?f=mta-js:mta.min.js";
        var n = e.getElementsByTagName("script")[0];
        n.parentNode.insertBefore(t, n)
    }

    if (t.MeituanAnalyticsObject = n,
        t[n] = t[n] || function () {
            (t[n].q = t[n].q || []).push(arguments)
        }
        ,
    "complete" === e.readyState)
        i();
    else {
        var s = "addEventListener"
            , r = "attachEvent";
        if (t[s])
            t[s]("load", i, !1);
        else if (t[r])
            t[r]("onload", i);
        else {
            var a = t.onload;
            t.onload = function () {
                i(),
                a && a()
            }
        }
    }
}(window, document, "mta"),
    function (t, e, n) {
        if (e && !("_mta" in e)) {
            e._mta = !0;
            var i = t.location.protocol;
            if ("file:" !== i) {
                var s = t.location.host
                    , r = e.prototype.open;
                e.prototype.open = function (e, n, a, o, h) {
                    if (this._method = "string" == typeof e ? e.toUpperCase() : null,
                        n) {
                        if (0 === n.indexOf("http://") || 0 === n.indexOf("https://") || 0 === n.indexOf("//"))
                            this._url = n;
                        else if (0 === n.indexOf("/"))
                            this._url = i + "//" + s + n;
                        else {
                            var l = i + "//" + s + t.location.pathname;
                            l = l.substring(0, l.lastIndexOf("/") + 1),
                                this._url = l + n
                        }
                        var u = this._url.indexOf("?");
                        -1 !== u ? (this._searchLength = this._url.length - 1 - u,
                            this._url = this._url.substring(0, u)) : this._searchLength = 0
                    } else
                        this._url = null,
                            this._searchLength = 0;
                    return this._startTime = (new Date).getTime(),
                        r.apply(this, arguments)
                }
                ;
                var a = "onreadystatechange"
                    , o = "addEventListener"
                    , h = e.prototype.send;
                e.prototype.send = function (e) {
                    function n(n, s) {
                        0 !== n._url.indexOf(i + "//frep.meituan.net/_.gif") && t.mta("send", "browser.ajax", {
                            url: n._url,
                            method: n._method,
                            error: !(0 === n.status.toString().indexOf("2") || 304 === n.status),
                            responseTime: (new Date).getTime() - n._startTime,
                            requestSize: n._searchLength + (e ? e.length : 0),
                            responseSize: n.responseText.length
                        })
                    }

                    if (o in this) {
                        var s = function (t) {
                            n(this, t)
                        };
                        this[o]("load", s),
                            this[o]("error", s),
                            this[o]("abort", s)
                    } else {
                        var r = this[a];
                        this[a] = function (e) {
                            r && r.apply(this, arguments),
                            4 === this.readyState && t.mta && n(this, e)
                        }
                    }
                    return h.apply(this, arguments)
                }
            }
        }
    }(window, window.XMLHttpRequest, "mta");
mta("create", "551517ddd0a88b586dc89658");
mta("send", "page");
