// 定义一个空对象用来和服务器通信
var api = {}

/*
给对象添加一个 ajax 方法
*/
api.ajax = function(url, method, form, callback) {
  // 生成一个请求
  var request = {
    url: url,
    type: method,
    data: form,
    success: function(response){
        var r = JSON.parse(response)
        callback(r)
    },
    error: function(error){
      log('网络错误', error)
      var r = {
        'success': false,
        message: '网络错误'
      }
      callback(r)
    }
  }
  $.ajax(request)
}

// api 内部函数，发一个 get 请求
api.get = function(url, response) {
    //  get 函数不需要传递 form 参数
    api.ajax(url, 'get', {}, response)
}

/*
api 内部函数，发一个 post 请求
*/
api.post = function(url, form, response) {
    api.ajax(url, 'post', form, response)
}

// ====================
// 以上是内部函数，内部使用
// --------------------
// 以下是功能函数，外部使用
// ====================

// user API
api.userRegister = function(form, response) {
    var url = '/api/user/register'
    api.post(url, form, response)
}
// --------------------
// weibo API
api.weiboAdd = function(form, response) {
    var url = '/api/weibo/add'
    api.post(url, form, response)
}

api.weiboDelete = function(weiboId, response) {
    var url = '/api/weibo/delete/' + weiboId
    var form = {}
    api.get(url, response)
}

// 评论 API

// 用户 API
