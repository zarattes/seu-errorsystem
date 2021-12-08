<template>
	<view class="background">
		<view class="box">
			<view class="textDis">
				<text>{{User}},你好！</text>
			</view>
			<view class="textDis1">
				<text>欢迎来到「大数据中心报障系统」</text>
			</view>
			<view style="background-color: #ffffff;border-radius: 10px;opacity: 0.9">
				<view class="allicon">
					<view class="icon1" @click="goToindex()">
						<image  class="image" src="http://47.100.78.158:8080/img/static/Usericon/shouye.png" ></image>
						<text class="text">报障</text>
					</view>
				</view>
				<view class="allicon">
					<view class="icon" @click="goTomyque()">
						<image  class="image" src="http://47.100.78.158:8080/img/static/Usericon/question.png" ></image>
						<text class="text">我的问题</text>
					</view>
					<view class="icon" @click="goToselfInfo()">
						<image  class="image" src="http://47.100.78.158:8080/img/static/Usericon/info.png" ></image>
						<text class="text">个人信息</text>
					</view>
				</view>
				<view class="allicon">
					<view class="icon" @click="showMessage()">
						<image  class="image" src="http://47.100.78.158:8080/img/static/Usericon/time.png" ></image>
						<text class="text">机时查询</text>
					</view>
					<view class="icon" @click="showMessage()">
						<image  class="image" src="http://47.100.78.158:8080/img/static/Usericon/money.png" ></image>
						<text class="text">费用查询</text>
					</view>
				</view>
				<view class="allicon">
					<view class="icon1" @click="goTomessage()">
						<image  class="image" src="http://47.100.78.158:8080/img/static/Usericon/advice.png" ></image>
						<text class="text">建议反馈</text>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data(){
			return{
				User:""
			};
		},
		onLoad() {
			uni.request({
				url: getApp().globalData.yuming + "/getUserInformation",
				method: "GET",
				header: {
					'token': this.$store.state.token
				},
				data: {
					'card_id': this.$store.state.card_id,
				},
				success: (res) => {
					this.User = res.data.data.name;
				},
				error: function(e) {
					this.$message.error(err);
				}
			})
		},
		methods:{
			goToindex(){
				uni.navigateTo({
					url:"../index/index"
				})
			},
			goTomyque(){
				uni.navigateTo({
					url:"../myque/myque"
				})
			},
			goToselfInfo(){
				uni.navigateTo({
					url:"../selfInfo/selfInfo"
				})
			},
			goTomessage(){
				uni.navigateTo({
					url:"../message/message"
				})
			},
			showMessage(){
				uni.showToast({
					title:"敬请期待",
					icon:"none"
				})
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
	.allicon{
		display: flex;
		justify-content: space-around;
	}
	.icon {
		width: 40%;
		height: 250rpx;
		background-color: #f7f7f7;
		display: flex;
		flex-direction: column;
		margin: 10px;
	}
	.icon1 {
		width: 90%;
		height: 250rpx;
		background-color: #f7f7f7;
		display: flex;
		flex-direction: column;
		margin: 10px;
	}
	.image {
		width: 200rpx;
		height: 200rpx;
		margin: auto;
	}
	.text {
		margin: auto;
		font-size: 35rpx;
		font-family: SimHei;
	}
	.box {
		margin: 0px 5% 0px 5%;
	}
</style>
