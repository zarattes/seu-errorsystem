<template>
	<view class="background">
		<view class="box">
			<view class="textDis">
				<text>故障查看</text>
			</view>
			<view class="textDis1">
				<text>在此页面，您可以查看处于不同处理状态的故障，并可以点击查看故障详情，选择进行处理，留言以及归档。</text>
			</view>
			<view class="look"><text class="leftlook">选择查看的种类:</text>
				<view class="rightlook">
					<picker @change="bindPickerChange" :value="index" :range="array">
						<view><text space="emsp" decode="true">{{array[index]}}{{kg}}</text><image src="../../static/down.png" style="height: 15px;width: 15px;"></image></view>
					</picker>
				</view>
			</view>
			<view style="border-radius: 10px;opacity: 0.9;">
				<uni-list>
					<uni-list-item v-for="(item, index) in dataList" :key="item.id" clickable
						@click="goToSolve(item.id,item.answer_status)" :showArrow="true">
						<view slot="header"><text v-if="item.answer_status==0" class="stateDisplay" space="emsp"
								decode="true">{{kg}}待处理{{kg}}</text>
							<text v-if="item.answer_status==3" class="stateDisplay" space="emsp"
								decode="true">{{kg}}{{item.name}}已归档{{kg}}</text>
							<text
								v-if="item.answer_status==1"
								class="stateDisplay" space="emsp" decode="true">{{kg}}{{item.name}}处理中{{kg}}</text>
							<text
								v-if="item.answer_status==2"
								class="stateDisplay" space="emsp" decode="true">{{kg}}{{item.name}}已解决{{kg}}</text>
							<view style="padding-top: 5rpx;padding-bottom: 5rpx;"><text class="idAndTime1">故障单号 {{item.id}}</text></view>
							<view style="padding-bottom: 5rpx;"><text class="queType">故障类型 {{item.category.category_name}}</text></view>
							<view style="padding-bottom: 5rpx;"><text class="queContent">故障描述 {{item.content}}</text></view>
							<view style="padding-bottom: 5rpx;"><text class="idAndTime">上报时间 {{happenTimeFun(item.create_time)}}</text></view>
							<view style="padding-bottom: 5rpx;"><text class="idAndTime">更新时间 {{happenTimeFun(item.update_time)}}</text></view>
						</view>

					</uni-list-item>
				</uni-list>
				<view v-show="ListShow" class="Page">
					<text @click.native="Left" class="page">上一页</text>
					<text class="page1">{{ListPage}}/{{Math.ceil(ListNumber/10)}}</text>
					<text @click.native="Right" class="page">下一页</text>
				</view>
			</view>
		</view>
	</view>
