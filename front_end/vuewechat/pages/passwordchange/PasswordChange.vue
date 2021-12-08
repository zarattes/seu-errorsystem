<template>
	<view class="background">
	<view class="box">
		<view class="textDis">
			<text>修改密码</text>
		</view>
		<view class="textDis1">
			<text>在此页中，您可以修改您的登陆密码（注意：密码格式为8-12位且带有字母和数字）</text>
		</view>
	<view class="whiteBack">
		<view class="content-wrapper">
			<view class="login-form">
				<view class="login-form-items">
					<view class="login-form-items-title">新密码</view>
					<input v-model="password" type="password" class="login-input" placeholder="请输入新密码" maxlength="12" placeholder-class="ph"/>
				</view>
	
				<view class="login-form-items">
					<view class="login-form-items-title">密码确认</view>
					<input v-model="passwordconfirm" type="password" class="login-input" placeholder="重新输入密码" maxlength="12" placeholder-class="ph"/>
				</view>
			</view>
		</view>
		<div class="submit-wrapper">
			<button class="btn" @click="trans">确认修改</button>
		</div>
	</view>
	</view>
	</view>
</template>

<script>
	function checkPassword(password)
	{
		console.log(password);
		var reg = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,12}$/;
		if (!reg.test(password) || password.length < 8 ||password.length > 12) return false;
		else return true;
	}
	export default {
		data() {
			return {
				password: '',
				passwordconfirm: ''
			};
		},
		onLoad() {
			uni.showModal({
				title:"密码修改",
				content:"密码需包含字母和数字，长度限制在8-12位",
				showCancel:false
			})
		},
		methods: {
			trans() {
				if(!checkPassword(this.password)) uni.showToast({
					title:"请输入正确格式的密码(需同时包含字母数字)",
					icon:"none"
				})
				else if(this.password!=this.passwordconfirm) uni.showToast({
					title:"两次密码不同，请检查",
					icon:"none"
				})
				else{
					uni.request({
						url: getApp().globalData.yuming + "/updateUserPassword",
						method: "POST",
						header: {
							'content-type':'application/x-www-form-urlencoded'
						},
						data: {
							'card_id':this.$store.state.card_id,
							'password':this.password
						},
						success: (res) => {
							console.log(res);
							if (res.statusCode === 200) {
								uni.showToast({
									title:"修改密码成功",
									icon:"none"
								});
								setTimeout(function() {
									uni.reLaunch({
										url:"../denglu/denglu"
									})
								}, 1000);
							} else {
								reject('获取信息失败');
							}
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
	page {
		background-color: #f0f0f0;
	}
	.textDis {
		font-size: 50rpx;
		font-weight: 900;
		color: #ffffff;
		padding-bottom: 20px;
	}
	.textDis1 {
		font-size: 30rpx;
		color: #ffffff;
		padding-bottom: 20px;
	}
	.box{
		margin: 0px 5% 0px 5%;
	}
	.content-wrapper {
		width: 100%;
	}
	
	.title {
		margin-top: 35rpx;
		width: 100%;
		margin-bottom: 10px;
	}
	
	.whiteBack{
		background-color: #ffffff;
		opacity: 0.9;
		border-radius: 10px;
	}
	
	.login-form {
		margin: 20px 10px 20px 15px;
		opacity: 0.8;
	}
	
	.login-form-items {
		padding: 15px 10px;
		border-bottom: 1px solid;
		position: relative;
		display: -webkit-flex;
		display: flex;
		font-family: "楷体", "楷体_GB2312";
	}
	
	.login-form-items-title {
		width: 30%;
		line-height: 22px;
		height: 22px;
		flex-shrink: 0;
	}
	
	.login-input {
		width: 100%
	}
	.submit-wrapper {
		padding: 10px;
		padding-top: 10px;
	}
	.ph {
		font-family: "楷体", "楷体_GB2312";
	}
	.btn {
		width: 43%;
		color: #ffffff;
		background-color: #00aaff;
		font-family: "楷体", "楷体_GB2312";
	}
	.background {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		background: url(http://47.100.78.158:8080/img/static/background/bg8.png) no-repeat center top;
		background-size: 100%;
		background-attachment: fixed;
		z-index: -1;
	}
</style>
