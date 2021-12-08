<template>
	<view class="background">
	<view class="box">
		<view class="textDis">
			<text>提交问题</text>
		</view>
		<view class="textDis1">
			<text>在此页中，您可以提交您想问的问题的相关信息（分类、联系电话、问题详情），后续可在问题详情页中上传补充图片</text>
		</view>
		<view style="background-color: #ffffff;border-radius: 10px;opacity: 0.9;padding-top: 10px;padding-bottom: 10px;">
		<view style="margin-bottom: 10px;padding-left: 10px;padding-right: 10px;">
			<view class="myview">
				<text class="mytext">故障分类:</text>
				<picker class="mytext" @change.native="bindPickerChange" :value="index" :range="array">
					<view>{{array[index]}}
					<image src="http://47.100.78.158:8080/img/static/down.png" style="height: 20px;width: 20px;"></image></view>
				</picker>
			</view>
			<br>
			<input class="text" v-model="contact_phone" placeholder="请输入联系电话">
			<br><br>
			<textarea class="text" v-model="quecontent" placeholder="请输入您的详细问题,我们将尽快为您解决"></textarea>
		</view>
		<view style="margin: 10px 10px;">
			<text class="mytext" style="padding-left: 10px;">截图（选填）：</text>
			<text class="buttonDisplay" @click="submitPhoto()">点击上传图片</text>
			<view v-for="(item,index) in imgArr" :key="index">
				<image :src="item"></image>
			</view>
		</view>
		<view>
			<button @click="trans()" class="btn">点此提交你的问题</button>
		</view>
		</view>
	</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				quesubmit:'故障提交：',
				index:0,
				array: [],//存分类名
				quetypeid: [],//存分类id
				categoryid:"",//先分类id
				quecontent:"",
				imgArr:[],
				question_id:'',
				contact_phone:'',
				dataList: [{
					category_name:"",
					create_time:"",
					id:""
				}, ],
			}
		},
		onLoad() {
			uni.request({
				url: getApp().globalData.yuming + "/getAllCategory",
				method: "GET",
				header: {
					'token': this.$store.state.token
				},
				data: {
				},
				success: (res) => {
					if (res.statusCode === 200) {
						this.dataList = res.data.data;
						this.array[0]="请选择";
						this.quetypeid[0]=0;
						for(let i=0;i<this.dataList.length;i++)
						{
							this.array[i+1]=this.dataList[i].category_name;
							this.quetypeid[i+1]=this.dataList[i].id;
						}
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
			bindPickerChange: function(e) {
				this.index = e.target.value;
				this.pickQuestion(e.target.value);
			},
			pickQuestion(value){
				this.categoryid=this.quetypeid[value];
			},
			submitPhoto() {
				uni.chooseImage({
					sizeType: ['original', 'compressed'], //可以指定是原图还是压缩图，默认二者都有
					sourceType: ['album'], //从相册选择
					success: (res) => {
						this.imgArr = res.tempFilePaths;
					}
				});
			},
			trans(){
				if(this.categoryid==0) {
					uni.showToast({
						title:"请选择合适的分类",
						icon:"none"
					})
				}
				else{
				if(this.quecontent=="") this.quecontent="暂无详细描述";
				uni.request({
					url: getApp().globalData.yuming + "/user/postQuestion",
					method: "POST",
					header: {
						'content-type':'application/x-www-form-urlencoded',
						'token': this.$store.state.token
					},
					data: {
						'user_id':this.$store.state.card_id,
						'content':this.quecontent,
						'category_id':this.categoryid,
						'contact_phone':this.contact_phone
					},
					success: (res) => {
						if (res.statusCode === 200) {
							this.question_id = res.data.question_id;
							if (this.imgArr.length > 0) {
								for (let i = 0; i < this.imgArr.length; i++) {
								uni.uploadFile({
									url:getApp().globalData.yuming + "/user/postImg",
									filePath:this.imgArr[i],
									name:'img',
									formData:{
										'question_id':this.question_id
									},
									header: {
										"content-type": "multipart/form-data",
										'token': this.$store.state.token
									},
									success:(res)=>{
										uni.showToast({
											title:"上传成功",
											icon:"none"
										});
										setTimeout(function() {
											uni.navigateBack({
											})
										}, 1000)
										
									}
								})
								}
							}
						} else {
							uni.showToast({
								title:"提交问题失败",
								icon:"none"
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
	.myview{
		display: flex;
		justify-content: left;
	}
	.mytext{
		font-size:20px;
	}
	.text{
		margin:5px 5px 5px 5px;
		width: 95%;
		border-style: solid;
		border-width:1px;
	}
	.titlearea {
		display: flex;
		justify-content: center;
		color: #333333;
	}

	.title {
		font-size: 40rpx;
		color: #333333;
	}
	.buttonDisplay {
		color:black;
		border-style: solid;
		border-width:1px;
		font-family: "楷体", "楷体_GB2312";
		height: 40px;
		border-radius: 10px;
	}
	.btn {
		width: 60%;
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
