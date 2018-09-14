"use strict";
!function (t, i) {
    var a = function (a) {
        if (!a) return !1;
        if (!a.element || !a.type) return !1;
        var r = i("#" + a.element);
        return r.length < 1 && (i(document.body).append('<div id="' + a.element + '"></div>'), r = i("#" + a.element)), r || alert("未匹配到验证码页面元素"), new function ()
        {
            t.xxzlfingertoken = "", t.isOK = function (e) {
                "success" === e.status && (t.xxzlfingertoken = e.token)
            };
            var n = document.createElement("script");
            n.src = "//j1.58cdn.com.cn/resource/xxzl/tracker/xzdfp.js?from=weba_captcha&clientType=1&callback=isOK", document.body.appendChild(n);
            var s = this, c = {
                width: parseInt(a.width),
                height: Math.ceil(9 * parseInt(a.width) / 16) + 55,
                placeHolderHeight: Math.ceil(9 * parseInt(a.width) / 16),
                handlerWidth: Math.ceil(96 * a.width / 480),
                type: a.type,
                showType: a.showType,
                sessionId: a.sessionId,
                winAutoShow: a.winAutoShow,
                responseId: "",
                sourceImgUrl: "",
                mouseTrack: [],
                startTimeStamp: "",
                urlCaptcha: "//verifycode.58.com",
                pathGetCaptcha: "/captcha/getV3",
                pathVerfiyCaptcha: "/captcha/checkV3",
                pj: []
            }, o = {
                canDrag: !1,
                canTrack: !1,
                isTrigger: !1,
                isTriggerShow: !1,
                isCaptchaShow: !1,
                isWinShow: !1,
                isVerifyed: !1,
                isUpgrade: !1,
                isIE: navigator.userAgent.indexOf("MSIE") >= 0 && navigator.userAgent.indexOf("Opera") < 0
            }, l = {}, d = null, p = null, h = null, f = {
                passTxt: "验证通过",
                rejectTxt: "验证失败",
                tips: "向右滑动滑块填充拼图",
                winDisappearTime: 1e3,
                triggerDisappearTime: 1e3,
                winCloseTime: 300,
                errShowTime: 600
            }, v = {
                loading: '<svg class="dvc-icon__loading" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="25%" height="25%" viewBox="0 0 40 40" xml:space="preserve"><path opacity="0.2" d="M20.201,5.169c-8.254,0-14.946,6.692-14.946,14.946c0,8.255,6.692,14.946,14.946,14.946s14.946-6.691,14.946-14.946C35.146,11.861,28.455,5.169,20.201,5.169z M20.201,31.749c-6.425,0-11.634-5.208-11.634-11.634c0-6.425,5.209-11.634,11.634-11.634c6.425,0,11.633,5.209,11.633,11.634C31.834,26.541,26.626,31.749,20.201,31.749z"/><path d="M26.013,10.047l1.654-2.866c-2.198-1.272-4.743-2.012-7.466-2.012h0v3.312h0C22.32,8.481,24.301,9.057,26.013,10.047z"><animateTransform attributeType="xml" attributeName="transform" type="rotate" from="0 20 20" to="360 20 20" dur=".625s" repeatCount="indefinite"/></path></svg>',
                arrow: '<svg class="dvc-icon__arrow" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="64px" height="64px" viewBox="0 0 64 64" enable-background="new 0 0 64 64" xml:space="preserve"><path d="M42.174,9.407c-0.394-0.393-0.907-0.59-1.422-0.59s-1.029,0.197-1.422,0.59c-0.785,0.785-0.785,2.058,0,2.843l17.805,17.806H2.354c-1.111,0-2.011,0.9-2.011,2.01c0,1.111,0.899,2.012,2.011,2.012h54.781L39.33,51.884c-0.785,0.785-0.785,2.058,0,2.844c0.785,0.785,2.058,0.785,2.844,0l21.237-21.24c0.785-0.785,0.785-2.058,0-2.843L42.174,9.407z"/></svg>',
                refresh: '<svg version="1.1" class="dvc-icon__refresh" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 496.156 496.156" xml:space="preserve"><path style="fill:#FFFFFF;" d="M428.243,172.149c-10.348,0.023-20.694,0.054-31.042,0.077c-23.272-52.177-68.95-89.871-126.649-98.91c-64.287-10.071-125.816,19.788-162.504,72.312c-16.296,23.326,22.003,45.165,38.16,22.034c50.317-72.037,157.757-65.527,201.907,4.686c-9.559,0.022-19.118,0.046-28.678,0.068c-2.674,0.008-4.574,1.197-5.749,2.877c-1.92,2.058-2.65,5.072-0.639,8.186c18.204,28.25,36.408,56.499,54.616,84.745c3.061,4.747,9.663,4.708,12.696-0.046c18.062-28.338,36.126-56.675,54.188-85.013C437.538,178.48,433.602,172.135,428.243,172.149z"/><path style="fill:#FFFFFF;" d="M350.353,327.224c-49.927,71.49-156.108,65.63-200.886-3.049c9.161-0.022,18.322-0.046,27.484-0.068c2.666-0.008,4.563-1.19,5.741-2.865c1.924-2.059,2.658-5.072,0.646-8.197c-18.2-28.246-36.405-56.499-54.609-84.741c-3.056-4.751-9.662-4.712-12.695,0.046c-18.063,28.334-36.13,56.671-54.196,85.009c-2.987,4.689,0.948,11.032,6.308,11.017c10.669-0.027,21.337-0.054,32.006-0.08c23.498,51.319,68.777,88.332,125.865,97.275c64.287,10.072,125.816-19.784,162.496-72.312C404.806,325.928,366.508,304.09,350.353,327.224z"/></svg>',
                info: '<svg version="1.1" class="dvc-icon__followInfo" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 426.667 426.667" xml:space="preserve"><path style="fill:#FAC917;" d="M213.338,0C95.509,0,0,95.497,0,213.325c0,117.854,95.509,213.342,213.338,213.342c117.82,0,213.329-95.488,213.329-213.342C426.667,95.497,331.157,0,213.338,0z M213.333,99.49c14.793,0,26.786,11.994,26.786,26.786s-11.998,26.782-26.786,26.782s-26.786-11.994-26.786-26.782C186.547,111.484,198.541,99.49,213.333,99.49z M260.207,327.181H166.46v-40.183h20.087v-80.358H166.46V166.46h73.664v40.179v80.358h20.087v40.183H260.207z"/><polygon style="fill:#FAC917;" points="325.935,394.449 419.55,419.529 394.466,325.918 "/></svg>',
                pass: '<svg class="dvc-icon__pass" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="64px" height="64px" viewBox="0 0 64 64" xml:space="preserve"><path d="M16.074,55.049c0.369,0.534,0.975,0.838,1.615,0.838c0.133,0,0.269-0.049,0.404-0.076c0.098,0.016,0.193,0.064,0.292,0.064c0.575,0,1.134-0.249,1.526-0.681l43.514-43.521c0.785-0.784,0.785-2.056,0-2.841c-0.784-0.784-2.056-0.784-2.84,0l-42.52,42.526L3.725,37.021c-0.784-0.785-2.056-0.785-2.84,0c-0.785,0.784-0.785,2.056,0,2.841L16.074,55.049z"/></svg>',
                followPass: '<svg version="1.1" class="dvc-icon__followPass" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 426.667 426.667" xml:space="preserve"><path style="fill:#6AC259;" d="M213.333,0C95.518,0,0,95.514,0,213.333s95.518,213.333,213.333,213.333c117.828,0,213.333-95.514,213.333-213.333S331.157,0,213.333,0z M174.199,322.918l-93.935-93.931l31.309-31.309l62.626,62.622l140.894-140.898l31.309,31.309L174.199,322.918z"/></svg>',
                reject: '<svg class="dvc-icon__reject" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="64px" height="64px" viewBox="0 0 64 64" xml:space="preserve"><path d="M28.941,31.786L0.613,60.114c-0.787,0.787-0.787,2.062,0,2.849c0.393,0.394,0.909,0.59,1.424,0.59 c0.516,0,1.031-0.196,1.424-0.59l28.541-28.541l28.541,28.541c0.394,0.394,0.909,0.59,1.424,0.59c0.515,0,1.031-0.196,1.424-0.59 c0.787-0.787,0.787-2.062,0-2.849L35.064,31.786L63.41,3.438c0.787-0.787,0.787-2.062,0-2.849c-0.787-0.786-2.062-0.786-2.848,0 L32.003,29.15L3.441,0.59c-0.787-0.786-2.061-0.786-2.848,0c-0.787,0.787-0.787,2.062,0,2.849L28.941,31.786z"/></svg>',
                followReject: '<svg version="1.1" class="dvc-icon__followReject" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 426.667 426.667" xml:space="preserve"><path style="fill:#F05228;" d="M213.333,0C95.514,0,0,95.514,0,213.333s95.514,213.333,213.333,213.333s213.333-95.514,213.333-213.333S331.153,0,213.333,0z M330.995,276.689l-54.302,54.306l-63.36-63.356l-63.36,63.36l-54.302-54.31l63.356-63.356l-63.356-63.36l54.302-54.302l63.36,63.356l63.36-63.356l54.302,54.302l-63.356,63.36L330.995,276.689z"/></svg>',
                shield: '<svg class="dvc-icon__normalShield"  width="290px" height="348px" viewBox="0 0 290 348" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><path d="M288.309,54.367 C228.933,54.367 183.445,37.403 144.98,0 C106.519,37.403 61.033,54.367 1.662,54.367 C1.662,151.772 -18.493,291.304 144.979,347.971 C308.463,291.305 288.309,151.773 288.309,54.367 Z"></path></svg>',
                close: '<svg class="dvc-icon__captchaClose" version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 21.9 21.9" xmlns:xlink="http://www.w3.org/1999/xlink"><path d="M14.1,11.3c-0.2-0.2-0.2-0.5,0-0.7l7.5-7.5c0.2-0.2,0.3-0.5,0.3-0.7s-0.1-0.5-0.3-0.7l-1.4-1.4C20,0.1,19.7,0,19.5,0  c-0.3,0-0.5,0.1-0.7,0.3l-7.5,7.5c-0.2,0.2-0.5,0.2-0.7,0L3.1,0.3C2.9,0.1,2.6,0,2.4,0S1.9,0.1,1.7,0.3L0.3,1.7C0.1,1.9,0,2.2,0,2.4  s0.1,0.5,0.3,0.7l7.5,7.5c0.2,0.2,0.2,0.5,0,0.7l-7.5,7.5C0.1,19,0,19.3,0,19.5s0.1,0.5,0.3,0.7l1.4,1.4c0.2,0.2,0.5,0.3,0.7,0.3  s0.5-0.1,0.7-0.3l7.5-7.5c0.2-0.2,0.5-0.2,0.7,0l7.5,7.5c0.2,0.2,0.5,0.3,0.7,0.3s0.5-0.1,0.7-0.3l1.4-1.4c0.2-0.2,0.3-0.5,0.3-0.7  s-0.1-0.5-0.3-0.7L14.1,11.3z"/></svg>',
                fail: '<svg class="dvc-icon__broken" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 512 512" xml:space="preserve"><path d="M192,42.667H21.333C9.551,42.667,0,52.218,0,64v384c0,11.782,9.551,21.333,21.333,21.333H192c19.065,0,28.556-23.101,14.998-36.505L173.79,400l33.208-32.829c8.447-8.351,8.447-21.992,0-30.343L173.79,304l33.208-32.829c8.447-8.351,8.447-21.992,0-30.343L173.79,208l33.208-32.829c8.447-8.351,8.447-21.992,0-30.343L173.79,112l33.208-32.829C220.556,65.768,211.065,42.667,192,42.667z M128.447,223.171L161.655,256l-33.208,32.829c-8.447,8.351-8.447,21.992,0,30.343L161.655,352l-33.208,32.829c-8.447,8.351-8.447,21.992,0,30.343l11.628,11.495H42.667V85.333h97.409l-11.628,11.495c-8.447,8.351-8.447,21.992,0,30.343L161.655,160l-33.208,32.829C120,201.179,120,214.821,128.447,223.171z"/><path d="M490.667,42.667H347.221c-5.615,0-11.005,2.214-14.998,6.162l-48.555,48c-8.447,8.351-8.447,21.992,0,30.343L316.877,160l-33.208,32.829c-8.447,8.351-8.447,21.992,0,30.343L316.877,256l-33.208,32.829c-8.447,8.351-8.447,21.992,0,30.343L316.877,352l-33.208,32.829c-8.447,8.351-8.447,21.992,0,30.343l48.555,48c3.994,3.948,9.383,6.162,14.998,6.162h143.445c11.782,0,21.333-9.551,21.333-21.333V64C512,52.218,502.449,42.667,490.667,42.667z M469.333,426.667H355.986L329.011,400l33.208-32.829c8.447-8.351,8.447-21.992,0-30.343L329.011,304l33.208-32.829c8.447-8.351,8.447-21.992,0-30.343L329.011,208l33.208-32.829c8.447-8.351,8.447-21.992,0-30.343L329.011,112l26.975-26.667h113.347V426.667z"/></svg>'
            }, u = v;
            if (o.isIE) {
                u = {
                    loading: '<span class="dvc-ico dvc-icon__loading"></span>',
                    arrow: '<span class="dvc-ico dvc-icon__arrow"></span>',
                    refresh: '<span class="dvc-ico dvc-icon__slideRefresh"></span>',
                    info: '<span class="dvc-ico dvc-icon__followInfo"></span>',
                    pass: '<span class="dvc-ico dvc-icon__pass"></span>',
                    followPass: '<span class="dvc-ico dvc-icon__followPass"></span>',
                    reject: '<span class="dvc-ico dvc-icon__reject"></span>',
                    followReject: '<span class="dvc-ico dvc-icon__followReject"></span>',
                    shield: '<span class="dvc-ico dvc-icon__normalShield"></span>',
                    close: '<span class="dvc-ico dvc-icon__captchaClose captchaImg"></span>',
                    fail: '<span class="dvc-icon__broken"></span>'
                }
            }
            var g = {
                captcha: '<div class="dvc-captcha"></div>',
                placeholder: '<div class="dvc-placeholder"></div>',
                loading: '<div class="dvc-loading">' + u.loading + "</div><span>加载中...</span></div>",
                refresh: '<div class="dvc-operate__refresh" title="换一张图片">' + u.refresh + "</div>",
                follow: '<div class="dvc-follow"></div>',
                followTxt: '<div class="dvc-follow__txt"></div>',
                followMask: '<div class="dvc-follow__mask"></div>',
                flashMask: '<div class="dvc-placeholder__mask"></div>',
                tips: '<div class="dvc-slider__tips">' + f.tips + "</div>",
                operate: '<div class="dvc-operate"></div>',
                track: '<div class="dvc-slider__track"></div>',
                bgImg: '<img class="dvc-captcha__bgImg" alt="" />',
                puzzleImg: '<img class="dvc-captcha__puzzleImg" alt="" />',
                sourceImg: '<img class="dvc-captcha__sourceImg" alt="" />',
                winMask: '<div class="dvc-mask"></div>',
                slider: '<div class="dvc-slider"></div>',
                failMessage: '<p class="dvc-captcha__failMessage"></p>',
                panel: '<div class="dvc-captcha__panel"></div>',
                panelFrame: '<iframe class="dvc-captcha__coverFrame"></iframe>',
                handler: '<div class="dvc-slider__handler" style="width:' + c.handlerWidth + 'px"></div>',
                captchaWin: '<div class="dvc-captcha__win"><div class="dvc-win__title">' + u.shield + '<span class="dvc-captcha__clickTxt">安全认证</span><div class="dvc-captcha__titleClose">' + u.close + '</div></div><div class="dvc-captcha__winBody"></div></div>'
            };
            c.pj[0] = /PhantomJS/.test(t.navigator.userAgent) ? 1 : 0, c.
                pj[1] = t.callPhantom || t._phantom ? 1 : 0, this.bootstrap = function () {
                if (r) {
                    if (r.empty(), o.isUpgrade) return s.toUpgradeCaptcha(), !1;
                    s.initCaptcha()
                } else alert("未匹配到验证码页面元素")
            }, this.resizeDom = function (e, t, a) {
                return t.css({display: e, width: c.width, height: c.height >= 250 || a ? c.height : 250}), i(t)
            }, this.initCaptcha = function () {
                switch (c.showType) {
                    case"win":
                        s.initWinCaptcha();
                        break;
                    case"trigger":
                        s.initTriggerCaptcha();
                        break;
                    case"embed":
                        s.resizeDom("inline-block", r), s.initEmbedCaptcha()
                }
            }, this.renderCaptcha = function () {
                s.renderLoading(), o.isUpgrade || s.renderSlider()
            }, this.initEmbedCaptcha = function () {
                s.renderCaptcha(), s.getInitData()
            }, this.initTriggerCaptcha = function () {
                s.renderSlider(), s.getInitData()
            }, this.initWinCaptcha = function () {
                i(".dvc-mask") && i(".dvc-mask").remove(),
                i(".dvc-captcha__win") && i(".dvc-captcha__win").remove(),
                    c.winAutoShow ? s.revealWinCaptcha() : o.isWinShow && s.revealWinCaptcha(),
                    p = i("#" + a.targetElm), s.bindWinTargetElement(p)
            }, this.mountCaptchaDom = function (e) {
                var t = e || r;
                l = {
                    captchaDom: t.find(".dvc-captcha"),
                    placeholderDom: t.find(".dvc-placeholder"),
                    operateDom: t.find(".dvc-operate"),
                    refreshDom: t.find(".dvc-operate__refresh"),
                    followDom: t.find(".dvc-follow"),
                    trackDom: t.find(".dvc-slider__track"),
                    handlerDom: t.find(".dvc-slider__handler"),
                    bgImgDom: t.find(".dvc-captcha__bgImg"),
                    puzzleImgDom: t.find(".dvc-captcha__puzzleImg"),
                    sliderTipsDom: t.find(".dvc-slider__tips"),
                    sliderDom: t.find(".dvc-slider"),
                    sliderImgDom: t.find(".dvc-captcha__bgImg")
                }
            }, this.addPlaceholderDom = function () {
                l.placeholderDom = r.find(".dvc-placeholder")
            }, this.adapterCaptcha = function () {
                switch (c.showType) {
                    case"win":
                        s.adapterWin(), s.mountCaptchaDom(d);
                        break;
                    case"trigger":
                        s.adapterTrigger(), s.mountCaptchaDom();
                        break;
                    case"embed":
                        s.adapterEmbed(), s.mountCaptchaDom()
                }
                s.bindEvents()
            }, this.adapterEmbed = function () {
                s.renderCaptchaImg(), s.renderOperate()
            }, this.adapterTrigger = function () {
                o.canDrag = !0, o.isCaptchaShow && (r.find(".dvc-captcha").remove(), r.append(i(g.captcha).append(i(g.panel).css({
                    display: "none",
                    width: c.width,
                    height: c.placeHolderHeight
                }).append(g.placeholder).append(i(g.panelFrame)))), o.isTriggerShow && r.find(".dvc-captcha__panel").show(), s.addPlaceholderDom(), s.renderCaptchaImg(), s.renderOperate(), s.bindTriggerEvents())
            }, this.adapterWin = function () {
                s.renderCaptchaImg(), s.renderOperate()
                // reveal the Img
            }, this.renderCaptchaImg = function (e) {
                l.placeholderDom.width(c.width).height(c.placeHolderHeight).empty(), e ?
                    l.placeholderDom.empty().append(i(g.sourceImg).attr("src", c.urlCaptcha + e))
                    : l.placeholderDom.empty().append(i(g.bgImg).attr("src", c.urlCaptcha + c.bgImgUrl)).
                    append(i(g.puzzleImg).attr("src", c.urlCaptcha + c.puzzleImgUrl))
            }, this.renderOperate = function () {
                l.placeholderDom.append(i(g.operate).append(g.refresh))
            }, this.renderLoading = function () {
                r.append(i(g.captcha).empty().append(i(g.placeholder).height(c.placeHolderHeight).append(g.loading)))
            }, this.renderSlider = function () {
                r.append(i(g.slider).width(c.width).append(g.track).append(i(g.tips).
                width(c.width - 2)).append(i(g.handler).append(u.arrow)))
            }, this.revealRequestFail = function (e) {
                if (i(".dvc-captcha__winBody").empty().append(s.resizeDom("table-cell", i(g.captcha), !0).addClass("dvc-captcha__error").append(i(v.fail)).append(i(g.failMessage).append(e))), "embed" === a.showType && (i(r).find(".dvc-placeholder").empty().append(i(v.fail)).append(i(g.failMessage).append(e)), i(r).find(".dvc-slider").remove()), "trigger" === a.showType) return i(r).find(".dvc-slider__handler").remove(), i(r).find(".dvc-slider__tips").text(e), !1
            }, this.revealFollowTips = function (e, t) {
                l.placeholderDom.append(i(g.follow).append(g.followMask).append(i(g.followTxt).append(e + "<span>" + t + "</span>")))
            }, this.revealFlashMask = function () {
                l.placeholderDom.append(g.flashMask);
                var e = l.placeholderDom.find(".dvc-placeholder__mask");
                e.animate({left: "-100%"}, 600, function () {
                    e.remove()
                })
            }, this.revealVerfiySuccess = function () {
                o.canDrag = !1, s.renderCaptchaImg(c.sourceImgUrl), s.revealFollowTips(u.followPass, f.passTxt), s.revealFlashMask(), l.operateDom.remove(), l.sliderTipsDom.empty(), l.sliderDom.addClass("dvc-slider__pass"), l.handlerDom.empty().append(u.pass), "win" === c.showType ? t.setTimeout(function () {
                    p.attr("disabled", "disabled"), h.remove(), d.remove()
                }, f.winDisappearTime) : "trigger" === c.showType && t.setTimeout(function () {
                    l.captchaDom.remove(), l.handlerDom.removeClass("dvc-slider__handler--active")
                }, f.triggerDisappearTime)
            }, this.revealVerfiyFail = function (e) {
                s.revealFollowTips(u.followReject, f.rejectTxt), l.sliderTipsDom.empty(), l.handlerDom.empty().append(u.reject), l.sliderDom.addClass("dvc-slider__reject"), t.setTimeout(function () {
                    l.captchaDom.find(".dvc-follow").remove(), l.sliderDom.removeClass("dvc-slider__reject"), l.handlerDom.empty().append(u.arrow), e ? s.refreshCaptcha() : s.resetCaptcha()
                }, f.errShowTime)
            }, this.revealTriggerCaptcha = function () {
            },
                this.revealWinCaptcha = function () {
                function e() {
                    r.remove(), d.remove(), h.remove(), o.isWinShow = !1
                }

                var n = c.width + 30, l = 300 * parseInt(a.width) / 560 + 165;
                h = i(g.winMask), d = i(g.captchaWin), d.css({
                    width: n,
                    height: l,
                    marginTop: -parseInt(l / 2),
                    marginLeft: -parseInt(n / 2)
                }), i(document.body).append(h).append(d),
                    i(".dvc-captcha__winBody").empty().append(i(r).empty()),
                    o.isUpgrade ? s.toUpgradeCaptcha() : (s.renderCaptcha(), s.getInitData(),
                    i(".dvc-captcha") && i(".dvc-captcha").show()), s.isMobile() ?
                    d.find(".dvc-captcha__titleClose").on("touchstart", function () {
                    t.setTimeout(function () {
                        e(), a.closeCallback && a.closeCallback()
                    }, f.winCloseTime)
                }) : d.find(".dvc-captcha__titleClose").on("click", function () {
                    e(), a.closeCallback && a.closeCallback()
                }), o.isWinShow = !0
            }, this.refreshCaptcha = function () {
                s.bootstrap()
            }, this.resetCaptcha = function () {
                l.trackDom.width(0), l.puzzleImgDom.css({left: 0}), l.sliderTipsDom.empty().append(f.tips), l.handlerDom.css({left: 0}).removeClass("dvc-handler--active")
            }, this.bindWinTargetElement = function (e) {
                s.isMobile() ? e.unbind().on("touchstart", function () {
                    if (o.isVerifyed) return !1;
                    s.revealWinCaptcha()
                }) : e.unbind().on("click", function () {
                    if (o.isVerifyed) return !1;
                    s.revealWinCaptcha()
                })
            }, this.bindOperateEvent = function () {
                s.isMobile() ? l.refreshDom.on("touchstart", function () {
                    s.refreshCaptcha()
                }) : l.refreshDom.on("click",function () {
                    s.refreshCaptcha()
                })
            }, this.bindEvents = function () {
                if (!o.canDrag) return t.event ? t.event.cancelBubble = !0 : e.stopPropagation(), !1;
                var a = void 0, r = void 0, n = !1;
                l.handlerDom.on("mousedown touchstart", function (e) {
                    var t = new Date;
                    c.startTimeStamp = t.getTime(), e.preventDefault();
                    var i = 0, r = 0;
                    s.isMobile() ? (i = e.originalEvent.targetTouches[0].pageX, r = e.originalEvent.targetTouches[0].pageY, s.mouseTrackLog(i, r)) : (i = e.pageX, r = e.pageY, s.mouseTrackLog(i, r)), a = i, n = !0, l.handlerDom.addClass("dvc-slider__handler--active")
                }), i(document).on("mousemove touchmove", function (e) {
                    if (n && o.canDrag) {
                        var t = 0, i = 0, d = l.sliderDom.width();
                        s.isMobile() ? (t = e.originalEvent.changedTouches[0].pageX, i = e.originalEvent.changedTouches[0].pageY) : (t = e.pageX, i = e.pageY), s.mouseTrackLog(t, i);
                        var p = t - a;
                        p <= 0 && (p = 0), p >= d - c.handlerWidth && (p = d - c.handlerWidth), p || (p = 0), l.handlerDom.css({left: p}), l.trackDom.show().width(p), l.puzzleImgDom.css({left: p}), r = p
                    }
                }).on("mouseup touchend", function (e) {
                    if (!o.canDrag) try {
                        if ((e.target.className ? e.target.className : "").indexOf("dvc") > -1 || i(e.target).parents().hasClass("dvc-captcha")) return !1
                    } catch (e) {
                        return !1
                    }
                    var t = 0, a = 0;
                    if (s.isMobile()) try {
                        t = e.originalEvent.changedTouches[0].pageX, a = e.originalEvent.changedTouches[0].pageY
                    } catch (e) {
                    } else t = e.pageX, a = e.pageY;
                    n && (s.mouseTrackLog(t, a), n = !1, l.handlerDom.removeClass("dvc-slider__handler--active"), s.checkVerifiyResult(r), c.mouseTrack = [])
                }), s.bindOperateEvent(), o.isIE && (l.handlerDom.on("mouseover", function () {
                    l.handlerDom.addClass("dvc-slider__handler--hover")
                }), l.handlerDom.on("mouseout", function () {
                    l.handlerDom.removeClass("dvc-slider__handler--hover")
                }))
            }, this.mouseTrackLog = function (e, t) {
                var i = parseInt(e - l.sliderDom.offset().left), a = parseInt(t - l.sliderDom.offset().top),
                    r = new Date, n = r.getTime() - c.startTimeStamp;
                c.mouseTrack.push({p: parseInt(i) + "," + parseInt(a), t: n})
            }, this.bindTriggerEvents = function () {
                r.on("mouseenter", function (e) {
                    c.width;
                    r.find(".dvc-captcha__panel").show().addClass("dvc-captcha__trigger"), o.isTriggerShow = !0
                }), r.on("mouseleave", function () {
                    if (o.isTrigger) return !1;
                    var e = r.find(".dvc-captcha__panel");
                    l.followDom.remove(), e.removeClass("dvc-captcha__trigger").hide(), o.isTriggerShow = !1
                }), i(document).on("mousedown", function () {
                    o.isTrigger = !0
                }), i(document).on("mouseup", function () {
                    o.isTrigger = !1
                })
            }, this.toUpgradeCaptcha = function () {
                if (o.isUpgrade) {
                    ISDCaptcha({
                        element: a.element,
                        sessionId: a.sessionId,
                        width: a.width,
                        type: 320,
                        showType: a.showType,
                        winAutoShow: a.winAutoShow,
                        targetElm: a.targetElm,
                        isUpgrade: o.isUpgrade,
                        successCallback: a.successCallback,
                        failCallback: a.failCallback,
                        errorCallback: a.errorCallback,
                        closeCallback: a.closeCallback
                    }).init()
                }
            }, this.checkVerifiyResult = function (e) {
                for (var r = c.mouseTrack.slice(0, 260), n = "", l = 0; l < r.length; l++) n += r[l].p + "," + r[l].t + "|";
                var d = s.AESEncryption('{"x":"' + (e || 0) + '","track":"' + n + '","p":"' + c.pj + '","finger":"' + (t.xxzlfingertoken ? t.xxzlfingertoken : "") + '"}');
                i.ajax({
                    type: "GET",
                    dataType: "JSONP",
                    url: c.urlCaptcha + c.pathVerfiyCaptcha,
                    timestamp: Date.parse(new Date) / 1e3,
                    data: {responseId: c.responseId, sessionId: c.sessionId, data: d}
                }).done(function (e) {
                    if (0 === e.code) {
                        var t = e.data;
                        0 === t.status ? (o.isVerifyed = !0, c.sourceImgUrl = t.sourceimg, s.revealVerfiySuccess(), a.successCallback({
                            responseId: c.responseId,
                            successToken: t.successToken
                        })) : 1 === t.status ? (s.revealVerfiyFail(t.ischange), a.errorCallback && a.errorCallback({responseId: c.responseId})) : 2 === t.status && (o.isUpgrade = !0, s.toUpgradeCaptcha())
                    }
                }).fail(function () {
                    s.revealRequestFail("验证码信息获取失败，请刷新页面重试。")
                })
            }, this.getInitData = function (e) {
                i.ajax({
                    method: "GET",
                    url: c.urlCaptcha + c.pathGetCaptcha,
                    dataType: "jsonp",
                    data: {showType: c.showType, sessionId: c.sessionId}
                }).done(function (e) {
                    var t = e.data;
                    if (o.canDrag = !1, s.addPlaceholderDom(), 0 !== e.code)
                        return o.isCaptchaShow = !1, s.revealRequestFail(e.message), !1;
                    if (0 === t.status) {
                        if (320 === t.level) return o.isUpgrade = !0, s.toUpgradeCaptcha(), !1;
                        o.canDrag = !0, o.isCaptchaShow = !0,
                            c.bgImgUrl = t.bgImgUrl, c.puzzleImgUrl = t.puzzleImgUrl,
                            c.responseId = t.responseId
                    } else 1 === t.status && (o.isCaptchaShow = !1, s.revealRequestFail(e.tip));
                    s.adapterCaptcha()
                }).fail(function () {
                    r.remove(), s.revealRequestFail("验证码信息获取失败，请刷新页面重试。")
                })
            }, this.AESEncryption = function (e) {
                var t = CryptoJS.enc.Utf8.parse(c.responseId.substr(0, 16));
                return CryptoJS.AES.encrypt(e, t, {
                    iv: t,
                    mode: CryptoJS.mode.CBC,
                    padding: CryptoJS.pad.Pkcs7
                }).ciphertext.toString().toUpperCase()
            }, this.isMobile = function () {
                for (var e = navigator.userAgent, t = ["Android", "iPhone", "SymbianOS", "Windows Phone", "iPad", "iPod"], i = !1, a = 0; a < t.length; a++) if (e.indexOf(t[a]) > 0) {
                    i = !0;
                    break
                }
                return i
            }
        }
    };
    t.CaptchaSlide = t.CaptchaSlide = a
}


