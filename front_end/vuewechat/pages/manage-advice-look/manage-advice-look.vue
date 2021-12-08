<template>
	<view class="background">
		<view class="box">
			<view>
				<view class="content"><text>建议详情</text></view>
				<view style="padding-left: 10px;padding-bottom: 10px;"><text class="Info">建议人邮箱 {{dataList.user_email}}</text></view>
				<view style="padding-left: 10px;padding-bottom: 10px;"><text class="Info2">建议描述 {{dataList.advice}}</text></view>
				<view style="padding-left: 10px;padding-bottom: 10px;"><text class="idAndTime">提交时间 {{happenTimeFun(dataList.create_time)}}</text></view>
			</view>
			<view v-for="(item,index) in dataList.url" :key="index" style="padding-bottom: 5px;">
				<image :src="item"></image>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				id: "",
				dataList: {
					user_email: "",
					create_time: "",
					user_id: "",
					advice: "",
					id: "",
					url:[],
				},
			}
		},
		//第一次进页面时加载这个建议的相关资料
		onLoad: function(option) {
			this.id = JSON.parse(option.id);
			console.log(this.id);
			uni.request({
				url: this.$store.state.yuming + "/admin/getAdvice",
				method: "GET",
				header: {
					'token': this.$store.state.token
				},
				data: {
					'id': this.id,
				},
				success: (res) => {
					if (res.statusCode === 200) {
						this.dataList = res.data.data;
					} else {
						reject('获取信息失败');
					}
				},
				error: function(e) {
					this.$message.error(err);
				}
			});
		},
		methods: {
			happenTimeFun(num) { //时间戳数据处理
				let date = new Date(num);
				//时间戳为10位需*1000，时间戳为13位的话不需乘1000
				let y = date.getFullYear();
				let MM = date.getMonth() + 1;
				MM = MM < 10 ? ('0' + MM) : MM; //月补0
				let d = date.getDate();
				d = d < 10 ? ('0' + d) : d; //天补0
				let h = date.getHours();
				h = h < 10 ? ('0' + h) : h; //小时补0
				let m = date.getMinutes();
				m = m < 10 ? ('0' + m) : m; //分钟补0
				let s = date.getSeconds();
				s = s < 10 ? ('0' + s) : s; //秒补0
				//return y + '-' + MM + '-' + d; //年月日
				return y + '-' + MM + '-' + d + ' ' + h + ':' + m + ':' + s; //年月日时分秒
			},
		},
	}
</script>

<style>
	.Info {
		font-size: 35rpx;
	}

	.Info2 {
		font-size: 35rpx;
	}

	.content {
		font-size: 50rpx;
		padding-top: 10px;
		padding-bottom: 10px;
		padding-left: 5px;
	}
	.idAndTime {
		font-size: 25rpx;
		color: #b8b8b8;
	}
	page {
		background-color: #f0f0f0;
	}
	
	.background {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: url(http://47.100.78.158:8080/img/static/background/bg8.png) no-repeat center top;
		background-size: 100%;
		background-attachment: fixed;
		z-index: -1;
	}
	
	.box {
		margin: 20px 5% 20px 5%;
		border: 1px solid #ffffff;
		background-color: #ffffff;
	}
</style>
