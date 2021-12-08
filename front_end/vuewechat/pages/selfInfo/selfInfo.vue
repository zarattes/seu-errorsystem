<template>
	<view class="background">
		<view class="box">
			<view class="textDis">
				<text>个人信息页</text>
			</view>
			<view class="textDis1">
				<text>在此页面，您可以查看您的个人信息，并可以修改姓名、学院以及导师。同时，您也可以点击修改密码按钮前往修改登陆密码</text>
			</view>
			<view class="whiteBack" >
				<view class="content-wrapper">
					<view class="login-form">
						<view class="login-form-items">
							<view class="login-form-items-title">一卡通号</view>
							<input v-model="dataList.card_id" type="number" disabled class="login-input" />
						</view>
						<view class="login-form-items">
							<view class="login-form-items-title">姓名</view>
							<input v-model="dataList.name" type="text" class="login-input" v-bind:disabled="ifedit"
								placeholder="姓名" />
						</view>
						<view class="login-form-items">
							<view class="login-form-items-title">邮箱</view>
							<input v-model="dataList.email" type="text" class="login-input" disabled
								placeholder="@seu.edu.cn" />
						</view>
						<view class="login-form-items">
							<view class="login-form-items-title">学院</view>
							<input v-show="ifedit==1" v-model="dataList.college" type="text" class="login-input" v-bind:disabled="ifedit"
								placeholder="学院" />
							<view v-show="ifedit==0">
							<picker  @change="bindPickerChange" :value="index" :range="array">
								<view>{{array[index]}}
								<image src="http://47.100.78.158:8080/img/static/down.png" style="height: 20px;width: 20px;margin-left: 10px;"></image></view>
							</picker>
							</view>
						</view>
						<view class="login-form-items">
							<view class="login-form-items-title">导师</view>
							<input v-model="dataList.supervisor" type="text" class="login-input" v-bind:disabled="ifedit"
								placeholder="导师" />
						</view>
						<view class="login-form-items">
							<view class="login-form-items-title">QQ/微信</view>
							<input v-model="dataList.qq_WeChat" type="text" class="login-input" v-bind:disabled="ifedit"/>
						</view>
						<view class="login-form-items">
							<view class="login-form-items-title">研究方向</view>
							<input v-model="dataList.research_direction" type="text" class="login-input" v-bind:disabled="ifedit"/>
						</view>
					</view>
				</view>
				<view style="text-align: center;padding-bottom: 10px;display: flex;">
					<button @click="Cancel()" v-show="show" class="btn">取消</button>
					<button @click="Confirm()" v-show="show" class="btn">确认</button>
				</view>
				<view style="display: flex;">
					<button v-show="confirm" @click="SelfInfoChange()" class="btn">修改个人信息</button>
					<button v-show="confirm" @click="PasswordChange()" class="btn">修改密码</button>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				ifedit: 1,
				show: 0,
				confirm:1,
				index:0,
				dataList: {
					college: "",
					password: "",
					last_login_time: "",
					create_time: "",
					name: "",
					card_id: "",
					email: "",
					supervisor: "",
					status: "",
					qq_WeChat:"",
					research_direction:""
				},
				collegelist:[{
					name:"",
					create_date:"",
					user_count:"",
					uuid:""
				},],
				array:[]
			};
		},
		onLoad() {
			this.ifedit = 1;
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
					console.log(res);
					this.dataList = res.data.data;
					console.log(this.dataList.college);
				},
				error: function(e) {
					this.$message.error(err);
				}
			}),
			uni.request({
					url: getApp().globalData.yuming + "/getAllCollege",
					method: "GET",
					header: {
					},
					data: {
					},
					success: (res) => {
						console.log(res);
						this.collegelist=res.data.data;
						this.array[0]="请选择";
						for(let i=0;i<this.collegelist.length;i++)
						{
							this.array[i+1]=this.collegelist[i].name;
						}
					},
					error: function(e) {
						this.$message.error(err);
					}
				})
		},
		methods: {
			bindPickerChange: function(e) {
				this.index = e.target.value;
			},
			SelfInfoChange() {
				uni.showModal({
					title: "修改个人信息",
					content: "仅可修改姓名、学院、导师、联系方式和研究方向",
					showCancel:false
				})
				this.ifedit = 0;
				this.show = 1;
				this.confirm=0;
				uni.request({
					url: getApp().globalData.yuming + "/getCollegePosition",
					method: "GET",
					header: {
						'token': this.$store.state.token
					},
					data: {
						'college': this.dataList.college
					},
					success: (res) => {
						this.index = res.data.data+1;
					},
					error: function(e) {
						this.$message.error(err);
					}
				})
			},
			Confirm() {
				if(this.array[this.index]!=this.dataList.college&&this.index!=0)
				{
					this.dataList.college=this.array[this.index]
				}
				if(this.index==0) uni.showToast({
					title:"请选择你的学院",
					icon:"error"
				})
				else {
					console.log(this.dataList.qq_Wechat);
					uni.request({
					url: getApp().globalData.yuming + "/updateUserInformation",
					method: "POST",
					header: {
						'content-type': 'application/x-www-form-urlencoded',
						'token': this.$store.state.token
					},
					data: {
						'card_id': this.dataList.card_id,
						'name': this.dataList.name,
						'password': this.dataList.password,
						'email': this.dataList.email,
						'college': this.dataList.college,
						'supervisor': this.dataList.supervisor,
						'qq_WeChat':this.dataList.qq_WeChat,
						'research_direction':this.dataList.research_direction
					},
					success: (res) => {
						if (res.statusCode == 200) uni.showToast({
							title: "修改成功",
							icon: "none"
						})
						setTimeout(function() {
							uni.navigateBack({
							})
						}, 1000)
					},
					error: function(e) {
						this.$message.error(err);
					}
				})
				}
			},
			Cancel(){
				uni.navigateBack({
				})
			},
			PasswordChange() {
				uni.navigateTo({
					url: "../passwordchange/PasswordChange"
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
	.content-wrapper {
		width: 100%;
	}
	.whiteBack{
		background-color: #ffffff;
		opacity: 0.9;
		border-radius: 10px;
	}
	.box{
		margin: 0px 5% 0px 5%;
	}
	.title {
		margin-top: 35rpx;
		width: 100%;
		margin-bottom: 10px;
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

	.btn {
		width: 43%;
		color: #ffffff;
		background-color: #00aaff;
		margin: 0px 15px  20px 15px;
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