(window, window.XXZL58 ? window.XXZL58 : window.jQuery), function () {
    var e = e || function (e, t) {
        var i = {}, a = i.lib = {}, r = function () {
        }, n = a.Base = {
            extend: function (e) {
                r.prototype = this;
                var t = new r;
                return e && t.mixIn(e), t.hasOwnProperty("init") || (t.init = function () {
                    t.$super.init.apply(this, arguments)
                }), t.init.prototype = t, t.$super = this, t
            }, create: function () {
                var e = this.extend();
                return e.init.apply(e, arguments), e
            }, init: function () {
            }, mixIn: function (e) {
                for (var t in e) e.hasOwnProperty(t) && (this[t] = e[t]);
                e.hasOwnProperty("toString") && (this.toString = e.toString)
            }, clone: function () {
                return this.init.prototype.extend(this)
            }
        }, s = a.WordArray = n.extend({
            init: function (e, t) {
                e = this.words = e || [], this.sigBytes = void 0 != t ? t : 4 * e.length
            }, toString: function (e) {
                return (e || o).stringify(this)
            }, concat: function (e) {
                var t = this.words, i = e.words, a = this.sigBytes;
                if (e = e.sigBytes, this.clamp(), a % 4) for (var r = 0; r < e; r++) t[a + r >>> 2] |= (i[r >>> 2] >>> 24 - r % 4 * 8 & 255) << 24 - (a + r) % 4 * 8; else if (i.length > 65535) for (r = 0; r < e; r += 4) t[a + r >>> 2] = i[r >>> 2]; else t.push.apply(t, i);
                return this.sigBytes += e, this
            }, clamp: function () {
                var t = this.words, i = this.sigBytes;
                t[i >>> 2] &= 4294967295 << 32 - i % 4 * 8, t.length = e.ceil(i / 4)
            }, clone: function () {
                var e = n.clone.call(this);
                return e.words = this.words.slice(0), e
            }, random: function (t) {
                for (var i = [], a = 0; a < t; a += 4) i.push(4294967296 * e.random() | 0);
                return new s.init(i, t)
            }
        }), c = i.enc = {}, o = c.Hex = {
            stringify: function (e) {
                var t = e.words;
                e = e.sigBytes;
                for (var i = [], a = 0; a < e; a++) {
                    var r = t[a >>> 2] >>> 24 - a % 4 * 8 & 255;
                    i.push((r >>> 4).toString(16)), i.push((15 & r).toString(16))
                }
                return i.join("")
            }, parse: function (e) {
                for (var t = e.length, i = [], a = 0; a < t; a += 2) i[a >>> 3] |= parseInt(e.substr(a, 2), 16) << 24 - a % 8 * 4;
                return new s.init(i, t / 2)
            }
        }, l = c.Latin1 = {
            stringify: function (e) {
                var t = e.words;
                e = e.sigBytes;
                for (var i = [], a = 0; a < e; a++) i.push(String.fromCharCode(t[a >>> 2] >>> 24 - a % 4 * 8 & 255));
                return i.join("")
            }, parse: function (e) {
                for (var t = e.length, i = [], a = 0; a < t; a++) i[a >>> 2] |= (255 & e.charCodeAt(a)) << 24 - a % 4 * 8;
                return new s.init(i, t)
            }
        }, d = c.Utf8 = {
            stringify: function (e) {
                try {
                    return decodeURIComponent(escape(l.stringify(e)))
                } catch (e) {
                    throw Error("Malformed UTF-8 data")
                }
            }, parse: function (e) {
                return l.parse(unescape(encodeURIComponent(e)))
            }
        }, p = a.BufferedBlockAlgorithm = n.extend({
            reset: function () {
                this._data = new s.init, this._nDataBytes = 0
            }, _append: function (e) {
                "string" == typeof e && (e = d.parse(e)), this._data.concat(e), this._nDataBytes += e.sigBytes
            }, _process: function (t) {
                var i = this._data, a = i.words, r = i.sigBytes, n = this.blockSize, c = r / (4 * n),
                    c = t ? e.ceil(c) : e.max((0 | c) - this._minBufferSize, 0);
                if (t = c * n, r = e.min(4 * t, r), t) {
                    for (var o = 0; o < t; o += n) this._doProcessBlock(a, o);
                    o = a.splice(0, t), i.sigBytes -= r
                }
                return new s.init(o, r)
            }, clone: function () {
                var e = n.clone.call(this);
                return e._data = this._data.clone(), e
            }, _minBufferSize: 0
        });
        a.Hasher = p.extend({
            cfg: n.extend(), init: function (e) {
                this.cfg = this.cfg.extend(e), this.reset()
            }, reset: function () {
                p.reset.call(this), this._doReset()
            }, update: function (e) {
                return this._append(e), this._process(), this
            }, finalize: function (e) {
                return e && this._append(e), this._doFinalize()
            }, blockSize: 16, _createHelper: function (e) {
                return function (t, i) {
                    return new e.init(i).finalize(t)
                }
            }, _createHmacHelper: function (e) {
                return function (t, i) {
                    return new h.HMAC.init(e, i).finalize(t)
                }
            }
        });
        var h = i.algo = {};
        return i
    }(Math);
    !function () {
        var t = e, i = t.lib.WordArray;
        t.enc.Base64 = {
            stringify: function (e) {
                var t = e.words, i = e.sigBytes, a = this._map;
                e.clamp(), e = [];
                for (var r = 0; r < i; r += 3) for (var n = (t[r >>> 2] >>> 24 - r % 4 * 8 & 255) << 16 | (t[r + 1 >>> 2] >>> 24 - (r + 1) % 4 * 8 & 255) << 8 | t[r + 2 >>> 2] >>> 24 - (r + 2) % 4 * 8 & 255, s = 0; s < 4 && r + .75 * s < i; s++) e.push(a.charAt(n >>> 6 * (3 - s) & 63));
                if (t = a.charAt(64)) for (; e.length % 4;) e.push(t);
                return e.join("")
            }, parse: function (e) {
                var t = e.length, a = this._map, r = a.charAt(64);
                r && -1 != (r = e.indexOf(r)) && (t = r);
                for (var r = [], n = 0, s = 0; s < t; s++) if (s % 4) {
                    var c = a.indexOf(e.charAt(s - 1)) << s % 4 * 2, o = a.indexOf(e.charAt(s)) >>> 6 - s % 4 * 2;
                    r[n >>> 2] |= (c | o) << 24 - n % 4 * 8, n++
                }
                return i.create(r, n)
            }, _map: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        }
    }(), function (t) {
        function i(e, t, i, a, r, n, s) {
            return ((e = e + (t & i | ~t & a) + r + s) << n | e >>> 32 - n) + t
        }

        function a(e, t, i, a, r, n, s) {
            return ((e = e + (t & a | i & ~a) + r + s) << n | e >>> 32 - n) + t
        }

        function r(e, t, i, a, r, n, s) {
            return ((e = e + (t ^ i ^ a) + r + s) << n | e >>> 32 - n) + t
        }

        function n(e, t, i, a, r, n, s) {
            return ((e = e + (i ^ (t | ~a)) + r + s) << n | e >>> 32 - n) + t
        }

        for (var s = e, c = s.lib, o = c.WordArray, l = c.Hasher, c = s.algo, d = [], p = 0; p < 64; p++) d[p] = 4294967296 * t.abs(t.sin(p + 1)) | 0;
        c = c.MD5 = l.extend({
            _doReset: function () {
                this._hash = new o.init([1732584193, 4023233417, 2562383102, 271733878])
            }, _doProcessBlock: function (e, t) {
                for (var s = 0; s < 16; s++) {
                    var c = t + s, o = e[c];
                    e[c] = 16711935 & (o << 8 | o >>> 24) | 4278255360 & (o << 24 | o >>> 8)
                }
                var s = this._hash.words, c = e[t + 0], o = e[t + 1], l = e[t + 2], p = e[t + 3], h = e[t + 4],
                    f = e[t + 5], v = e[t + 6], u = e[t + 7], g = e[t + 8], m = e[t + 9], w = e[t + 10], _ = e[t + 11],
                    y = e[t + 12], x = e[t + 13], C = e[t + 14], k = e[t + 15], D = s[0], S = s[1], b = s[2], T = s[3],
                    D = i(D, S, b, T, c, 7, d[0]), T = i(T, D, S, b, o, 12, d[1]), b = i(b, T, D, S, l, 17, d[2]),
                    S = i(S, b, T, D, p, 22, d[3]), D = i(D, S, b, T, h, 7, d[4]), T = i(T, D, S, b, f, 12, d[5]),
                    b = i(b, T, D, S, v, 17, d[6]), S = i(S, b, T, D, u, 22, d[7]), D = i(D, S, b, T, g, 7, d[8]),
                    T = i(T, D, S, b, m, 12, d[9]), b = i(b, T, D, S, w, 17, d[10]), S = i(S, b, T, D, _, 22, d[11]),
                    D = i(D, S, b, T, y, 7, d[12]), T = i(T, D, S, b, x, 12, d[13]), b = i(b, T, D, S, C, 17, d[14]),
                    S = i(S, b, T, D, k, 22, d[15]), D = a(D, S, b, T, o, 5, d[16]), T = a(T, D, S, b, v, 9, d[17]),
                    b = a(b, T, D, S, _, 14, d[18]), S = a(S, b, T, D, c, 20, d[19]), D = a(D, S, b, T, f, 5, d[20]),
                    T = a(T, D, S, b, w, 9, d[21]), b = a(b, T, D, S, k, 14, d[22]), S = a(S, b, T, D, h, 20, d[23]),
                    D = a(D, S, b, T, m, 5, d[24]), T = a(T, D, S, b, C, 9, d[25]), b = a(b, T, D, S, p, 14, d[26]),
                    S = a(S, b, T, D, g, 20, d[27]), D = a(D, S, b, T, x, 5, d[28]), T = a(T, D, S, b, l, 9, d[29]),
                    b = a(b, T, D, S, u, 14, d[30]), S = a(S, b, T, D, y, 20, d[31]), D = r(D, S, b, T, f, 4, d[32]),
                    T = r(T, D, S, b, g, 11, d[33]), b = r(b, T, D, S, _, 16, d[34]), S = r(S, b, T, D, C, 23, d[35]),
                    D = r(D, S, b, T, o, 4, d[36]), T = r(T, D, S, b, h, 11, d[37]), b = r(b, T, D, S, u, 16, d[38]),
                    S = r(S, b, T, D, w, 23, d[39]), D = r(D, S, b, T, x, 4, d[40]), T = r(T, D, S, b, c, 11, d[41]),
                    b = r(b, T, D, S, p, 16, d[42]), S = r(S, b, T, D, v, 23, d[43]), D = r(D, S, b, T, m, 4, d[44]),
                    T = r(T, D, S, b, y, 11, d[45]), b = r(b, T, D, S, k, 16, d[46]), S = r(S, b, T, D, l, 23, d[47]),
                    D = n(D, S, b, T, c, 6, d[48]), T = n(T, D, S, b, u, 10, d[49]), b = n(b, T, D, S, C, 15, d[50]),
                    S = n(S, b, T, D, f, 21, d[51]), D = n(D, S, b, T, y, 6, d[52]), T = n(T, D, S, b, p, 10, d[53]),
                    b = n(b, T, D, S, w, 15, d[54]), S = n(S, b, T, D, o, 21, d[55]), D = n(D, S, b, T, g, 6, d[56]),
                    T = n(T, D, S, b, k, 10, d[57]), b = n(b, T, D, S, v, 15, d[58]), S = n(S, b, T, D, x, 21, d[59]),
                    D = n(D, S, b, T, h, 6, d[60]), T = n(T, D, S, b, _, 10, d[61]), b = n(b, T, D, S, l, 15, d[62]),
                    S = n(S, b, T, D, m, 21, d[63]);
                s[0] = s[0] + D | 0, s[1] = s[1] + S | 0, s[2] = s[2] + b | 0, s[3] = s[3] + T | 0
            }, _doFinalize: function () {
                var e = this._data, i = e.words, a = 8 * this._nDataBytes, r = 8 * e.sigBytes;
                i[r >>> 5] |= 128 << 24 - r % 32;
                var n = t.floor(a / 4294967296);
                for (i[15 + (r + 64 >>> 9 << 4)] = 16711935 & (n << 8 | n >>> 24) | 4278255360 & (n << 24 | n >>> 8), i[14 + (r + 64 >>> 9 << 4)] = 16711935 & (a << 8 | a >>> 24) | 4278255360 & (a << 24 | a >>> 8), e.sigBytes = 4 * (i.length + 1), this._process(), e = this._hash, i = e.words, a = 0; a < 4; a++) r = i[a], i[a] = 16711935 & (r << 8 | r >>> 24) | 4278255360 & (r << 24 | r >>> 8);
                return e
            }, clone: function () {
                var e = l.clone.call(this);
                return e._hash = this._hash.clone(), e
            }
        }), s.MD5 = l._createHelper(c), s.HmacMD5 = l._createHmacHelper(c)
    }(Math), function () {
        var t = e, i = t.lib, a = i.Base, r = i.WordArray, i = t.algo, n = i.EvpKDF = a.extend({
            cfg: a.extend({keySize: 4, hasher: i.MD5, iterations: 1}), init: function (e) {
                this.cfg = this.cfg.extend(e)
            }, compute: function (e, t) {
                for (var i = this.cfg, a = i.hasher.create(), n = r.create(), s = n.words, c = i.keySize, i = i.iterations; s.length < c;) {
                    o && a.update(o);
                    var o = a.update(e).finalize(t);
                    a.reset();
                    for (var l = 1; l < i; l++) o = a.finalize(o), a.reset();
                    n.concat(o)
                }
                return n.sigBytes = 4 * c, n
            }
        });
        t.EvpKDF = function (e, t, i) {
            return n.create(i).compute(e, t)
        }
    }(), e.lib.Cipher || function (t) {
        var i = e, a = i.lib, r = a.Base, n = a.WordArray, s = a.BufferedBlockAlgorithm, c = i.enc.Base64,
            o = i.algo.EvpKDF, l = a.Cipher = s.extend({
                cfg: r.extend(), createEncryptor: function (e, t) {
                    return this.create(this._ENC_XFORM_MODE, e, t)
                }, createDecryptor: function (e, t) {
                    return this.create(this._DEC_XFORM_MODE, e, t)
                }, init: function (e, t, i) {
                    this.cfg = this.cfg.extend(i), this._xformMode = e, this._key = t, this.reset()
                }, reset: function () {
                    s.reset.call(this), this._doReset()
                }, process: function (e) {
                    return this._append(e), this._process()
                }, finalize: function (e) {
                    return e && this._append(e), this._doFinalize()
                }, keySize: 4, ivSize: 4, _ENC_XFORM_MODE: 1, _DEC_XFORM_MODE: 2, _createHelper: function (e) {
                    return {
                        encrypt: function (t, i, a) {
                            return ("string" == typeof i ? u : v).encrypt(e, t, i, a)
                        }, decrypt: function (t, i, a) {
                            return ("string" == typeof i ? u : v).decrypt(e, t, i, a)
                        }
                    }
                }
            });
        a.StreamCipher = l.extend({
            _doFinalize: function () {
                return this._process(!0)
            }, blockSize: 1
        });
        var d = i.mode = {}, p = function (e, t, i) {
            var a = this._iv;
            a ? this._iv = void 0 : a = this._prevBlock;
            for (var r = 0; r < i; r++) e[t + r] ^= a[r]
        }, h = (a.BlockCipherMode = r.extend({
            createEncryptor: function (e, t) {
                return this.Encryptor.create(e, t)
            }, createDecryptor: function (e, t) {
                return this.Decryptor.create(e, t)
            }, init: function (e, t) {
                this._cipher = e, this._iv = t
            }
        })).extend();
        h.Encryptor = h.extend({
            processBlock: function (e, t) {
                var i = this._cipher, a = i.blockSize;
                p.call(this, e, t, a), i.encryptBlock(e, t), this._prevBlock = e.slice(t, t + a)
            }
        }), h.Decryptor = h.extend({
            processBlock: function (e, t) {
                var i = this._cipher, a = i.blockSize, r = e.slice(t, t + a);
                i.decryptBlock(e, t), p.call(this, e, t, a), this._prevBlock = r
            }
        }), d = d.CBC = h, h = (i.pad = {}).Pkcs7 = {
            pad: function (e, t) {
                for (var i = 4 * t, i = i - e.sigBytes % i, a = i << 24 | i << 16 | i << 8 | i, r = [], s = 0; s < i; s += 4) r.push(a);
                i = n.create(r, i), e.concat(i)
            }, unpad: function (e) {
                e.sigBytes -= 255 & e.words[e.sigBytes - 1 >>> 2]
            }
        }, a.BlockCipher = l.extend({
            cfg: l.cfg.extend({mode: d, padding: h}), reset: function () {
                l.reset.call(this);
                var e = this.cfg, t = e.iv, e = e.mode;
                if (this._xformMode == this._ENC_XFORM_MODE) var i = e.createEncryptor; else i = e.createDecryptor, this._minBufferSize = 1;
                this._mode = i.call(e, this, t && t.words)
            }, _doProcessBlock: function (e, t) {
                this._mode.processBlock(e, t)
            }, _doFinalize: function () {
                var e = this.cfg.padding;
                if (this._xformMode == this._ENC_XFORM_MODE) {
                    e.pad(this._data, this.blockSize);
                    var t = this._process(!0)
                } else t = this._process(!0),
                    e.unpad(t);
                return t
            }, blockSize: 4
        });
        var f = a.CipherParams = r.extend({
            init: function (e) {
                this.mixIn(e)
            }, toString: function (e) {
                return (e || this.formatter).stringify(this)
            }
        }), d = (i.format = {}).OpenSSL = {
            stringify: function (e) {
                var t = e.ciphertext;
                return e = e.salt, (e ? n.create([1398893684, 1701076831]).concat(e).concat(t) : t).toString(c)
            }, parse: function (e) {
                e = c.parse(e);
                var t = e.words;
                if (1398893684 == t[0] && 1701076831 == t[1]) {
                    var i = n.create(t.slice(2, 4));
                    t.splice(0, 4), e.sigBytes -= 16
                }
                return f.create({ciphertext: e, salt: i})
            }
        }, v = a.SerializableCipher = r.extend({
            cfg: r.extend({format: d}), encrypt: function (e, t, i, a) {
                a = this.cfg.extend(a);
                var r = e.createEncryptor(i, a);
                return t = r.finalize(t), r = r.cfg, f.create({
                    ciphertext: t,
                    key: i,
                    iv: r.iv,
                    algorithm: e,
                    mode: r.mode,
                    padding: r.padding,
                    blockSize: e.blockSize,
                    formatter: a.format
                })
            }, decrypt: function (e, t, i, a) {
                return a = this.cfg.extend(a), t = this._parse(t, a.format), e.createDecryptor(i, a).finalize(t.ciphertext)
            }, _parse: function (e, t) {
                return "string" == typeof e ? t.parse(e, this) : e
            }
        }), i = (i.kdf = {}).OpenSSL = {
            execute: function (e, t, i, a) {
                return a || (a = n.random(8)), e = o.create({keySize: t + i}).compute(e, a), i = n.create(e.words.slice(t), 4 * i), e.sigBytes = 4 * t, f.create({
                    key: e,
                    iv: i,
                    salt: a
                })
            }
        }, u = a.PasswordBasedCipher = v.extend({
            cfg: v.cfg.extend({kdf: i}), encrypt: function (e, t, i, a) {
                return a = this.cfg.extend(a), i = a.kdf.execute(i, e.keySize, e.ivSize), a.iv = i.iv, e = v.encrypt.call(this, e, t, i.key, a), e.mixIn(i), e
            }, decrypt: function (e, t, i, a) {
                return a = this.cfg.extend(a), t = this._parse(t, a.format), i = a.kdf.execute(i, e.keySize, e.ivSize, t.salt), a.iv = i.iv, v.decrypt.call(this, e, t, i.key, a)
            }
        })
    }(), function () {
        for (var t = e, i = t.lib.BlockCipher, a = t.algo, r = [], n = [], s = [], c = [], o = [], l = [], d = [], p = [], h = [], f = [], v = [], u = 0; u < 256; u++) v[u] = u < 128 ? u << 1 : u << 1 ^ 283;
        for (var g = 0, m = 0, u = 0; u < 256; u++) {
            var w = m ^ m << 1 ^ m << 2 ^ m << 3 ^ m << 4, w = w >>> 8 ^ 255 & w ^ 99;
            r[g] = w, n[w] = g;
            var _ = v[g], y = v[_], x = v[y], C = 257 * v[w] ^ 16843008 * w;
            s[g] = C << 24 | C >>> 8, c[g] = C << 16 | C >>> 16, o[g] = C << 8 | C >>> 24, l[g] = C, C = 16843009 * x ^ 65537 * y ^ 257 * _ ^ 16843008 * g, d[w] = C << 24 | C >>> 8, p[w] = C << 16 | C >>> 16, h[w] = C << 8 | C >>> 24, f[w] = C, g ? (g = _ ^ v[v[v[x ^ _]]], m ^= v[v[m]]) : g = m = 1
        }
        var k = [0, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54], a = a.AES = i.extend({
            _doReset: function () {
                for (var e = this._key, t = e.words, i = e.sigBytes / 4, e = 4 * ((this._nRounds = i + 6) + 1), a = this._keySchedule = [], n = 0; n < e; n++) if (n < i) a[n] = t[n]; else {
                    var s = a[n - 1];
                    n % i ? i > 6 && n % i == 4 && (s = r[s >>> 24] << 24 | r[s >>> 16 & 255] << 16 | r[s >>> 8 & 255] << 8 | r[255 & s]) : (s = s << 8 | s >>> 24, s = r[s >>> 24] << 24 | r[s >>> 16 & 255] << 16 | r[s >>> 8 & 255] << 8 | r[255 & s], s ^= k[n / i | 0] << 24), a[n] = a[n - i] ^ s
                }
                for (t = this._invKeySchedule = [], i = 0; i < e; i++) n = e - i, s = i % 4 ? a[n] : a[n - 4], t[i] = i < 4 || n <= 4 ? s : d[r[s >>> 24]] ^ p[r[s >>> 16 & 255]] ^ h[r[s >>> 8 & 255]] ^ f[r[255 & s]]
            }, encryptBlock: function (e, t) {
                this._doCryptBlock(e, t, this._keySchedule, s, c, o, l, r)
            }, decryptBlock: function (e, t) {
                var i = e[t + 1];
                e[t + 1] = e[t + 3], e[t + 3] = i, this._doCryptBlock(e, t, this._invKeySchedule, d, p, h, f, n), i = e[t + 1], e[t + 1] = e[t + 3], e[t + 3] = i
            }, _doCryptBlock: function (e, t, i, a, r, n, s, c) {
                for (var o = this._nRounds, l = e[t] ^ i[0], d = e[t + 1] ^ i[1], p = e[t + 2] ^ i[2], h = e[t + 3] ^ i[3], f = 4, v = 1; v < o; v++) var u = a[l >>> 24] ^ r[d >>> 16 & 255] ^ n[p >>> 8 & 255] ^ s[255 & h] ^ i[f++], g = a[d >>> 24] ^ r[p >>> 16 & 255] ^ n[h >>> 8 & 255] ^ s[255 & l] ^ i[f++], m = a[p >>> 24] ^ r[h >>> 16 & 255] ^ n[l >>> 8 & 255] ^ s[255 & d] ^ i[f++], h = a[h >>> 24] ^ r[l >>> 16 & 255] ^ n[d >>> 8 & 255] ^ s[255 & p] ^ i[f++], l = u, d = g, p = m;
                u = (c[l >>> 24] << 24 | c[d >>> 16 & 255] << 16 | c[p >>> 8 & 255] << 8 | c[255 & h]) ^ i[f++], g = (c[d >>> 24] << 24 | c[p >>> 16 & 255] << 16 | c[h >>> 8 & 255] << 8 | c[255 & l]) ^ i[f++], m = (c[p >>> 24] << 24 | c[h >>> 16 & 255] << 16 | c[l >>> 8 & 255] << 8 | c[255 & d]) ^ i[f++], h = (c[h >>> 24] << 24 | c[l >>> 16 & 255] << 16 | c[d >>> 8 & 255] << 8 | c[255 & p]) ^ i[f++], e[t] = u, e[t + 1] = g, e[t + 2] = m, e[t + 3] = h
            }, keySize: 8
        });
        t.AES = i._createHelper(a)
    }(), window.CryptoJS = window.CryptoJS = e
}();