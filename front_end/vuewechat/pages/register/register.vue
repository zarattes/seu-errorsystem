<template>
	<view class="background">
	<view class="box">
		<view class="textDis">
			<text>注册</text>
		</view>
		<view class="textDis1">
			<text>在此页中，您可以利用您的一卡通号进行注册。正确输入注册信息后发送验证邮件,邮件验证通过后点击确认注册即可完成注册，注意：密码格式为8-12位且带有字母和数字</text>
		</view>
		<view style="background-color: #ffffff;border-radius: 10px;opacity: 0.9;padding-bottom: 10px;">
		<view class="content-wrapper">
			<view class="login-form">
				<view class="login-form-items">
					<view class="login-form-items-title">一卡通号</view>
					<input v-model="card_id" type="number" class="login-input" @input="setemail()" placeholder="请输入一卡通号"
						maxlength="9" placeholder-class="ph">
				</view>
				<view class="login-form-items">
					<view class="login-form-items-title">姓名</view>
					<input v-model="name" type="text" class="login-input" placeholder="请输入姓名" placeholder-class="ph" />
				</view>
				<view class="login-form-items">
					<view class="login-form-items-title">密码</view>
					<input v-model="password" type="password" class="login-input" placeholder="请输入密码" maxlength="12"
						placeholder-class="ph" />
				</view>
				<view class="login-form-items">
					<view class="login-form-items-title">密码确认</view>
					<input v-model="Confirmpassword" type="password" class="login-input" placeholder="请再次输入密码"
						placeholder-class="ph" />
				</view>
				<view class="login-form-items">
					<view class="login-form-items-title">学院</view>
					<picker @change="bindPickerChange" :value="index" :range="array">
						<view>{{array[index]}}
						<image src="http://47.100.78.158:8080/img/static/down.png" style="height: 20px;width: 20px;margin-left: 10px;"></image></view>
					</picker>
				</view>
				<view class="login-form-items">
					<view class="login-form-items-title">用户类型</view>
					<picker @change="bindPickerChange2" :value="index2" :range="permission">
						<view>{{permission[index2]}}
						<image src="http://47.100.78.158:8080/img/static/down.png" style="height: 20px;width: 20px;margin-left: 10px;"></image>
						</view>
					</picker>
				</view>
				<view class="login-form-items">
					<view class="login-form-items-title">QQ/微信</view>
					<input v-model="qq_Wechat" type="text" class="login-input" placeholder="请输入联系方式" placeholder-class="ph" />
				</view>
				<view class="login-form-items">
					<view class="login-form-items-title">邮箱</view>
					<input v-model="email" type="text" class="login-input" disabled placeholder="@seu.edu.cn"
						placeholder-class="ph" />
				</view>
				<view class="login-form-items">
					<view class="login-form-items-title">导师(选填)</view>
					<input v-model="supervisor" type="text" class="login-input" placeholder="请输入导师"
						placeholder-class="ph" />
				</view>
				<view class="login-form-items">
					<view class="login-form-items-title">研究方向</view>
					<input v-model="research_direction" type="text" class="login-input" placeholder="请输入研究方向" placeholder-class="ph" />
				</view>
			</view>
		</view>
		<view style="display: flex;">
			<button @click="Preregister" class="btn">发送验证邮件</button>
			<button v-bind:disabled="ifSend" @click="register" class="btn">确认注册</button>
		</view>
		</view>
	</view>
	</view>
</template>

