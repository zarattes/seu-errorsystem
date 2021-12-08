<template>
	<view class="background">
		<view class="logo">
			<image src="http://47.100.78.158:8080/img/static/xiaohui.png" class="logo-display"></image>
		</view>
		<view class="content-wrapper">
			<view class="login-form">
				<view class="login-form-items">
					<view class="login-form-items-title">一卡通号</view>
					<input v-model="card_id" type="text" class="login-input" placeholder="请输入一卡通号"
						placeholder-class="ph" maxlength="9">
				</view>

				<view class="login-form-items">
					<view class="login-form-items-title">密码</view>
					<input v-model="password" type="password" class="login-input" placeholder="请输入密码"
						placeholder-class="ph">
				</view>
			</view>
		</view>
		<view class="findPw">
			<text style="text-align: left;width: 50%;" @click="register">注册账号</text>
			<text style="text-align: right;width: 50%;" @click="findPassWord">忘记密码</text>
		</view>
		<view style="display: flex;">
			<button size="default" class="btn" @click="trans">登录</button>
		</view>
	</view>
</template>

<script>
	import store from '@/store/index.js'
	export default {
		data() {
			return {
				card_id: '',
				password: ''
			};
		},
		methods: {
			register() {
				uni.navigateTo({
					url: "../register/register"
				});
				console.log("注册")
			},
			trans() {
				uni.request({
					url: getApp().globalData.yuming + "/login",
					method: "POST",
					header: {
						'content-type': 'application/x-www-form-urlencoded'
					},
					data: {
						'card_id': this.card_id,
						'password': this.password
					},
					success: (res) => {
						if (res.statusCode === 200) {
							uni.setStorageSync("token", res.data.token);
							store.commit("token", res.data.token);
							store.commit("card_id", this.card_id);
							store.commit("firstLogin", res.data.firstLogin);
							store.commit("role", res.data.identity);
							store.commit("roleHasLoad", true);
							/*if (this.$store.state.firstLogin == 1) {
							if (this.$store.state.firstLogin == 0) {
								uni.redirectTo({
									url: "../passwordchange/PasswordChange"
								});
							} else {*/
							if (this.$store.state.role == 0) {
								uni.redirectTo({
									url: "../Users/user"
								})
							} else if (this.$store.state.role > 0) {
								uni.redirectTo({
									url: "../admin/admin"
								});
								//}
							}
						} else {
							reject('登录失败');
							uni.showToast({
								title: "请检查你的用户名或密码是否正确",
								icon: "none"
							})
						}
					},
					error: function(e) {
						this.$message.error(err);
					}
				})
			},
			findPassWord() {
				if (this.card_id == "") uni.showToast({
					title: "请输入需要找回密码的一卡通号",
					icon: "none"
				})
				else {
					uni.request({
						url: getApp().globalData.yuming + "/retrievePassword",
						method: "GET",
						header: {},
						data: {
							'card_id': this.card_id,
							'email': this.card_id + "@seu.edu.cn"
						},
						success: (res) => {
							console.log(res);
							uni.showToast({
								title: "请登陆邮箱进行密码找回",
								icon: "none"
							})
						},
						error: function(e) {
							this.$message.error(err);
						}
					})
				}
			}
		}
	}
</script>

<style>
	.logo {
		align-items: center;
		text-align: center;
	}

	.logo-display {
		width: 150px;
		height: 120px;
	}

	.content-wrapper {
		width: 100%;
	}

	.login-form {
		margin: 0px 10px 10px 15px;
		background: #FFFFFF;
		opacity: 0.8;
	}

	.login-form-items {
		padding: 15px 10px;
		border-bottom: 1px solid #F3F4F5;
		position: relative;
		display: -webkit-flex;
		display: flex;
	}

	.login-form-items-title {
		width: 30%;
		line-height: 22px;
		height: 22px;
		flex-shrink: 0;
		text-align: center;
	}

	.login-input {
		width: 100%
	}

	.submit-wrapper {
		padding: 10px;
		padding-top: 10px;
		display: flex;
	}

	.btn {
		width: 60%;
		color: #ffffff;
		background-color: #00aaff;
		margin-top: 10px;
	}

	.findPw {
		display: flex;
		padding: 10px 20px 20px 25px;
		color: #00aaff;
	}
	.background {
		position: absolute;
		top: calc(15vh);
		left: 0;
		width: 100%;
		background-size: 100%;
		background-attachment: fixed;
		z-index: -1;
	}
</style>
