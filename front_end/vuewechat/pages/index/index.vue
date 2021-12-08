<template>
	<view class="background">
		<view class="box">
			<view class="textDis">
				<text>首页</text>
			</view>
			<view class="textDis1">
				<text>在此页面，您可以查看热门问题或者搜索您需要的问题，若没有找到您想问的问题，也可点击去提交问题，将有管理人员为您解答。</text>
			</view>
			<view style="background-color: #ffffff;border-radius: 10px;opacity: 0.9;">
				<view style="display: flex;height: 65.6px;">
					<input class="text" v-model="QueText" placeholder="🔍请输入需要查询的问题">
					<view style="width: 40%;"><button size="default" class="btn1" @click="search()">搜索</button></view>
				</view>
				<view style="border-top: 1px solid #e6e6e7;" v-show="QueShow">
					<view style="margin-left: 10px;margin-top: 10px;margin-bottom: 10px;"><text class="title">{{mayquestion}}</text></view>
					<view>
					<uni-list>
						<uni-list-item v-for="(item, index) in dataList" :key="item.question.id" clickable  @click="goToDetail(item.question.id)" :showArrow="true">
							<view slot="header">
								<text  class="stateDisplay" space="emsp" decode="true">{{kg}}{{array[item.question.answer_status]}}{{kg}}</text>
								<view><text class="idAndTime">单号：{{item.question.id}}</text></view>
								<view><text class="queType">负责人id：{{item.question.admin_id}}</text></view>
								<view><text class="queContent">故障描述：{{item.question.content}}</text></view>
								<view><text class="idAndTime">上报时间：{{happenTimeFun(item.question.create_time)}}</text></view>
							</view>
						</uni-list-item>	
					</uni-list>
					</view>
				</view>
				<view style="text-align: center;display: flex;margin-top: 10px;padding-bottom: 10px;">
					<button size="default" class="btn"@click="submit()">没找到？</button>
					<button size="default" class="btn"@click="advice()">我想提建议</button>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				title: '用户报障中心',
				kg: " ",
				QueText:"",
				Page:0,
				QueShow:0,
				mayquestion:'常见问题',
				array: [ '未审核', '已审核', '已解决',  '已归档'],
				dataList:[{
					question:{
						update_time:"",
						category_id:"",
						create_time:"",
						user_id:"",
						img_url:[],
						admin_id:"",
						name:"",
						id:"",
						category:{
							category_name:"",
							create_time:"",
							id:"",
						},
						content:"",
						answer_status:"",
					},
					message:[{
						create_name:"",
						user_id:"",
						identity:"",
						message_id:"",
						question_id:"",
						content:"",
						url:[]
					}],
				}],
				noquestion:"没有找到你想找的问题？"
			}
		},
		onLoad() {
		},
		methods: {
			search(){
				this.QueShow=1;
				uni.request({
					url:getApp().globalData.yuming + "/user/query",
					method:"POST",
					header: {
						'content-type': 'application/x-www-form-urlencoded',
						'token': this.$store.state.token
					},
					data: {
						'text': this.QueText
					},
					success: (res) => {
						console.log(res);
						//this.mayquestions=res.data.data;
						//this.QueShow=1;
						this.dataList=res.data.data;
					},
					error: function(e) {
						this.$message.error(err);
						console.log("error")
					}
				})
			},
			submit(){
				uni.navigateTo({
					url:"../submit/submit"
				})
			},
			advice(){
				uni.navigateTo({
					url:"../message/message"
				})
			},
			goToDetail(Q_id){
				console.log(Q_id);
				uni.navigateTo({
					url:"../searchforMessage/searchforMessage?id="+Q_id
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
	.box{
		margin: 0px 5% 0px 5%;
	}
	.text{
		height: auto;
		margin:10px 5px 10px 5px;
		width: 95%;
		border-style: solid;
		border-width:1px;
		border-radius: 10px;
	}

	.title {
		font-size: 40rpx;
		font-family: "楷体", "楷体_GB2312";
		font-weight: 600;
	}
	
	.pagebutton{
		display: flex;
		justify-content: space-between;
	}
	.buttonDisplay {
		font-family: "楷体", "楷体_GB2312";
		height: 20px;
		border-radius: 10px;
		font-size: 25rpx;
	}
	.btn {
		width: 43%;
		color: #ffffff;
		background-color: #00aaff;
		font-family: "楷体", "楷体_GB2312";
	}
	.btn1 {
		color: #ffffff;
		margin: 10px 10px 10px 0;
		background-color: #00aaff;
		align-items: center;
		text-align: center;
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
		margin-bottom: 10px;
	}
	.background1{
		background-image: linear-gradient( #F0F8FF,#00BFFF);
		width: 100%;
		height: calc(100vh);
		background-size: 100%;
	}
	.idAndTime{
		color:#b8b8b8;
		font-size: 14px;
		font-family: "楷体", "楷体_GB2312";
	}
	.queType{
		font-size:large;
		font-family: "楷体", "楷体_GB2312";
	}
	.queContent{
		font-size:medium;
		font-family: "楷体", "楷体_GB2312";
	}
	.stateDisplay {
		background-color: #00aaff;
		color: #ffffff;
		height: 20px;
		border-radius: 10px;
		
	}
</style>
