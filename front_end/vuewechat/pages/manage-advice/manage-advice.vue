<template>
	<view class="background">
		<view class="box">
			<view class="textDis">
				<text>建议查看</text>
			</view>
			<view class="textDis1">
				<text>在此页面，您可以查看建议，并可以点击查看建议详情，您可以通过建议人的邮箱与对方取得联系。</text>
			</view>
			<view style="opacity: 0.9;">
				<view style="opacity: 0.9;border-top-left-radius: 10px;border-top-right-radius: 10px;height: 10px;background-color: #ffffff;"></view>
				<uni-list>
					<uni-list-item v-for="(item, index) in dataList" :key="item.id" clickable @click="goToLook(item.id)"
						:showArrow="true">
						<view slot="header">
							<view><text class="queContent">建议人邮箱 {{item.user_email}}</text></view>
							<view><text class="queContent">建议描述 {{item.advice}}</text></view>
							<view><text class="idAndTime">提交时间 {{happenTimeFun(item.create_time)}}</text></view>
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
				dataList: [{
					user_email: "",
					create_time: "",
					user_id: "",
					advice: "",
					id: "",
					url: [],
				}],
				ListPage: 1,
				ListShow: 0,
				ListNumber: 0,
			}
		},
		onLoad() {
			uni.request({
				url: this.$store.state.yuming + "/admin/getAllAdvice",
				method: "GET",
				header: {
					'token': this.$store.state.token
				},
				data: {
					'offset': JSON.stringify((this.ListPage - 1) * 10),
					'limit': 10
				},
				success: (res) => {
					if (res.statusCode === 200) {
						this.dataList = res.data.data;
						if (this.dataList.length != 0) this.ListShow = 1;
						else this.ListShow = 0;
						uni.request({
							url: this.$store.state.yuming + "/admin/getAdviceTotal",
							method: "GET",
							header: {
								'token': this.$store.state.token
							},
							data: {},
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
			//查看具体建议
			goToLook(value) {
				uni.navigateTo({
					url: "../manage-advice-look/manage-advice-look?id=" + JSON.stringify(value)
				});
			},
			Left() {
				if (this.ListPage > 1) {
					this.ListPage--;
					console.log(this.ListPage);
					uni.request({
						url: this.$store.state.yuming + "/admin/getAllAdvice",
						method: "GET",
						header: {
							'token': this.$store.state.token
						},
						data: {
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
						url: this.$store.state.yuming + "/admin/getAllAdvice",
						method: "GET",
						header: {
							'token': this.$store.state.token
						},
						data: {
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
		}
	}
</script>

<style>
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

	.idAndTime {
		font-size: 25rpx;
		color: #b8b8b8;
	}

	.queContent {
		font-size: 30rpx;
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
	.Page {
		display: flex;
		text-align: center;
		background-color: #ffffff;
		border-bottom: 1px solid #ffffff;
		border-right: 1px solid #ffffff;
		border-left: 1px solid #ffffff;
		border-bottom-left-radius: 10px;
		border-bottom-right-radius: 10px;
	}
</style>
