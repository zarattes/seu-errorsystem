<template>
	<view class="background">
		<view class="box">
			<view class="textDis">
				<text>{{admin}}，你好！</text>
			</view>
			<view class="textDis1">
				<text>欢迎来到「大数据中心报障系统」</text>
			</view>
			<view style="background-color: #ffffff;border-radius: 10px;opacity: 0.9;">
				<view class="allicon">
					<view class="icon1" @click="goToindex()">
						<image class="image" src="http://47.100.78.158:8080/img/static/icon2.png"></image>
						<text class="text">查看故障</text>
					</view>
				</view>
				<view class="allicon">
					<view class="icon" @click="goToClass()">
						<image class="image" src="http://47.100.78.158:8080/img/static/icon3.png"></image>
						<text class="text">故障分类管理</text>
					</view>
					<view class="icon" @click="goToAdvice()">
						<image class="image" src="http://47.100.78.158:8080/img/static/icon1.png"></image>
						<text class="text">查看建议</text>
					</view>
				</view>
				<view class="allicon">
					<view class="icon1" @click="goToSelfinfo()">
						<image class="image" src="http://47.100.78.158:8080/img/static/icon4.png"></image>
						<text class="text">个人信息</text>
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
				admin:""
			};
		},
		onLoad() {
			uni.request({
				url: this.$store.state.yuming + "/getUserInformation",
				method: "GET",
				header: {
					'token': this.$store.state.token
				},
				data: {
					'card_id': this.$store.state.card_id,
				},
				success: (res) => {
					this.admin = res.data.data.name;
				},
				error: function(e) {
					this.$message.error(err);
				}
			})
		},
		methods: {
			goToindex() {
				uni.navigateTo({
					url: "../manage-index/manage-index"
				})
			},
			goToClass() {
				uni.navigateTo({
					url: "../manage-class/manage-class"
				})
			},
			goToAdvice() {
				uni.navigateTo({
					url: "../manage-advice/manage-advice"
				})
			},
			goToSelfinfo(){
				uni.navigateTo({
					url: "../admin-selfinfo/admin-selfinfo"
				})
			}
		}
	}
</script>

<style>
	page {
		background-color: #f0f0f0;
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

	.box {
		margin: 20px 5% 20px 5%;
	}

	.allicon {
		display: flex;
		justify-content: space-around;
		text-align: center;
	}

	.icon {
		width: 40%;
		height: 300rpx;
		background-color: #f7f7f7;
		display: flex;
		flex-direction: column;
		margin: 10px;
	}

	.icon1 {
		width: 90%;
		height: 300rpx;
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
</style>
