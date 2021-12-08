<template>
	<view class="background">
		<view class="box">
			<view class="textDis">
				<text>故障分类管理</text>
			</view>
			<view class="textDis1">
				<text>在此页面，您可以查看并管理所有故障分类，包括新增分类，编辑、删除现有分类。</text>
			</view>
			<view style="background-color: #ffffff;opacity: 0.9;border-radius: 10px;">
				<list loadmoreoffset="50">
					<!-- 注意事项: 不能使用 index 作为 key 的唯一标识 -->
					<view style="display: flex;align-items: center;padding-left: 5px;"><text class="listItem2">新增分类</text>
						<input class="listItem3" type="text" v-model="name" placeholder="请输入新分类名称"
							placeholder-class="ph">
						<button size="mini" class="btn" @click="add">确定</button>
					</view>
					<cell v-for="(item, index) in classList" :key="index">
						<view style="display: flex;text-align: center;"><text
								class="listItem">{{item.category_name}}</text><text class="listItem1"
								@click.native="open(item.category_name,item.id)">编辑</text><text class="listItem1"
								@click.native="deleteClass(item.id)">删除</text>
						</view>
					</cell>
				</list>
				<uni-popup ref="popup" type="dialog">
					<uni-popup-dialog ref="inputClose" mode="input" title="修改分类名称" v-model="name1" :before-close="true"
						@close="close" @confirm="update">
					</uni-popup-dialog>
				</uni-popup>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				name: "",
				name1: "",
				id: "",
				classList: [{
					category_name: "",
					create_time: "",
					id: ""
				}],
			}
		},
		onLoad() {
			uni.request({
				url: this.$store.state.yuming + "/getAllCategory",
				method: "GET",
				header: {
					'token': this.$store.state.token
				},
				data: {},
				success: (res) => {
					if (res.statusCode === 200) {
						this.classList = res.data.data;
						console.log(this.classList);
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
			//重新加载
			reloadData() {
				uni.request({
					url: this.$store.state.yuming + "/getAllCategory",
					method: "GET",
					header: {
						'token': this.$store.state.token
					},
					data: {},
					success: (res) => {
						if (res.statusCode === 200) {
							this.classList = res.data.data;
							this.name = "";
							console.log(this.classList);
						} else {
							reject('获取信息失败');
						}
					},
					error: function(e) {
						this.$message.error(err);
					}
				});
			},
			add() {
				uni.request({
					url: this.$store.state.yuming + "/admin/addCategory",
					method: "POST",
					header: {
						'content-type': 'application/x-www-form-urlencoded',
						'token': this.$store.state.token
					},
					data: {
						'name': this.name,
					},
					success: (res) => {
						if (res.statusCode === 200) {
							uni.showToast({
								title: '添加新分类成功',
								duration: 1000
							});
							setTimeout(function() {
								uni.redirectTo({
									url: "../manage-class/manage-class"
								})
							}, 1000)

						} else {
							reject('获取信息失败');
						}
					},
					error: function(e) {
						this.$message.error(err);
					}
				});
			},
			open(value, key) {
				this.name1 = value;
				this.id = key;
				this.$refs.popup.open();
			},
			close() {
				this.$refs.popup.close()
			},
			update(value) {
				uni.request({
					url: this.$store.state.yuming + "/admin/modifyCategory",
					method: "POST",
					header: {
						'content-type': 'application/x-www-form-urlencoded',
						'token': this.$store.state.token
					},
					data: {
						'name': value,
						'id': this.id,
					},
					success: (res) => {
						if (res.statusCode === 200) {
							uni.showToast({
								title: '修改分类成功',
								duration: 1000
							});
							this.$refs.popup.close();
							setTimeout(function() {
								uni.redirectTo({
									url: "../manage-class/manage-class"
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
			},
			deleteClass(id) {
				uni.request({
					url: this.$store.state.yuming + "/admin/deleteCategory",
					method: "POST",
					header: {
						'content-type': 'application/x-www-form-urlencoded',
						'token': this.$store.state.token
					},
					data: {
						'id': id,
					},
					success: (res) => {
						if (res.statusCode === 200) {
							uni.showToast({
								title: '删除分类成功',
								duration: 1000
							});
							setTimeout(function() {
								uni.redirectTo({
									url: "../manage-class/manage-class"
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
			},
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

	.listItem {
		width: 52%;
		font-size: small;
		padding: 10px 0 10px 0;
		border-top: 1px solid #e6e6e7;
		border-right: 1px solid #e6e6e7;
	}

	.listItem1 {
		color: #00aaff;
		width: 24%;
		font-size: small;
		padding: 10px 0 10px 0;
		border-top: 1px solid #e6e6e7;
		border-right: 1px solid #e6e6e7;
	}

	.listItem2 {
		width: 30%;
		padding: 20px 0 20px 0;
	}
	.listItem3 {
		width: 45%;
		padding: 20px 0 20px 0;
	}

	.btn {
		color: #ffffff;
		background-color: #00aaff;
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
