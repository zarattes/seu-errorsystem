<template>
	<view class="content">
		<view @click="login()" class="logo">点击登录</view> 
		<button type="primary" @click="onhuoqu()">获取</button>
	</view>
</template>

<script>
	import uniRequest from 'uni-request';
	import axios from 'axios';
	export default {
		data() {
			return {
				title: 'Hello'
			}
		},
		onLoad() {

		},
		methods: {
			login() {
				uniRequest.post('/login', {
					username: 'admin',
					password: '123456'
				}).then(function(res) {
					console.log(res.data.data);
					Lockr.set('authKey', res.data.data.authKey)
					Lockr.set('sessionId', res.data.data.sessionId)
				}).catch(function(error) {
					console.log(error);
				});
				
				 // axios.post('/login',{  
				 //  	username: 'admin',
				 //  	password: '123456'
				 //    }).then(function(res){
				 //        console.log(res.data.data);
				 //    }).catch(function (error) {
				 //        console.log(error);
				 //    });
			},
			onhuoqu() { 
				uniRequest.post('/index/index', {  
				}).then(function(res) {
					console.log(res);
				}).catch(function(err) {
					console.log(err);
				});
				
				// axios.post('/index/index', { 
				// }).then(function(res) {
				// 	console.log(res); 
				// }).catch(function(err) {
				// 	console.log(err);
				// });
			}
		}
	}
</script>

<style>
	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.logo {
		height: 200rpx;
		width: 750rpx; 
		display: flex;
		justify-content: center;
		margin-top: 200rpx;
	}

	.text-area {
		display: flex;
		justify-content: center;
	}

	.title {
		font-size: 36rpx;
		color: #8f8f94;
	}
</style>