</template>
<script>
	export default {
		data() {
			return {
				kg: " ",
				array: ['所有', '待处理', '所有处理中', '所有已解决', '自己处理中', '自己已解决', '已归档'],
				index: 0,
				ListPage: 1,
				ListShow: 0,
				ListNumber: 0,
				dataList: [{
					create_time: "",
					update_time: "",
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
					name:"",
				}, ],
			}
		},
		//第一次进页面时加载所有问题
		onLoad() {
			uni.request({
				url: this.$store.state.yuming + "/admin/getAllQuestion",
				method: "GET",
				header: {
					'token': this.$store.state.token
				},
				data: {
					'style': 0,
					'admin_id': this.$store.state.card_id,
					'offset': JSON.stringify((this.ListPage - 1) * 10),
					'limit': 10
				},
				success: (res) => {
					if (res.statusCode === 200) {
						this.dataList = res.data.data;
						if (this.dataList.length != 0) this.ListShow = 1;
						else this.ListShow = 0;
						uni.request({
							url: this.$store.state.yuming + "/admin/getTotal",
							method: "GET",
							header: {
								'token': this.$store.state.token
							},
							data: {
								'style': 0,
								'admin_id': this.$store.state.card_id
							},
							success: (res) => {
								if (res.statusCode === 200) {
									this.ListNumber = res.data.data;
									console.log(this.ListNumber);
								} else {
									reject('获取信息失败');
								}
							},
							error: function(e) {
								this.$message.error(err);
							}
						});
					} else {
						reject('获取信息失败');
					}
				},
				error: function(e) {
					this.$message.error(err);
				}
			});
			uni.$on('refreshData', () => {
				uni.request({
					url: this.$store.state.yuming + "/admin/getAllQuestion",
					method: "GET",
					header: {
						'token': this.$store.state.token
					},
					data: {
						'style': 0,
						'admin_id': this.$store.state.card_id,
						'offset': JSON.stringify((this.ListPage - 1) * 10),
						'limit': 10
					},
					success: (res) => {
						if (res.statusCode === 200) {
							this.dataList = res.data.data;
							if (this.dataList.length != 0) this.ListShow = 1;
							else this.ListShow = 0;
							uni.request({
								url: this.$store.state.yuming + "/admin/getTotal",
								method: "GET",
								header: {
									'token': this.$store.state.token
								},
								data: {
									'style': 0,
									'admin_id': this.$store.state.card_id
								},
								success: (res) => {
									if (res.statusCode === 200) {
										this.ListNumber = res.data.data;
										console.log(this.ListNumber);
									} else {
										reject('获取信息失败');
									}
								},
								error: function(e) {
									this.$message.error(err);
								}
							});
							console.log(this.dataList);
						} else {
							reject('获取信息失败');
						}
					},
					error: function(e) {
						this.$message.error(err);
					}
				});
			});
		},
		methods: {
			bindPickerChange: function(e) {
				this.index = e.target.value;
				this.pickQuestion(e.target.value);
			},
			//选择问题种类
			pickQuestion(value) {
				uni.request({
					url: this.$store.state.yuming + "/admin/getAllQuestion",
					method: "GET",
					header: {
						'token': this.$store.state.token
					},
					data: {
						'style': value,
						'admin_id': this.$store.state.card_id,
						'offset': JSON.stringify((this.ListPage - 1) * 10),
						'limit': 10
					},
					success: (res) => {
						if (res.statusCode === 200) {
							this.dataList = res.data.data;
							this.ListPage = 1;
							if (this.dataList.length != 0) this.ListShow = 1;
							else this.ListShow = 0;
							uni.request({
								url: this.$store.state.yuming + "/admin/getTotal",
								method: "GET",
								header: {
									'token': this.$store.state.token
								},
								data: {
									'style': value,
									'admin_id': this.$store.state.card_id
								},
								success: (res) => {
									if (res.statusCode === 200) {
										this.ListNumber = res.data.data;
										console.log(this.ListNumber);
									} else {
										reject('获取信息失败');
									}
								},
								error: function(e) {
									this.$message.error(err);
								}
							});
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
			//跳转至相应问题界面
			goToSolve(id, status) {
				if (status == 0) {
					uni.request({
						url: this.$store.state.yuming + "/admin/handleQuestion",
						method: "POST",
						header: {
							'content-type': 'application/x-www-form-urlencoded',
							'token': this.$store.state.token
						},
						data: {
							'question_id': id,
							'admin_id': this.$store.state.card_id
						},
						success: (res) => {
							if (res.statusCode === 200) {

							} else {
								reject('进行处理失败');
							}
						},
						error: function(e) {
							this.$message.error(err);
						}
					})
				};
				if (status == 2) {
					uni.navigateTo({
						url: "../manage-solved/manage-solved?id=" + JSON.stringify(id)
					});
				};
				if (status == 3) {
					uni.navigateTo({
						url: "../manage-save/manage-save?id=" + JSON.stringify(id)
					});
				}
				uni.navigateTo({
					url: "../manage-solve/manage-solve?id=" + JSON.stringify(id)
				});
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
			//上一页
			Left() {
				if (this.ListPage > 1) {
					this.ListPage--;
					console.log(this.ListPage);
					uni.request({
						url: this.$store.state.yuming + "/admin/getAllQuestion",
						method: "GET",
						header: {
							'token': this.$store.state.token
						},
						data: {
							'style': this.index,
							'admin_id': this.$store.state.card_id,
							'offset': JSON.stringify((this.ListPage - 1) * 10),
							'limit': 10
						},
						success: (res) => {
							if (res.statusCode === 200) {
								this.dataList = res.data.data;
								if (this.dataList.length != 0) this.ListShow = 1;
								console.log(this.dataList);
							} else {
								reject('获取信息失败');
							}
						},
						error: function(e) {
							this.$message.error(err);
						}
					})
					uni.pageScrollTo({
						scrollTop: 0,
						duration: 300
					})
				} else {
					console.log(this.ListPage);
					uni.showToast({
						title: "已经是第一页了",
						icon: "none"
					})
				}
			},
			//下一页
			Right() {
				if (this.ListPage < Math.ceil(this.ListNumber / 10)) {
					this.ListPage++;
					console.log(this.ListPage);
					uni.request({
						url: this.$store.state.yuming + "/admin/getAllQuestion",
						method: "GET",
						header: {
							'token': this.$store.state.token
						},
						data: {
							'style': this.index,
							'admin_id': this.$store.state.card_id,
							'offset': JSON.stringify((this.ListPage - 1) * 10),
							'limit': 10
						},
						success: (res) => {
							if (res.statusCode === 200) {
								this.dataList = res.data.data;
								if (this.dataList.length != 0) this.ListShow = 1;
								console.log(this.dataList);
							} else {
								reject('获取信息失败');
							}
						},
						error: function(e) {
							this.$message.error(err);
						},
					});
					uni.pageScrollTo({
						scrollTop: 0,
						duration: 300
					})
				} else {
					uni.showToast({
						title: "已经是最后一页了",
						icon: "none"
					})
				}
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
	}

	.content {
		display: flex;
		flex-direction: column;
		align-items: left;
		justify-content: left;
	}

	.logo {
		height: 200rpx;
		width: 200rpx;
		margin-top: 200rpx;
		margin-left: auto;
		margin-right: auto;
		margin-bottom: 50rpx;
	}

	.text-area {
		display: flex;
		justify-content: left;
		color: #333333;
	}

	.title {
		font-size: 36rpx;
		color: #333333;
	}
	
	.textDis{
		font-size: 50rpx;
		font-weight: 900;
		color: #ffffff;
		padding-bottom: 20px;
	}
	
	.textDis1{
		font-size: 30rpx;
		color: #ffffff;
		padding-bottom: 20px;
	}
	
	.look {
		display: flex;
		border-top: 0px solid #e6e6e7;
		text-align: center;
		align-items: center;
		opacity: 0.9;
	}

	.leftlook {
		width: 50%;
		background-color: #FFFFFF;
		align-items: center;
		text-align: center;
		padding: 10px 0 10px 0;
		border-right: 0px solid #e6e6e7;
		border-left: 0px solid #e6e6e7;
		border-top-left-radius: 10px ;
	}

	.rightlook {
		width: 50%;
		background-color: #FFFFFF;
		align-items: center;
		text-align: center;
		padding: 10px 0 10px 0;
		border-right: 0px solid #e6e6e7;
		border-top-right-radius: 10px ;
	}

	.listDisplay {
		height: 100px;
	}

	.stateDisplay {
		background-color: #00aaff;
		color: #ffffff;
		height: 20px;
		border-radius: 10px;
	}

	.idAndTime {
		font-size: 30rpx;
		color: #b8b8b8;
	}
	.idAndTime1 {
		font-size: 25rpx;
		color: #b8b8b8;
	}

	.queType {
		font-size: 35rpx;
	}

	.queContent {
		font-size: 30rpx;
	}

	.titleDisplay {
		font-size: 20px;
	}

	.butDis {
		font-size: 15px;
	}

	.page {
		text-align: center;
		width: 30%;
		padding: 10px 0 10px 0;
	}

	.page1 {
		text-align: center;
		width: 40%;
		padding: 10px 0 10px 0;
	}

	.Page {
		display: flex;
		text-align: center;
		background-color: #ffffff;
		border-bottom: 1px solid #ffffff;
		border-right: 1px solid #ffffff;
		border-left: 1px solid #ffffff;
		border-bottom-left-radius: 10px;
		border-bottom-right-radius: 10px;
		opacity: 0.9;
	}
</style>
