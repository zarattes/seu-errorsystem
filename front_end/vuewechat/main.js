import Vue from 'vue'
import App from './App'
import axios from 'axios'
import store from './store'
//axios赋值给变量http		将axios挂到vue原型上
Vue.prototype.$axios = axios
Vue.prototype.$store = store

Vue.config.productionTip = false

App.mpType = 'app'
const app = new Vue({
	...App,
	store
})
app.$mount()

/*new Vue({
	store,
	render: h => h(App),
}).$mount('#app')*/


axios.interceptors.request.use(
	config => {
		if (store.state.token) { // 判断是否存在token，如果存在的话，则每个http header都加上token
			config.headers.token = `${store.state.token}`;
		}
		return config;
	},
	err => {
		return Promise.reject(err);
	});
//跳转后返回顶部
/*router.afterEach((to, from, next) => {
	window.scrollTo(0, 0);
});*/
axios.interceptors.response.use(function(response) { //token过期（12小时） code==9 token无效
	if (response.data.code === 9) {
		store.commit("clearCache"); // 删除已经失效或过期的token（不删除也可以，因为登录后覆盖）    
		Message("登陆已过期")
		uni.navigateTo({
			url: 'pages/denglu/denglu'
		}); // 到登录页重新获取token 
		/*router.replace({
		  path: ''    
		})*/
	} else if (response.headers.token) { // 判断token是否存在，如果存在说明需要更新token    
		store.commit('token', response.headers.token) // 覆盖原来的token(默认一天刷新一次)
		sessionStorage.setItem('token', response.headers.token)
	}
	return response
}, function(error) {
	return Promise.reject(error)
})
