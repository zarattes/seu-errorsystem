<template>
	<view class="background">
	<view class="box">
		<view class="textDis">
			<text>已解决的问题</text>
		</view>
		<view class="textDis1">
			<text>在此页中，您可以查看问题的相关信息</text>
		</view>
		<view style="background-color: #ffffff;border-radius: 10px;opacity: 0.9;padding-top: 10px;padding-bottom: 10px;">
		<view>
			<view class="content"><text >故障单详情</text></view>
			<view style="padding-left: 10px;padding-bottom: 10px;"><text class="Info1">单号 {{dataList.id}}</text></view>
			<view style="padding-left: 10px;padding-bottom: 10px;"><text class="Info">上报时间 {{happenTimeFun(dataList.create_time)}}</text></view>
			<view style="padding-left: 10px;padding-bottom: 10px;"><text class="Info">故障类型 {{dataList.category.category_name}}</text></view>
			<view style="padding-left: 10px;padding-bottom: 10px;"><text class="Info">负责人id {{dataList.admin_id}}</text></view>
			<view style="border-bottom: 1px solid #e6e6e7;padding-left: 10px;padding-bottom: 10px;"><text class="Info2">故障描述 {{dataList.content}}</text></view>
			<view v-for="(item,index) in dataList.img_url" :key="index">
			    <image :src="item"></image>
			</view>
		</view>
		</view>
	</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				Q_id: '',
				imgArr:"",
				photoShow:0,
				dataList:{
					update_time: "",
					category_id: "",
					create_time: "",
					user_id:"",
					img_url:[],
					admin_id:"",
					id: "",
					category:{
						category_name:"",
						create_time:"",
						id:""
					},
					content: "",
					answer_status: 2,
				}
			}
		},
		//第一次进页面时加载这个问题的相关资料
		onLoad: function(option) {
			this.Q_id = option.id;
			console.log(this.Q_id);
			uni.request({
				url: getApp().globalData.yuming + "/user/getQuestionById",//需要接口
				method: "GET",
				header: {
					'content-type':'application/x-www-form-urlencoded',
					'token': this.$store.state.token
				},
				data: {
					'question_id': this.Q_id,
				},
				success: (res) => {
					if (res.statusCode === 200) {
						this.dataList = res.data.data;
						if(this.dataList.img_url.length>0) this.photoShow=1;
						console.log(this.dataList);
					} else {
						reject('获取信息失败');
					}
				},
				error: function(e) {
					this.$message.error(err);
				}
			})
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
			}
		},
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
	.mytext{
		font-size:30rpx;
		font-family: "楷体", "楷体_GB2312";
	}
	.box{
		margin: 0px 5% 0px 5%;
	}
	.content {
		font-size: 50rpx;
		padding-top: 10px;
		padding-bottom: 10px;
		padding-left: 5px;
	}
	.Info {
		font-size: 30rpx;
	}
	
	.Info1 {
		font-size: 30rpx;
	}
	
	.Info2 {
		font-size: 30rpx;
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
