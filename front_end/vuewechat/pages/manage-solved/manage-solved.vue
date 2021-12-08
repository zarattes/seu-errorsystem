<template>
	<view class="background">
		<view class="box">
			<view>
				<view>
					<view class="content"><text>故障单详情</text></view>
					<view style="padding-left: 10px;padding-bottom: 10px;"><text class="Info1">故障单号 {{dataList.id}}</text></view>
					<view style="padding-left: 10px;padding-bottom: 10px;"><text class="Info">故障类型 {{dataList.category.category_name}}</text></view>
					<view style="border-bottom: 1px solid #e6e6e7;padding-left: 10px;padding-bottom: 10px;"><text class="Info2">故障描述 {{dataList.content}}</text></view>
				</view>
				<view v-for="(item,index) in dataList.img_url" :key="index">
					<image :src="item"></image>
				</view>
				<view>
					<view class="content"><text>留言消息</text><br></view>
					<uni-list>
						<uni-list-item v-for="(mes,key) in messageList" :key="key">
							<view slot="header">
								<text class="user" v-if="mes.identity_id>0">{{kg}}运维人员{{kg}}</text>
								<text class="user" v-if="mes.identity_id==0">{{kg}}用户{{kg}}</text>
								<text class="time">{{happenTimeFun(mes.create_time)}}</text>
								<view><text class="content">{{mes.content}}</text></view>
								<view v-for="(photo,index1) in mes.url" :key="index">
									<image :src="photo"></image>
								</view>
							</view>
						</uni-list-item>
					</uni-list>
				</view>
			</view>
			<view>
				<view class="content"><text>故障归档答案</text></view>
				<textarea class="text" v-model="message" placeholder="此处填写归档故障的答案" placeholder-class="ph"></textarea>
			</view>
			<view style="display: flex;padding-bottom: 10px;">
				<button size="default" class="btn" @click="saved">将该故障归档</button>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				kg:" ",
				imgUrl: [],
				src1: [],
				id: "",
				submitContent: "",
				kg: "  ",
				message: "",
				year: "",
				month: "",
				date_time: "",
				dataList: {
					create_time: "",
					updatae_time: "",
					category_id: "",
					category: {
						"category_name": "",
						"create_time": "",
						"id": ""
					},
					contact_phone: "",
					user_id: "",
					img_url: [],
					admin_id: "",
					id: "",
					content: "",
					answer_status: 0,
				},
				messageList: [{
					create_time: "",
					user_id: "",
					identity_id: 0,
					question_id: "",
					message_id: 0,
					content: "",
					url: [],
				}],
			}
		},
		//第一次进页面时加载这个问题的相关资料
		onLoad: function(option) {
			this.id = JSON.parse(option.id);
			uni.request({
				url: this.$store.state.yuming + "/admin/getQuestionById",
				method: "GET",
				header: {
					'token': this.$store.state.token
				},
				data: {
					'question_id': this.id,
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
			//加载留言
			uni.request({
				url: this.$store.state.yuming + "/getMessage",
				method: "GET",
				header: {
					'token': this.$store.state.token
				},
				data: {
					'questionId': this.id,
				},
				success: (res) => {
					if (res.statusCode === 200) {
						this.messageList = res.data.data;
						for (let i = 0; i < this.messageList.length; i++) {
							if (this.messageList[i].identity_id == 0) {
								this.message += "追问：";
								this.message += this.messageList[i].content;
								this.message += "   ";
							} else if (this.messageList[i].identity_id > 0) {
								this.message += "回答：";
								this.message += this.messageList[i].content;
								this.message += "   ";
							}
						}
						console.log(this.message);
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
			saved() {
				let date = new Date();
				this.year = date.getFullYear();
				this.month = date.getMonth() + 1;
				this.month = this.month < 10 ? ('0' + this.month) : this.month; //月补0
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
				this.date_time = y + '-' + MM + '-' + d + ' ' + h + ':' + m + ':' + s;
				console.log(this.date_time);
				uni.request({
					url: this.$store.state.yuming + "/admin/addData",
					method: "POST",
					header: {
						'content-type': 'application/x-www-form-urlencoded',
						'token': this.$store.state.token
					},
					data: {
						'year': this.year,
						'month': this.month,
						'date_time': this.date_time,
						'question': this.dataList.content,
						'category': this.dataList.category.category_name,
						'answer': this.message,
						'question_id': this.id,
					},
					success: (res) => {
						if (res.statusCode === 200) {
							uni.showToast({
								title: '归档成功',
								duration: 1000
							});
							setTimeout(function() {
								uni.$emit('refreshData');
								uni.navigateBack({
									url: "../manage-index/manage-index"
								});
							}, 1000)
						} else {
							reject('获取信息失败');
						}
					},
					error: function(e) {
						this.$message.error(err);
					}
				});
			}
		},
	}
</script>

<style>
	.Info {
		font-size: 30rpx;
	}

	.Info1 {
		font-size: 30rpx;
	}

	.Info2 {
		font-size: 30rpx;
	}

	.user {
		font-size: 40rpx;
		color: #8a8a8a;
	}

	.time {
		font-size: 30rpx;
		color: #8a8a8a;
	}

	.content {
		font-size: 50rpx;
		padding-top: 10px;
		padding-bottom: 10px;
		padding-left: 5px;
	}

	.text {
		margin: 5px 5px 5px 5px;
		width: 95%;
		border-style: solid;
		border-width: 1px;
	}

	.btn {
		margin-top: 20px;
		width: 60%;
		color: #ffffff;
		background-color: #00aaff;
		padding-right: 10px;
	}

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
		border: 1px solid #ffffff;
		background-color: #ffffff;
		opacity: 0.9;
		border-radius: 10px;
	}
</style>
