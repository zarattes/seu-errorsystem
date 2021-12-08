import Vue from 'vue'
import App from './App'

Vue.config.productionTip = false



import uniRequest from 'uni-request';
uniRequest.defaults.withCredentials=true;//让请求头携带参数cookie
uniRequest.defaults.baseURL = 'http://xxxxxxxxxxxxx/';      //配置接口地址  
uniRequest.defaults.headers.authKey = Lockr.get('authKey');
uniRequest.defaults.headers.sessionId = Lockr.get('sessionId');
uniRequest.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';
console.log(Lockr.get('authKey'))
console.log(Lockr.get('sessionId'))

//引入Lockr存储插件
import Lockr from 'lockr'; //本地存储插件 
window.Lockr = Lockr; //使用本地存储插件

//axios
import axios from 'axios';
Vue.prototype.$axios = axios; 
axios.defaults.timeout = 5000;   //响应时间
axios.defaults.withCredentials=true;//让请求头携带参数cookie
axios.defaults.baseURL = 'http://xxxxxxxxxxxx/';   //配置接口地址  
axios.defaults.headers.authKey = Lockr.get('authKey');
axios.defaults.headers.sessionId =Lockr.get('sessionId'); 
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';        //配置请求头


App.mpType = 'app'

const app = new Vue({
	...App
})
app.$mount()
