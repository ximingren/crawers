/**
 * 向后台请求的接口列表。
 *
 * @date 2014.01.06
 */

define(function() {
  'use strict';

  var passportDomain = (window.MT && MT.ENV=='test') ?
      'passport.test.meituan.com' : 'passport.meituan.com';
  var locationOrigin = location.protocol+'//'+location.host;
  return {
    'locationOrigin' : locationOrigin, //模拟webkit浏览器中的location.origin

    // ---------- 账户操作相关 ------------ start
    // 登出
    'getLogout' : '/login/out',

    // 登录
    'getLogin' : '/login',

    // 获取手机验证码
    'getMobileVerify' : '/account/bind/captcha',

    // 绑定手机号
    'bindMobile' : '/account/bind/verifycaptcha',

    // 修改用户名
    'reName' : '/account/ajax/resetaccount',

    // 修改密码接口
    'changePassword' : '/account/ajax/resetaccount',

    // 验证用户是否登录
    'verifyLogin' : '/account/islogin',

    // 验证手机号的登录
    'verifyPhone' : '/account/isbindphone',

    // 获得登录url
    'loginUrl' : 'http://'+passportDomain+'/account/unitivelogin?service=waimai&continue='+encodeURIComponent(locationOrigin+'/account/settoken'),

    // 获得注册url
    'registerUrl' : 'http://'+passportDomain+'/account/unitivesignup?service=waimai&continue='+encodeURIComponent(locationOrigin+'/account/settoken'),

    // 获得登录url
    'logoutUrl' : 'http://'+passportDomain+'/account/unitivelogout?service=waimai&continue='+encodeURIComponent(locationOrigin+'/account/logout'),

    // 登录弹框的js
    'loginDlgJs' : 'http://'+passportDomain+'/account/fetchunitiveloginscript',

    // ---------- 账户操作相关 ------------ end

    // 全局搜索 ajax接口
    'searchAll' : '/search/ajax/rtofd',

    // 收藏店铺 ajax接口
    'favoriteRest' : '/ajax/favorite/restaurant',
    // 取消收藏店铺 ajax接口
    'unfavoriteRest' : '/ajax/favorite/restaurant_del',

    // 搜索 菜品结果 购买按钮埋点ajax接口
    'searchFoodBuy' : '/search/log/logClickFoodBuy',

    // 下单过程中获取手机验证码接口
    'getSMSCode' : '/ajax/order/getsmscode',

    // 获取抽奖号码
    'getLottery' : '/lottery/ajax/participate',

    // 发送反馈信息
    // （登录）
    'sendFeedbackL' : '/help/feedback',
    // （未登录）
    'sendFeedback' : '/help/nologin/feedback',

    // 商务合作
    'getCooperate': '/help/ajax/cooperate',

    // 斑马合作
    'getBanmaCooperate': '/help/ajax/banma',

    //代理商加盟
    'postAgentJoin': '/help/ajax/agent',

    // 获取位置信息
    'getDistrict' : '/point',

    // 发送邮箱和当前您所在的城市信息
    'sendEmail' : '/city/wish',

    // 提交订单接口
    'submitOrder' : '/order/submit',

    // 页面日志请求地址
    'setLog' : '/help/ajax/__.gif',

    // 新增地址接口（包括了对地址的增删改查等操作）
    'editAddress' : '/customer/hisaddr/ajax/edit',

    // 食品评价接口
    'commentFood' : '/comment/food',

    // 获取某家门店的所有评论信息
    'getComments' : '/ajax/comment',

    // 评价某一次订单的体验信息
    'commentOrder' : '/comment',

    // 确定订单消息
    'orderConfirm' : '/order/confirm',

    // 是否可以首单立减
    // 'isFirstReduce' : '/node/order/act/canFst',
    'isFirstReduce' : '/ajax/order/getFstOrderActInfo',

    // 获取当前手机号对对应的优惠券
    'getCurrentTickets' : '/ajax/order/getUserCouponList',

    // 使用抵价券
    'useCoupon': '/order/act/usecoupon',

    // 更新购物车的信息
    'updateCart': '/ajax/order/preview',

    // 获取订单当前的状态的接口
    'getOrderStatus' : '/ajax/order/getstatus',

    // 取消订单的接口
    'cancelOrder' : '/ajax/order/cancel',

    // 自动提示的文案
    'buildSuggest' : '/build/suggest/wmpoi',

    // 获取手机动态码（用手机登录的过程中）
    'getPhoneCode' : '/login_d/captcha',

    // 发送举报
    'sendInform' : '/help/ajax/report/cheatingpoi',

    // 获取手机动态码（用手机注册的过程中）
    'getRegisterCode' : '/register/captcha',

    // 手机动态码登录
    'phoneCodeLogin' : '/login_d',

    // 用户新注册
    'userRegister' : '/register',

    // 检查支付状态
    'getPayStatus' : '/ajax/order/getpaystatus',

    //去支付
    'pay' : '/order/pay',

    //支付发送验证码
    'paySendSms' : '/order/pay/resendsmscode',

    // 获取当前城市信息
    'getCityInfo' : '/ajax/city/entrance_info/city_id',

    // 根据了某个坐标点，获取当前坐标的蜂窝信息（批量获取蜂窝的信息）
    'getRestInfo' : '/ajax/location/info',

    'getBatchRestInfo' : '/ajax/location/batch/count/restaurant',

    // 增加语音验证的功能
    'voiceVerify' : '/ajax/order/getcallcode',

    // 删除某个发票的信息
    'deleteCheque' : '/ajax/invoice/del',

    // 满减升级接口（点击了在线支付按钮出发的事件）
    'fullMinusUpgrade' : '/order/act/addition/onlinepay',

    //黄条已阅
    'readTip' : '/help/tip/del',

    'getTip' : '/help/tip/get',

    'chargeDiscountPlus' : '/order/act/fstordersp/addition/onlinepay',

    // 套餐在线支付减优惠
    'packageOnline' : '/order/act/addition/onlinespecial',

    // 用户发起退款的申诉
    'refundAppeal' : '/order/refund/appeal/submit',

    // 取消退款
    'cancelRefund' : '/order/refund/apply/cancel/submit',

    //申请退款，订单页, 检查订单是否百胜锁定
    'applyRefund' : "/order/refund/apply/validate",

    // 取消退款申诉
    'cancelAppeal' : '/order/refund/appeal/cancel/submit',

    // 日志的统一接口
    'logger' : '/log',

    // 在购买过的页面点击餐厅，加上统计 /ajax/poiByOrder/{poiId}
    'homeOrderedLog' : '/ajax/poiByOrder'
  };
});









