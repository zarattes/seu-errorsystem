<template>
	<view class="background">
		<view class="box">
			<view>
				<view>
					<view class="content"><text >故障单详情</text></view>
					<view style="padding-left: 10px;padding-bottom: 10px;"><text class="Info1">故障单号 {{dataList.id}}</text></view>
					<view style="padding-left: 10px;padding-bottom: 10px;"><text class="Info">故障类型 {{dataList.category.category_name}}</text></view>
					<view style="border-bottom: 1px solid #e6e6e7;padding-left: 10px;padding-bottom: 10px;"><text class="Info2">故障描述 {{dataList.content}}</text></view>
				</view>
				<view v-for="(item,index) in dataList.img_url" :key="index">
					<image :src="item"></image>
				</view>
				<view>
					<view class="content"><text >留言消息</text></view>
					<uni-list>
						<uni-list-item v-for="(mes,key) in messageList" :key="key">
							<view slot="header">
								<text class="user" v-if="mes.identity_id>0">{{kg}}运维人员{{kg}}</text>
								<text class="user" v-if="mes.identity_id==0">{{kg}}用户{{kg}}</text>
								<text class="time">{{happenTimeFun(mes.create_time)}}</text>
								<view><text class="content1">{{mes.content}}</text></view>
								<view v-for="(photo,index1) in mes.url" :key="index">
									<image :src="photo"></image>
								</view>
							</view>
						</uni-list-item>
					</uni-list>
				</view>
			</view>
			<view style="padding-top: 10px;">
				<textarea class="text" v-model="submitContent" placeholder="此处填写故障的留言"
					placeholder-class="ph"></textarea>
			</view>
			<view style="display: flex;padding-bottom: 10px;padding-top: 10px;">
				<button size="default" class="btn" @click="submitPhoto()">上传图片</button>
				<button size="default" class="btn" @click="submit()">提交留言</button>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				imgUrl: [],
				src1: [],
				id: "",
				submitContent: "",
				messageIdentity: 0,
				kg: "  ",
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
						console.log(this.messageList);
						/*for (let i = 0; i < this.messageList.length; i++) {
							uni.request({
								url: this.$store.state.yuming + "/getMessageImg",
								method: "GET",
								header: {
									'token': this.$store.state.token
								},
								data: {
									'messageId': this.messageList[i].message_id,
								},
								success: (res) => {
									if (res.statusCode === 200) {
										this.messageList[i].photoList = res.data.data;
										for (let j = 0; j < this.messageList[i].photoList
											.length; j++) {
											console.log(this.messageList[i].photoList[j]
												.img_url);
										}
									} else {
										reject('获取信息失败');
									}
								},
								error: function(e) {
									this.$message.error(err);
								}
							});
						};*/
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
			submit() {
				//先上传文字
				uni.request({
					url: this.$store.state.yuming + "/message",
					method: "POST",
					header: {
						'content-type': 'application/x-www-form-urlencoded',
						'token': this.$store.state.token
					},
					data: {
						'questionId': this.id,
						'userId': this.$store.state.card_id,
						'message': this.submitContent,
						'identityId': this.$store.state.role,
					},
					success: (res) => {
						if (res.statusCode === 200) {
							this.messageIdentity = res.data.data;
							console.log(this.messageIdentity);
							if (this.imgUrl.length > 0) {
								for (let i = 0; i < this.imgUrl.length; i++) {
									console.log(this.messageIdentity);
									uni.uploadFile({
										url: this.$store.state.yuming + "/messageImg",
										filePath: this.imgUrl[i],
										name: 'img', //对应字段名！！！
										formData: {
											// 上传附带参数
											'questionId': this.id,
											'messageId': this.messageIdentity,
										},
										header: {
											"content-type": "multipart/form-data",
											'token': this.$store.state.token
										},
										success: (uploadFileRes) => {
											// 根据接口具体返回格式   赋值具体对应url
											uni.showToast({
												title: '提交成功',
												duration: 1000
											});
											setTimeout(function() {
												uni.$emit('refreshData');
												uni.navigateBack({
													url: "../manage-index/manage-index"
												});
											}, 1000)
											console.log(uploadFileRes.data);
										}
									});
									/*uni.request({
										url: this.$store.state.yuming + "/messageImg",
										method: "POST",
										header: {
											'content-type': 'application/x-www-form-urlencoded',
											//'content-type': 'application/json',
											'token': this.$store.state.token
										},
										data: {
											'questionId': this.id,
											'messageId': this.messageIdentity,
											'url': this.imgUrl[i],
										},
										success: (res) => {
											if (res.statusCode === 200) {
												if (i == this.imgUrl.length - 1) {
													uni.showToast({
														title: '提交成功',
														duration: 2000
													});
													setTimeout(function() {
														uni.$emit('refreshData');
														uni.navigateBack({
															url: "../manage-index/manage-index"
														});
													}, 2000)
												};
											} else {
												reject('获取信息失败');
											}
										},
										error: function(e) {
											this.$message.error(err);
										}
									});*/
								}
							} else {
								uni.showToast({
									title: '提交成功',
									duration: 1000
								});
								setTimeout(function() {
									uni.$emit('refreshData');
									uni.navigateBack({
										url: "../manage-index/manage-index"
									});
								}, 1000)
							}
						} else {
							reject('获取信息失败');
						}
					},
					error: function(e) {
						this.$message.error(err);
					}
				});
				//再上传图片
			},
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
			submitPhoto() {
				uni.chooseImage({
					sizeType: ['original', 'compressed'], //可以指定是原图还是压缩图，默认二者都有
					sourceType: ['album'], //从相册选择
					success: (res) => {
						this.imgUrl = res.tempFilePaths;
						console.log(this.imgUrl);
					}
				});
			},
		},
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
		border: 1px solid #ffffff;
		background-color: #ffffff;
		opacity: 0.9;
		border-radius: 10px;
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

	.content1 {
		font-size: 40rpx;
	}

	.text {
		margin: 5px 5px 5px 5px;
		width: 95%;
		border-style: solid;
		border-width: 1px;
		height:50px
	}

	.btn {
		width: 35%;
		color: #ffffff;
		background-color: #00aaff;
		margin-bottom: 10px;
	}

</style>
