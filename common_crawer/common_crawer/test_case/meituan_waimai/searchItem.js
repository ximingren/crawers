// /**
//  * 搜索地图页的时候拼装模板
//  *
//  * @date 2014-08-06 星期三
//  *
//  */
//
// define(function () {
//     'use strict';
//
//     return '<div class="bd-info-box">' +
//         '  <div class="title"><%= title %></div>' +
//         '  <div class="addr">地址：<%= address %></div>' +
//         '  <% if(count != 0) { %><div class="nearby">附近有<span><%= count %></span>家外卖餐厅</div><% } %>' +
//         '  <div class="btn-group clearfix">' +
//         '    <% if(count != 0) { %>' +
//         '      <a class="borderradius-2 check-it fl" href="<%= url %>">开始订餐</a>' +
//         '    <% } else { %>' +
//         '      <a href="javascript:;" class="borderradius-2 no-cover fl">努力覆盖中...</a>' +
//         '      <% if (isPoiview) { %>' +
//         '        <a class="borderradius-2 check-covered fl" href="javascript:;" onclick="openPoi(1)">查看已覆盖地址</a>' +
//         '      <% } %>' +
//         '    <% } %></div>' +
//         '</div>';
// });
//


/**
 * 更新后的地图页面脚本文件（将初始化页面移除了地图的展示功能，并且改变了功能上的一些细节）
 *
 * @date 2015-02-10 星期二
 * @date 2016-12-29 modify module/general
 */

require.config({
  shim : {
    'lib/jquery/jscrollpane' : {
      deps : ['lib/jquery']
    },
    'lib/jquery/mousewheel' : {
      deps : ['lib/jquery']
    }
  },
  baseUrl : MT.STATIC_ROOT + '/js'
});


