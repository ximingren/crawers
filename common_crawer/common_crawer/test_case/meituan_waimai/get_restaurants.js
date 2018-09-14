/**
 *  动态加载商家列表，同时实现图片懒加载
 *
 *  @author jinweigang@meituan.com
 *  @date 2016-04-07
 */

define(['lib/jquery', 'module/bridge', 'module/general','util/utils', 'util/cookie'], function($, bridge, general, utils, Cookie) {
  'use strict';

  var TIMER      = null;
  var ICON_LEN   = 0;
  var IS_LOADING = false;
  var HAS_MORE   = true;
  var CLASSIFY   = ['cate_all'];

  // 数字加密回传参数: mtsi_font_css_version
  var CSS_REG = /^[\s\S]*\/font\/(\S*)\.eot[\s\S]*$/;
  var mtsi_font_css_version = '';
  if (window.cssResource) {
    mtsi_font_css_version = window.cssResource.match(CSS_REG)[1];
  }
  var PARAM      = {
    classify_type: '',
    sort_type: 0,
    price_type: 0,
    support_online_pay: 0,
    support_invoice: 0,
    support_logistic: 0,
    page_offset: 21,
    page_size: 20,
    mtsi_font_css_version: mtsi_font_css_version
  };

  //DOM对象
  var DOMS = {
    container   : $(window),
    body        : $('body,html'),
    restList    : $('.rest-list ul'),
    cateFilter  : $('.imgsort-list'),
    restFilter  : $('.rest-filter a'),
    sortFilter  : $('.sort-filter .sort'),
    priceFilter : $('.prices li a'),
    priceBox    : $('.prices .all')
  };

  /**
   * @function preload
   * @description 预加载图片
   * @param {el} 当前img对象
   * @param {callback} 图片加载完毕后的回调函数
   */
  var preload = function(el, callback) {
    var src = el.data('src');

    var i = new Image();
    //创建一个Image对象，实现图片的预下载
    i.onload = function() {
      i.onload = null;
      if (callback) {
        callback(src, {
          width: i.width,
          height: i.height
        });
      }
      el.data('loaded', 1);
    };
    i.src = src;
  };

  /**
   * @function loading
   * @description 循环遍历，图片居中处理
   */
  var loading = function() {
    var els = [];
    $.each($('.scroll-loading'), function(i, el) {
      el = $(el);
      if (el.data('loaded') != 1) {
        preload(el, function(src, options) {
          // 如果设了max-width或max-height，则自动缩放居中
          var imgWidth = options.width;
          var imgHeight = options.height;
          var maxWidth = el.data('max-width');
          var maxHeight = el.data('max-height');
          if (maxWidth && maxHeight && imgWidth && imgHeight) {
            var maxRate = maxWidth / maxHeight;
            var imgRate = imgWidth / imgHeight;
            if (imgRate <= maxRate) {  // 瘦高型，左右居中
              imgHeight = maxHeight;
              imgWidth = imgHeight * imgRate;
            } else {  // 矮胖型，上下居中
              imgWidth = maxWidth;
              imgHeight = imgWidth / imgRate;
            }

            el.css({
              width: imgWidth+'px',
              height: imgHeight+'px'
            });
          }
          el.attr('src',src);

        });

        // 有统计需求的门店
        els.push(el);
      }
    });
    if (els.length != 0) {
      bridge.trigger('log:home', els);
    }
  };

  //商家模板拼接
  var template = {
    //变量不存在返回空字符串
    judgeNull: function(data, type){
      var tag = null;
      tag = type == 'num' ? 0 : '';
      return data ? data : tag;
    },
    //tag标签循环拼接
    loopTag: function(arr){
      var tagList = '';
      if(!arr.length) return tagList;
      arr.map(function(item, index) {
        tagList += (' data-' + item + '="1"');
      });
      return tagList;
    },

    //预览
    preview: function(data,index){
      var html,url,newRest;
      url = (data.pic_url && data.pic_url != "") ? data.pic_url : 'http://xs01.meituan.net/waimai_web/img/poidefault_1.png';
      newRest = (data && data.new_promotion==1) ? '<div class="rest-tag rest-tag-new">新店</div>' : '';
      html = '<div class="preview">\
                <img data-rid="' + template.judgeNull(data.wm_poi_id) + '" data-index="' + index + '" class="scroll-loading" src="http://xs01.meituan.net/waimai_web/img/a.gif" data-src="' + url + '" data-max-width="208" data-max-height="156"  />\
                <div class="rest-tags">\
                  <!-- 新商家提示icon -->\
                  ' + newRest + '\
                </div>\
              </div>';
      return html;
    },

    shipping: function(data){
      var html, busy, scoreNum, saleNum;
      var score = (data.wmPoi4Web.wm_poi_score)/5 * 60,
          scoreEmpty = data.wmPoi4Web.wm_poi_score * 3;
      scoreNum = data.wmPoi4Web.wm_poi_score > 0 ? data.wmPoi4Web.wm_poi_score.toFixed(1)+'分'  : '暂无';

      if(data.busy){
        busy = '<div class="outof-sale busycolor">忙碌中</div>';
      } else {
        busy = '<div class="timer-tip"><span class="timer cc-lightred-new">接受预订，' + template.judgeNull(data.shipping_time_info.beg_shipping_time) + '开始送餐</span></div>';
      }

      if(data.wmPoi4Web.status != 3){
        if (data.wmPoi4Web.month_sale_num == 0) {
          saleNum = '<span class="total cc-lightred-new fr"></span>';
        } else if(data.wmPoi4Web.month_sale_num <= 200000) {
          saleNum = '<span class="total cc-lightred-new fr">月售' + template.judgeNull(data.wmPoi4Web.month_sale_num) + '单</span>';
        } else {
          saleNum = '<span class="total cc-lightred-new fr">月售200000+单</span>';
        }
      }

      if (data.shipping_time_info.in_shipping_time==0 && data.wmPoi4Web.status!=3) {
        html = busy;
      } else if (data.wmPoi4Web.status == 3) {
        html = '<div class="outof-sale">休息中，不接受订单</div>';
      } else {
        html = '<div class="rank clearfix">\
                      <span class="star-ranking fl">\
                        <span class="star-score" style="width: '+ (score + scoreEmpty) + 'px"></span>\
                      </span>\
                      <span class="score-num fl">' + scoreNum + '</span>\
                    </div>';
      }
      return html;
    },

    //内容
    content: function(data){
      var html='', busy='', shipping='', shippingFee='', shippingTime='', scoreNum='', saleNum='';

      if (data.wmPoi4Web.wmCPoiLbs.shipping_fee != 0) {
        shippingFee = '<span class="send-price mtsi-num">配送费:￥' + template.judgeNull(data.shipping_fee_encoded) + '</span>';
      } else {
        shippingFee = '<span class="send-price">免配送费</span>';
      }

      if (data.shipping_time_info.in_shipping_time != 0) {
        if (data.wmPoi4Web.avg_delivery_time == 0) {
          shippingTime = '暂无';
        } else if(data.wmPoi4Web.avg_delivery_time <= 50) {
          shippingTime = data.avg_delivery_time_encoded + '分钟';
        } else {
          shippingTime = '50+分钟';
        }
      }
      html = '<div class="content">\
                  <div class="name">\
                    <span title="' + template.judgeNull(data.wmPoi4Web.name) + '">' + utils.countChars(data.wmPoi4Web.name, 22) + '</span>\
                  </div>\
                  ' + this.shipping(data) + '\
                  <div class="price">\
                    <span class="start-price mtsi-num">起送:￥' + template.judgeNull(data.min_price_encoded, 'num') + '</span>\
                    ' + shippingFee + '\
                    <span class="send-time mtsi-num"><i class="icon i-poi-timer"></i>' + shippingTime + '</span>\
                  </div>\
                </div>';
      return html;
    },
    //其他条件
    logistic: function(data){
      var html = '';
      if(data.logistic_type && data.logistic_type==1){
        if (ICON_LEN < 7) {
          ICON_LEN++;
          html += '<i class="icon i-delivery"></i>';
        }
        html += '<script type="text/template" data-icon="i-delivery">由美团专送提供专业高品质送餐服务</script>';
      }
      return html;
    },

    //在线支付
    onlinePay: function(data){
      var html = '';
      if(data.wmPoi4Web.support_pay && data.wmPoi4Web.support_pay > 0){
        if (ICON_LEN < 7) {
          ICON_LEN++;
          html += '<i class="icon i-pay"></i>';
        }
        html += '<script type="text/template" data-icon="i-pay">该商家支持在线支付</script>';
      }
      return html;
    },

    //支持代金券
    coupon: function(data){
      var html = '';
      if(data.actInfoVo && data.actInfoVo.use_coupon_marketing_enjoyed){
        if (ICON_LEN < 7) {
          ICON_LEN++;
          html += '<i class="icon i-ticket"></i>';
        }
        html += '<script type="text/template" data-icon="i-ticket">该餐厅支持使用代金券<span class="special">(手机客户端专享)</span></script>';
      }
      return html;
    },

    //新用户下单返券
    sendCoupon: function(data){
      var html = '',
          price = '',
          arr=[];
      var couponTip = '新用户下单，返';

      if(data.actInfoVo && data.actInfoVo.first_order_send_coupon_enjoyed){
        if (ICON_LEN < 7) {
          ICON_LEN++;
          html += '<i class="icon i-fan"></i>';
        }
        data.actInfoVo.first_order_send_coupon_logo.details.map(function(item) {
          price = item.coupon_price ? item.coupon_price.toFixed(1)+'元' : '';
          couponTip = couponTip + item.coupon_count + price;
          if(item.coupon_type == 1){
            couponTip += '代金券';
          } else {
            couponTip += '支付红包';
          }
          arr.push(couponTip);
        });

        html += '<script type="text/template" data-icon="i-fan">' + arr.join(',') +'<span class="special">(手机客户端专享)</span></script>';
      }
      return html;
    },

    //支持发票
    supportInvoice: function(data){
      var html = '';
      if(data.wmPoi4Web.invoice_support == 1){
        if (ICON_LEN < 7) {
          ICON_LEN++;
          html += '<i class="icon i-cheque"></i>';
        }
        html += '<script type="text/template" data-icon="i-cheque">支持开发票，开票金额'+data.wmPoi4Web.invoice_min_price+'元起。请在下单时填好发票抬头。'+template.judgeNull(data.wmPoi4Web.invoice_description)+'</script>';
      }
      return html;
    },

    //新版套餐送优惠
    fullDonation: function(data){
      var html = '',
          text = '';
      if(data.actInfoVo && data.actInfoVo.full_donation_enjoyed){
        if (ICON_LEN < 7) {
          ICON_LEN++;
          html += '<i class="icon i-free-gift"></i>';
        }
        if (data.actInfoVo.full_donation_logo && data.actInfoVo.full_donation_logo.full_price <= 0.000001) {
          text = '下单即赠' + template.judgeNull(data.actInfoVo.full_donation_logo.gift_name);
        } else {
          text = '每单满' + template.judgeNull(data.actInfoVo.full_donation_logo.full_price) + '元赠送' + template.judgeNull(data.actInfoVo.full_donation_logo.gift_name);
        }
        html += '<script type="text/template" data-icon="i-free-gift">' + text + '<span class="special">(手机客户端专享)</span></script>';
      }
      return html;
    },

    //首单立减
    firstOrder: function(data){
      var html = '';
      if(data.actInfoVo && data.actInfoVo.first_order_enjoyed){
        if (ICON_LEN < 7) {
          ICON_LEN++;
          html += '<i class="icon i-first"></i>';
        }
        html += '<script type="text/template" data-icon="i-first">新用户首次下单,立减' + template.judgeNull(data.actInfoVo.first_order_logo.discount,'num') + '元<span class="special">(手机客户端专享)</span></script>';
      }
      return html;
    },

    //阶梯满减
    fullDiscount: function(data){
      var html = '',
          discountTip = '',
          arr = [];

      if(data.actInfoVo && data.actInfoVo.full_discount_enjoyed){
        if (ICON_LEN < 7) {
          ICON_LEN++;
          html += '<i class="icon i-minus"></i>';
        }
        data.actInfoVo.full_discount_logo.discount_detail.map(function(item) {
          discountTip = discountTip + '满' + item.limit_price+'元减' + template.judgeNull(item.discount,'num').toFixed(0) + '元';
          if(item.online_discount > 0.000001){
            discountTip = discountTip + ',在线支付再减' + template.judgeNull(item.online_discount,'num').toFixed(0);
          }
          arr.push(discountTip);
        });

        html += '<script type="text/template" data-icon="i-fan">' + arr.join(';') +'<span class="special">(手机客户端专享)</span></script>';
      }
      return html;
    },

    //超时赔付
    overTime: function(data){
      var html = '',
          specailMealTip = '';
      if(data.actInfoVo && data.actInfoVo.compensate_enjoyed){
        if (ICON_LEN < 7) {
          ICON_LEN++;
          html += '<i class="icon i-reimbursement"></i>';
        }
        specailMealTip = '该餐厅支持超时赔付活动,超' + data.actInfoVo.compensate_logo.minutes+'分钟'+data.actInfoVo.compensate_logo.discount+'。'
             + data.actInfoVo.compensate_logo.note+'。预订订单不参与超时赔付。';
        html += '<script type="text/template" data-icon="i-reimbursement">' + specailMealTip + '<span class="special">(手机客户端专享)</span></script>';
      }
      return html;
    },

    //预订享优惠
    aheadDiscount: function(data){
      var html = '',
          aheadTip = '',
          arr = [];

      if(data.actInfoVo && data.actInfoVo.ahead_discount_enjoyed){
        if (ICON_LEN < 7) {
          ICON_LEN++;
          html += '<i class="icon i-ding"></i>';
        }
        data.actInfoVo.ahead_discount_logo.ahead_discount_detail.map(function(item) {
          aheadTip = aheadTip + item.start_time + '-' + item.end_time+'下单减'+item.discount+'元';
          arr.push(aheadTip);
        });

        html += '<script type="text/template" data-icon="i-ding">' + arr.join(';') +'<span class="special">(手机客户端专享)</span></script>';
      }
      return html;
    },

    //增加抵价券优惠
    couponDiscount: function(data){
      var html = '';
      if(data.actInfoVo && data.actInfoVo.coupon_discount_enjoyed){
        if (ICON_LEN < 7) {
          ICON_LEN++;
          html += '<i class="icon i-di"></i>';
        }
        html += '<script type="text/template" data-icon="i-di">该餐厅支持使用抵价券，用抵价券订餐可抵' + template.judgeNull(data.actInfoVo.coupon_discount_logo.discount).toFixed(1) + '元<span class="special">(手机客户端专享)</span></script>';
      }
      return html;
    },

    //支持使用代金券
    supportCoupon: function(data){
      var html = '';
      if(data.is_fst5coupon_act == 1){
        if (ICON_LEN < 7) {
          ICON_LEN++;
          html += '<i class="icon i-ticket fl"></i>';
        }
        html += '<script type="text/template" data-icon="i-ticket">本店支持使用代金券</script>';
      }
      return html;
    },

    //增加套餐赠品
    mealsDonation: function(data){
      var html = '',
          mealsTip = '';

      if(data.actInfoVo && data.actInfoVo.meals_donation_enjoyed && data.actInfoVo.meal_donation_logos && data.actInfoVo.meal_donation_logos.length!=0){
        data.actInfoVo.meal_donation_logos.map(function(item, index) {
          if ((7 - ICON_LEN - index - 1) > -1 ) {
            html += '<i class="i-ph17x17"><img src="' + template.judgeNull(item.pic_url) + '" height="17" width="17"></i>';
          }
          html += '<script type="text/template" data-icon="i-ph17x17"  data-pic="' + template.judgeNull(item.pic_url) + '">' + template.judgeNull(item.description) + '<span class="special">(手机客户端专享)</span></script>';
        });
        ICON_LEN += data.actInfoVo.meal_donation_logos.length;
      }
      return html;
    },

    //增加特价套餐 x元管饱
    specialMeal: function(data){
      var html = '',
          mealsTip = '';

      if(data.actInfoVo && data.actInfoVo.special_meal_enjoyed && data.actInfoVo.special_meal_logos && data.actInfoVo.special_meal_logos.length!=0){
        data.actInfoVo.special_meal_logos.map(function(item, index) {
          if ((7 - ICON_LEN - index - 1) > -1 ) {
            ICON_LEN++;
            html += '<i class="i-ph17x17"><img src="' + template.judgeNull(item.pic_url) + '" height="17" width="17"></i>';
          }
          html += '<script type="text/template" data-icon="i-ph17x17"  data-pic="' + template.judgeNull(item.pic_url) + '">' + template.judgeNull(item.act_price).toFixed(1) + '元管饱<span class="special">(手机客户端专享)</span></script>';
        });
        ICON_LEN += data.actInfoVo.meal_donation_logos.length;
      }
      return html;
    },

    //阶梯满返红包
    fullSendCoupon: function(data){
      var html = '',
          fullSend = '',
          arr = [];

      if(data.actInfoVo && data.actInfoVo.full_send_coupon_enjoyed){
        if (ICON_LEN < 7) {
          ICON_LEN++;
          html += '<i class="icon i-fan"></i>';
        }
        data.actInfoVo.ahead_discount_logo.ahead_discount_detail.map(function(item) {
          fullSend = fullSend +'支付金额' + item.full_price+'元返'+template.judgeNull(item.coupon_price).toFixed(1)+'元红包';
          arr.push(fullSend);
        });

        html += '<script type="text/template" data-icon="i-fan">' + arr.join(';') +'<span class="special">(手机客户端专享)</span></script>';
      }
      return html;
    },

    //随机红包
    randomCoupon: function(data){
      var html = '';
      if(data.actInfoVo && data.actInfoVo.random_red_package_enjoyed){
        if (ICON_LEN < 7) {
          ICON_LEN++;
          html += '<i class="icon i-fan"></i>';
        }
        html += '<script type="text/template" data-icon="i-fan">下单并选择在线支付立返最高' + template.judgeNull(data.actInfoVo.random_red_package_logo.max).toFixed(1) + '元手机APP专用支付红包<span class="special">(手机客户端专享)</span></script>';
      }
      return html;
    },

    //是否收藏商家
    collection: function(data){
      var html = '';
      if(data.favorite_restaurant_flag && data.favorite_restaurant_flag=='YES'){
        html = '<a href="javascript:;" class="favorite j-save-up" data-poiid="' + template.judgeNull(data.wm_poi_id_str) + '" title="取消收藏">\
                    <i class="icon i-poi-fav2"></i>\
                </a>';
      } else {
        html = '<a href="javascript:;" class="un-favorite j-save-up" data-poiid="' + template.judgeNull(data.wm_poi_id_str) + '" title="收藏商家">\
                    <i class="icon i-poi-fav1"></i>\
                </a>';
      }
      return html;
    },

    actInfoVos: function(data) {
        var html='',
            actInfoVos = data.actInfoVos;

        if(actInfoVos.length > 0) {
            for(var i = 0; i<actInfoVos.length;i++) {
               html += '<i class="icon" style="width:17px;height:17px;background:none;">'+
                           '<img src="'+ actInfoVos[i].iconUrl +'" style="display:block;width:100%;"/>'+
                      '</i>' +
                       '<script type="text/template">'+
                          '<i class="icon" style="width:17px;height:17px;margin:0 10px 0 -28px;background:none;">'+
                             '<img src="'+ actInfoVos[i].iconUrl +'" style="display:block;width:100%;"/>'+
                          '</i>' +
                          actInfoVos[i].text +
                          '<span class="special">(手机客户端专享)</span>'+
                       '</script>';
            }
        }
        return html;
    },

    //主dom结构
    main: function(data,hasmore){
      var html = '',
          restMask = '';
      var split = '<li class="rest-separate j-rest-separate"></li>';
      var noData = '<div class="no-rests"><div class="tip borderradius-2">没有找到符合条件的商家，换个姿势再试一次？</div></div>';
      for (var i = 0; i < data.length; i++) {
        restMask = data[i].wmPoi4Web.status==3 ? ' rest-mask' : '';
        html += '<li class="fl rest-li" >\
                   <div class="j-rest-outer rest-outer transition' + restMask + '">\
                      <div data-title="' + template.judgeNull(data[i].wmPoi4Web.name) + '" data-bulletin="'+ template.judgeNull(data[i].wmPoi4Web.bulletin)
                        + '" data-poiid="' + template.judgeNull(data[i].wm_poi_id_str) + '" class="restaurant" data-all="1"'
                        + this.loopTag(data[i].classify_tagset) + ' data-minpricelevel="' + template.judgeNull(data[i].min_price_level) + '">\
                        <a class="rest-atag" href="/restaurant/' + data[i].wm_poi_id_str + '" data-pos="' + i + '" target="_blank">\
                          <div class="top-content">\
                            ' + this.preview(data[i].wmPoi4Web,i) + '\
                            ' + this.content(data[i]) + '\
                             <div class="clear"></div>\
                          </div>\
                          <div class="others" style="display:none;">\
                             <div class="discount">'
                             + this.logistic(data[i])
                             + this.onlinePay(data[i])
                          //   + this.coupon(data[i])
                           ///  + this.sendCoupon(data[i])
                             + this.supportInvoice(data[i])
                          //   + this.fullDonation(data[i])
                          //   + this.firstOrder(data[i])
                         //    + this.fullDiscount(data[i])
                         //    + this.overTime(data[i])
                         //    + this.aheadDiscount(data[i])
                         //    + this.couponDiscount(data[i])
                             + this.supportCoupon(data[i])
                             + this.actInfoVos(data[i])
                         //    + this.mealsDonation(data[i])
                         //    + this.specialMeal(data[i])
                            // + this.fullSendCoupon(data[i])
                           //  + this.randomCoupon(data[i])
                             +'</div>\
                          </div>'
                          + this.collection(data[i]) +
                        '</a>\
                      </div>\
                    </div>\
                  </li>';

        if((i%4)==3 && i!=(data.length-1)) {html += split;}
        ICON_LEN = 0;
      }
      if(data.length == 0) {
        DOMS.restList.html(noData);
        return false;
      } else {
        if(hasmore) {
          html += '<li class="rest-separate j-rest-separate loading" id="loading"><div class="isloading">点击加载更多商家</div></li>';
        } else {
          html += '<li class="rest-separate j-rest-separate"><div class="isloading" style="color:#707070;">扫描左下角二维码查看更多商家</div></li>';
        }
        return html;
      }
    }
  };

  //获取商家列表
  var restaurants = {
    /**
     * @function request
     * @description 获取商家列表
     */
    request: function(restart){
      PARAM.classify_type = CLASSIFY.join('|');
      PARAM.uuid = Cookie.get('w_uuid');
      PARAM.platform = 1;
      PARAM.partner = 4;
      PARAM.originUrl = encodeURIComponent(window.location.href);

      var toCaledParams = '', index = 0;
      for (var i in PARAM) {
        toCaledParams += ((index == 0) ? '' : '&') + i + '=' + PARAM[i];
        index++;
      }
      var token = Rohr_Opt.reload('http://' + 'waimai.meituan.com/ajax/poilist?' + toCaledParams);
      console.log(token);
      $.ajax({
        url: 'http://waimai.meituan.com/ajax/poilist?_token=' + token,
        type: 'POST',
        dataType: 'json',
        data: PARAM
      })
      .done(function(res) {
        if (+res.code == 0) {
          HAS_MORE = res.data.hasMore;
          var html = template.main(res.data.poiList,HAS_MORE);
          PARAM.page_offset += PARAM.page_size;
          $('#loading').remove();
          if(restart && res.data.poiList.length){DOMS.restList.html('');}
          DOMS.restList.append(html).promise().done(function(){
            IS_LOADING = false;
            TIMER && clearTimeout(TIMER);
            TIMER = setTimeout(loading, 100);
          });
        } else if (+res.code === 406) {
          if (res.customData && res.customData.verifyPageUrl && /^https?:\/\//.test(res.customData.verifyPageUrl)) {
            var verifyUrl = res.customData.verifyPageUrl;
            if (verifyUrl.indexOf('?') > -1) {
              verifyUrl += '&';
            } else {
              verifyUrl += '?';
            }
            verifyUrl += 'uuid=' + Cookie.get('w_uuid') + '&platform=1&partner=4&theme=waimai';
            window.location.href = verifyUrl;
          }
        } else {
          alert(res.msg);
        }
      });
    },

    //滚动加载
    scrollLoad: function(){
      // 如果没有更多的数据的话，返回空
      if(!FIRST_HAS_MORE) return;
      var me = $(this);
      // 删除点击加载更多那行
      me.remove();
      var isLoading = '加载更多中...';
      if(HAS_MORE && !IS_LOADING){
        IS_LOADING = true;
        $('#loading').find('div').text(isLoading);

        // cate改动
        var currentUrl = window.location.href;
        var urlPieces = currentUrl.split('-');
        var cate;
        if (urlPieces.length === 1) {
          cate = 'cate_all';
        } else {
          cate = urlPieces[1];
        }
        CLASSIFY.length = 0;
        CLASSIFY.push(cate);
        restaurants.request(false);
      }
    },

    /**
     * @function listener
     * @description 商家节点上事件监听
     */
    listener: function(){
      //商家分类
     /*
      DOMS.cateFilter.on('click', function() {
        var self = $(this),
            parent = self.parent(),
            cate = self.data('cate'),
            activeCate = $('.imgsort-content .selected').find('a').data('cate');

        PARAM.page_offset = 1;
        FIRST_HAS_MORE = true;
        CLASSIFY = utils.popArray(activeCate, CLASSIFY);
        CLASSIFY.push(cate);
        parent.addClass('selected').siblings().removeClass('selected');
        restaurants.request(true);
      });
     */

      //优惠筛选
      DOMS.restFilter.on('click', function() {
        var self     = $(this),
            rest     = self.data('rest'),
            checkbox = self.find('.checkbox'),
            checked  = checkbox.hasClass('checked');

        PARAM.page_offset = 1;
        FIRST_HAS_MORE = true;
        switch (rest) {
          case 'online_pay':
            PARAM.support_online_pay = checked ? 0 : 1;
            break;
          case 'logistic':
            PARAM.support_logistic = checked ? 0 : 1;
            break;
          case 'invoice':
            PARAM.support_invoice = checked ? 0 : 1;
            break;
          default:
            if(!checked){
              CLASSIFY.push(rest);
            } else {
              CLASSIFY = utils.popArray(rest, CLASSIFY);
            }
        }
        restaurants.request(true);
        checked ? checkbox.removeClass('checked') : checkbox.addClass('checked');
      });

      //排序筛选
      DOMS.sortFilter.on('click', function() {
        var self = $(this),
            sort = self.data('sort');

        PARAM.page_offset = 1;
        FIRST_HAS_MORE = true;
        self.addClass('active').siblings().removeClass('active');
        PARAM.sort_type = sort;
        restaurants.request(true);
      });

      //起送价筛选
      DOMS.priceFilter.on('click', function() {
        var self = $(this),
            price = self.data('price');

        PARAM.page_offset = 1;
        FIRST_HAS_MORE = true;
        self.parents('.prices').removeClass('hover');
        DOMS.priceBox.text(self.text());
        PARAM.price_type = price;
        restaurants.request(true);
      });

      //滚动加载
      //DOMS.container.on('click','.loading',this.scrollLoad);
      //   点击加载更多商家后执行这个函数
      $("body").on('click','#loading',this.scrollLoad);
    }
  };

  /**
   * @function init
   * @description 全局初始化
   */
  var init = function(){
    //restaurants.request(false);
    //   开启监听
    restaurants.listener();
  };
  init();
    console.log('');
});