<script>
	function checkPassword(password) {
		console.log(password);
		var reg = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,12}$/;
		if (!reg.test(password) || password.length < 8 || password.length > 12) return false;
		else return true;
	}

	function checkCard(card) {
		if (card.slice(0, 2) != 21 && card.slice(0, 2) != 22 && card.slice(0, 2) != 23 && card.slice(0, 2) != 10)
		return false;
		else return true;
	}
	export default {
		data() {
			return {
				index:0,
				index2:0,
				ifSend: 1,
				status: 0,
				card_id: "",
				name: "",
				password: "",
				Confirmpassword: "",
				email: "",
				supervisor: "",
				permission:["请选择","管理员","本科生","研究生","博士","老师"],
				qq_Wechat:"",
				research_direction:"",
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
			uni.showModal({
				title: "注册提示",
				content: "正确输入注册信息后发送验证邮件,邮件验证通过后点击确认注册即可完成注册，注意：密码格式为8-12位且带有字母和数字",
				success: function(res) {
					if (res.confirm) {
						console.log('用户点击确定');
					} else if (res.cancel) {
						uni.reLaunch({
							url: "../denglu/denglu"
						})
					}
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
			bindPickerChange2: function(e) {
				this.index2 = e.target.value;
				console.log(this.index2+this.permission[this.index2]);
			},
			setemail() {
				this.email = this.card_id + "@seu.edu.cn"
			},
			Preregister() {
				if (!checkCard(this.card_id)) uni.showToast({
					title: "请输入正确的一卡通号",
					icon: "none"
				})
				else if (this.name == "") uni.showToast({
					title: "请输入姓名",
					icon: "none"
				})
				else if (!checkPassword(this.password)) uni.showToast({
					title: "请输入包含字母和数字的8-12位密码",
					icon: "none"
				})
				else if (this.password != this.Confirmpassword) uni.showToast({
					title: "两次密码输入不同，请检查",
					icon: "none"
				})
				else if (this.array[this.index] == "请选择") uni.showToast({
					title: "请选择学院",
					icon: "none"
				})
				else if (this.index2==0) uni.showToast({
					title: "请选择用户类型",
					icon: "none"
				})
				else {
					uni.request({
						url: this.$store.state.yuming + "/register",
						method: "POST",
						header: {
							'content-type':'application/x-www-form-urlencoded',
						},
						data: {
							'card_id': this.card_id,
							'name': this.name,
							'password': this.password,
							'email': this.email,
							'college': this.array[this.index],
							'supervisor': this.supervisor,
							'permission':this.index2-1,
							'qq_Wechat':this.qq_Wechat,
							'research_direction':this.research_direction
						},
						success: (res) => {
							if (res.statusCode === 200) {
								uni.showToast({
									title: "成功发送验证邮件,请前往激活",
									icon: "none"
								});
								this.ifSend = 0;
							} else {
								reject('获取信息失败');
							}
						},
						error: function(e) {
							this.$message.error(err);
						}
					})
				}
			},
			register() {
				uni.request({
					url: this.$store.state.yuming + "/checkStatus",
					method: "GET",
					header: {},
					data: {
						'card_id': this.card_id
					},
					success: (res) => {
						console.log(res.data);
						if (res.data.code == 200) {
							this.status=1;
							uni.showToast({
								title: "注册成功",
								icon: "none"
							});
							setTimeout(function() {
								uni.reLaunch({
									url: "../denglu/denglu"
								})
							}, 1000)
						} else if(res.data.code == 13){
							this.status=0;
							uni.showToast({
								title: "请完成邮箱激活",
								icon: "none"
							});
						}
					},
					error: function(e) {
						this.$message.error(err);
					}
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

	.title {
		margin-top: 35rpx;
		width: 100%;
		margin-bottom: 10px;
		font-family: "楷体", "楷体_GB2312";
	}


	.login-form {
		margin: 20px 10px 20px 15px;
		background: #FFFFFF;
	}

	.login-form-items {
		padding: 15px 10px;
		border-bottom: 1px solid #e6e6e7;
		position: relative;
		display: -webkit-flex;
		display: flex;
	}

	.login-form-items-title {
		width: 30%;
		line-height: 22px;
		height: 22px;
		flex-shrink: 0;
	}

	.login-input {
		width: 100%;
	}

	.ph {
		font-family: "楷体", "楷体_GB2312";
	}
	.btn {
		width: 43%;
		color: #ffffff;
		background-color: #00aaff;
	}
	.box{
		margin: 0px 5% 20px 5%;
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