require(['lib/jquery', 'lib/jquery/cookie', 'lib/jquery/mousewheel', 'module/bridge', 'module/general', 'module/interface', 'module/map/mapnew', 'module/storage', 'util/request', 'util/utils'], function($, cookie, mousewheel, bridge, general, i, map, storage, request, utils) {
  'use strict';

  var jQcitylist = $('#citylist'), jQhistorylist = $('#historylist'), jQresult = $('#result'), jQsearchInput = $('#searchKeywords'), jQguider = $('#guider');
  var jQmap = $('#map'), jQbdmap = $('#bd-map');

  // 在IE6,7设置容器的高度，被ele.me代入坑中。
  var jQhtml = $('html');
  jQhtml.hasClass('ie7') && jQbdmap.height(jQmap.height());
  jQhtml.hasClass('ie6') && jQbdmap.height(500);

  var tmp = '';
  console.log(tmp);

  // 打开城市列表
  var listcityView = function(evt) {
    jQguider.find('.bg').removeClass('search');
    bridge.trigger('dialog:close-poi', evt);

    if ($('.dialog-citylist').size()) {
      return;
    }
    var self = $(this);
    require(['module/map/city'], function(city) {
      city.show(self);
    });
  };

  // 重新加载地图或者打开地标列表页
  var isPoiview = (jQcitylist.data('ispoi') == 2) ? true : false, poiData;

  bridge.register('isPoiview', isPoiview);
  var realodCity = function(cityData) {
    var cityid = cityData.cityid;
    if (!cityid) {
      return;
    }

    jQcitylist.find('span').text(cityData.real);
    jQresult.addClass('hidden');
    map.locateCity(cityData.real);
    map.clearOverlays();
    request.post(i.getCityInfo, {
      'city_id' : cityid
    }, function(ret) {
      if (ret.code == 0) {

        // 如果是地图页面
        if (ret.data == -1) {
          isPoiview = false;
          bridge.trigger('dialog:close-city');

        // 如果是poi地区列表页
        } else {
          isPoiview = true;
          poiData = ret.data;
          for (var j = 0; j < poiData.length; j++) {
            for (var k = 0; k < poiData[j].list.length; k++) {
              poiData[j].list[k].sub = utils.countChars(poiData[j].list[k].name, 22);
            }
          }
          require(['module/map/poi'], function(poi) {
            poi.show(jQcitylist, {
              data : poiData
            });
          });
        }
        bridge.register('isPoiview', isPoiview);
      } else {
        utils.showError(ret.msg);
      }
    }, 'json');
  };

  // 展示历史地址的列表
  var listHistory = function() {
    if ($('.dialog-historyaddr').size()) {
      return;
    }
    var self = $(this);
    require(['module/map/history'], function(history) {
      history.show(self);
    });
  };

  var closeTip = function() {
    jQguider.css('visibility', 'hidden');
    storage.set('guider', 0);
  };

  // 页面上开始搜索的功能
  var search = function(evt) {
    // $(".merchant-join").animate({
    //   opacity: 0
    // },700).css('display','none').remove();
    jQmap.css('bottom', '-160px');
    var keywords = jQsearchInput.val();
    if ($.trim(keywords).length == 0) {
      //utils.showError('请输入您的送餐地址！');
      return;
    }

    bridge.trigger('dialog:close-poi', evt);
    map.search(keywords, bridge.get('city') || '北京');
  };

  // 增加和删除over的类
  var addOverClass = function() {
    $(this).addClass('over');
  };

  var leaveOverClass = function() {
    $(this).removeClass('over');
  };

  // 改变头部的提示框的信息
  var changeBanner = function() {
    jQguider.find('.bg').addClass('search');
  }

  // 打开信息展示的弹框
  var openInfo = function() {
    var self = $(this);
    jQresult.find('li.active').removeClass('active');
    self.addClass('active');

    var link = '/geo/geohash?lat=' + self.data('lat') + '&lng=' + self.data('lng') + '&addr=' + encodeURI(encodeURI(self.find('.title').text())) + '&from=m';
    var infoBoxHTML = '<div class="bd-info-box">' + self.find('.content').html() +
        '<div class="btn-group clearfix">';

    // 判断附近是否有餐厅
    if (self.find('.nearby').size() == 0) {
      infoBoxHTML += '<a href="javascript:;" class="borderradius-2 no-cover fl">努力覆盖中...</a>';
      if (isPoiview) {
        infoBoxHTML += '<a class="borderradius-2 check-covered fl" href="javascript:;" onclick="openPoi(1)">查看已覆盖地址</a>';
      }
    } else {
      infoBoxHTML += '<a class="borderradius-2 fl" href="' + link + '">立即订餐</a>';
    }
    infoBoxHTML += '</div></div>';
    map.openInfo(self.data('index'), infoBoxHTML);
  };

  // 搜索结果页面的跳转
  var gotoPage = function(evt) {
    map.gotoPage($(this).data('page'));
  };

  // 按下回车的时候进行的搜索功能
  var keydownSearch = function(evt) {
    // $(".merchant-join").css({
    //   opacity: 0,
    //   display:'none'
    // });
    if (evt.which == 13) {
      search(evt);
    }
  };

  // 打开Poi列表，在且仅在用户处于地标页的时候
  var openPoi = function(isHide) {
    if (poiData) {
      require(['module/map/poi'], function(poi) {
        poi.show(jQcitylist, {
          data : poiData
        });
      });
    } else {
      request.post(i.getCityInfo, {
        'city_id' : jQcitylist.data('cid')
      }, function(ret) {
        if (ret.code == 0) {
          poiData = ret.data;
          for (var j = 0; j < poiData.length; j++) {
            for (var k = 0; k < poiData[j].list.length; k++) {
              poiData[j].list[k].sub = utils.countChars(poiData[j].list[k].name, 22);
            }
          }

          require(['module/map/poi'], function(poi) {
            poi.show(jQcitylist, {
              data : poiData
            });
          });
        } else {
          utils.showError(ret.msg);
        }
      }, 'json');
    }

    // isHide && map.clearOverlays();
  };
  // 比较恶心的写法，百度地图内部元素事件绑定
  window.openPoi = openPoi

  // 当改变了窗口大小的时候，重新加载页面
  var resizeTimer;
  var reloadDocument = function() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function() {

      // 修改原来简单粗暴的搜索逻辑
      // location.reload();
      bridge.trigger('dialog:close-city');
      bridge.trigger('dialog:close-poi');
      bridge.trigger('dialog:close-history');
      jQresult.height(jQbdmap.height());
    }, 500);
  };

  // var blurFun = function() {
  //   var height = $("#result").height();
  //   if(height > 1) {
  //     $(".merchant-join").css({
  //       opacity: 1,
  //       display:'block'
  //     });
  //   } else {
  //     return false;
  //   }
  // };

  var bindEvt = function() {
    jQcitylist.click(listcityView);
    jQhistorylist.click(listHistory);
    jQsearchInput.keydown(keydownSearch);
    // jQsearchInput.blur(blurFun);
    $(window).resize(reloadDocument);

    $('#search').click(search);
    $('#tipclose').click(closeTip);
    jQresult.delegate('.field', 'mouseenter', addOverClass)
            .delegate('.field', 'mouseleave', leaveOverClass)
            .delegate('.field', 'click', openInfo)
            .delegate('.pager a', 'click', gotoPage);
    jQresult.delegate('.check-covered', 'click', openPoi);

    jQsearchInput.focus(changeBanner);

    bridge.register('map:reloadCity', realodCity);
  };

  var setPOIPageView = function() {
    LXPV('c_9le3i2l', function(valLab) {
      return null;
    });
  };

  bindEvt();
  setPOIPageView(); // 发送pv

  if (storage.get('guider') != 0) {
    jQguider.css('visibility', 'visible');
  }
});
