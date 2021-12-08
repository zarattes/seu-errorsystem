<template>
	<view class="background">
		<view class="box">
			<view class="textDis">
				<text>建议反馈页</text>
			</view>
			<view class="textDis1">
				<text>在此页面，您可以提交对于本小程序的意见以及处理情况的反馈，将有专人通过您的邮箱与您取得联系。</text>
			</view>
			<view class="whiteBack">
				<view>
					<text class="title" style="padding-left: 10px;">建议与反馈：</text>
					<textarea  class="text" v-model="submitContent" placeholder="请输入您的建议与反馈,我们将尽快进行改进"></textarea>
				</view>
				<view style="margin: 10px 0px;">
					<text class="title" style="padding-left: 10px;">截图（选填）：</text>
					<text class="buttonDisplay" @click="submitPhoto()">点击上传图片</text>
					<view v-for="(item,index) in imgUrl" :key="index">
						<image :src="item"></image>
					</view>
				</view>
				<button class="btn" @click="submit()">提交建议</button>
			</view>
		</view>
	</view>
</template>

<script>
	export default{
		data(){
			return {
				imgUrl:[],
				submitContent: "",
				adviceId:""
			}
		},
		methods:{
			submitPhoto() {
				uni.chooseImage({
					sizeType: ['original', 'compressed'], //可以指定是原图还是压缩图，默认二者都有
					sourceType: ['album'], //从相册选择
					success: (res) => {
						this.imgUrl = res.tempFilePaths;
						//console.log(this.imgUrl);
					}
				});
			},
			submit() {
				//先上传文字
				uni.request({
					url: getApp().globalData.yuming + "/user/addAdvice",
					method: "POST",
					header: {
						'content-type': 'application/x-www-form-urlencoded',
						'token': this.$store.state.token
					},
					data: {
						'user_id': this.$store.state.card_id,
						'advice': this.submitContent,
						'user_email':this.$store.state.card_id+"@seu.edu.cn",
					},
					success: (res) => {
						if (res.statusCode === 200) {
							this.adviceId=res.data.data;
							console.log(this.adviceId);
							if (this.imgUrl.length > 0) {
								for (let i = 0; i < this.imgUrl.length; i++) {
									uni.uploadFile({
										url: getApp().globalData.yuming + "/user/addAdviceImg",
										filePath: this.imgUrl[i],
										name: 'img', //对应字段名！！！
										formData: {
											// 上传附带参数
											'advice_id':this.adviceId
										},
										header: {
											"content-type": "multipart/form-data",
											'token': this.$store.state.token
										},
										success: (uploadFileRes) => {
											// 根据接口具体返回格式   赋值具体对应url
											uni.showToast({
												title: '提交建议和图片成功,后续将通过邮箱取得联系',
												icon:"none",
												success: (res) => {
													setTimeout(function() {
														uni.navigateBack({
														})
													}, 2000)
												}
											});
										}
									});
								}
							} else {
								uni.showToast({
									title: '提交建议成功,后续将通过邮箱取得联系',
									icon:"none",
									success: (res) => {
										setTimeout(function() {
											uni.navigateBack({
											})
										}, 2000)
									}
								});
							}
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
	.box{
		margin: 0px 5% 20px 5%;
	}
	.title{
		font-size:40rpx;
		font-family: "楷体", "楷体_GB2312";
	}
	.text{
		margin:10px 5px 10px 5px;
		width: 95%;
		border-style: solid;
		border-width:1px;
	}
	.buttonDisplay {
		color:black;
		border-style: solid;
		border-width:1px;
		font-family: "楷体", "楷体_GB2312";
		height: 40px;
		border-radius: 10px;
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
	.btn {
		width: 60%;
		color: #ffffff;
		background-color: #00aaff;
		margin: 0px 50px  20px 70px;
		font-family: "楷体", "楷体_GB2312";
	}
	.whiteBack{
		background-color: #ffffff;
		opacity: 0.9;
		border-radius: 10px;
		padding-top: 10px;
		padding-bottom: 5px;
	}
</style>
