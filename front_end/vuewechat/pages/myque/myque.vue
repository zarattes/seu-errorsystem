<template>
	<view class="background">
	<view class="box">
		<view class="textDis">
			<text>我的问题</text>
		</view>
		<view class="textDis1">
			<text>在此页中，您可以选择查看您提交的问题并点击查看其详情</text>
		</view>
		<view class="look" style="opacity: 0.9;">
			<text class="leftlook">选择查看问题的种类</text>
			<view class="rightlook">
				<picker @change="bindPickerChange" :value="index" :range="array">
					<view>{{array[index]}}<image src="http://47.100.78.158:8080/img/static/down.png" style="height: 15px;width: 15px;"></image></view>
				</picker>
			</view>
		</view>
		<view style="background-color: #ffffff;opacity: 0.9;border-radius: 10px;" >
		<view v-show="index==0">
			<uni-list>
				<uni-list-item v-for="(item, index) in dataList0.slice(List0Page1*3,List0Page1*3+3)" :key="item.id" clickable  @click="goToDetail(item.id)" :showArrow="true">
					<view slot="header">
						<text  class="stateDisplay" space="emsp" decode="true">{{kg}}未审核{{kg}}</text>
						<view><text class="idAndTime">单号：{{item.id}}</text></view>
						<view><text class="queType">负责人id：{{item.admin_id}}</text></view>
						<view><text class="queContent">故障描述：{{item.content}}</text></view>
						<view><text class="idAndTime">上报时间：{{happenTimeFun(item.create_time)}}</text></view>
					</view>
				</uni-list-item>	
			</uni-list>
			<view class="pagebutton" v-show="List0Show">
				<text class="buttonDisplay" @click="Left0()">上一页</text>
				<text class="buttonDisplay" @click="Right0()">下一页</text>
			</view>
		</view>

		<view v-show="index==1">
			<uni-list>
				<uni-list-item  v-for="(item, index) in dataList1.slice(List1Page1*3,List1Page1*3+3)" :key="item.id"  clickable  @click="goToSolving(item.id)" :showArrow="true">
					<view slot="header">
						<text  class="stateDisplay" space="emsp" decode="true">{{kg}}已审核{{kg}}</text>
						<view><text class="idAndTime">单号：{{item.id}}</text></view>
						<view><text class="queType">负责人id：{{item.admin_id}}</text></view>
						<view><text class="queContent">问题描述：{{item.content}}</text></view>
						<view><text class="idAndTime">上报时间：{{happenTimeFun(item.create_time)}}</text></view>
					</view>
				</uni-list-item>
			</uni-list>
			<view class="pagebutton" v-show="List1Show">
				<text class="buttonDisplay" @click="Left1()">上一页</text>
				<text class="buttonDisplay" @click="Right1()">下一页</text>
			</view>
		</view>

		<view v-show="index==2">
			<uni-list>
				<uni-list-item  v-for="(item, index) in dataList2.slice(List2Page1*3,List2Page1*3+3)" :key="item.id" clickable  @click="goToSolved(item.id)" :showArrow="true">
					<view slot="header">
						<text  class="stateDisplay" space="emsp" decode="true">{{kg}}已解决{{kg}}</text>
						<view><text class="idAndTime">单号：{{item.id}}</text></view>
						<view><text class="queType">负责人id：{{item.admin_id}}</text></view>
						<view><text class="queContent">问题描述：{{item.content}}</text></view>
						<view><text class="idAndTime">上报时间：{{happenTimeFun(item.create_time)}}</text></view>
					</view>
				</uni-list-item>
			</uni-list>
			<view class="pagebutton" v-show="List2Show">
				<text class="buttonDisplay" @click="Left2()">上一页</text>
				<text class="buttonDisplay" @click="Right2()">下一页</text>
			</view>
		</view>

		<view v-show="index==3">
			<uni-list>
				<uni-list-item  v-for="(item, index) in dataList3.slice(List3Page1*3,List3Page1*3+3)" :key="item.id" clickable  @click="goToSolved(item.id)" :showArrow="true">
					<view slot="header">
						<text  class="stateDisplay" space="emsp" decode="true">{{kg}}已归档{{kg}}</text>
						<view><text class="idAndTime">单号：{{item.id}}</text></view>
						<view><text class="queType">负责人id：{{item.admin_id}}</text></view>
						<view><text class="queContent">问题描述：{{item.content}}</text></view>
						<view><text class="idAndTime">上报时间：{{happenTimeFun(item.create_time)}}</text></view>
					</view>
				</uni-list-item>
			</uni-list>
			<view class="pagebutton" v-show="List3Show">
				<text class="buttonDisplay" @click="Left3()">上一页</text>
				<text class="buttonDisplay" @click="Right3()">下一页</text>
			</view>
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
				array: [ '未审核', '已审核', '已解决',  '已归档'],
				index: 0,
				List0Page1:0,
				List0Show:0,
				List1Page1:0,
				List1Show:0,
				List2Page1:0,
				List2Show:0,
				List3Page1:0,
				List3Show:0,
				dataList0: [{
					admin_id:"",
					answer_status: 0,
					category_id: "",
					contact_phone: "",
					content: "",
					create_time: "",
					id: "",
					update_time: "",
					user_id:"",
				}, ],
				dataList1: [{
					admin_id:"",
					answer_status: 1,
					category_id: "",
					contact_phone: "",
					content: "",
					create_time: "",
					id: "",
					update_time: "",
					user_id:"",
				}, ],
				dataList2: [{
					admin_id:"",
					answer_status: 2,
					category_id: "",
					contact_phone: "",
					content: "",
					create_time: "",
					id: "",
					update_time: "",
					user_id:"",
				}, ],
				dataList3: [{
					admin_id:"",
					answer_status: 3,
					category_id: "",
					contact_phone: "",
					content: "",
					create_time: "",
					id: "",
					update_time: "",
					user_id:"",
				}, ],
			}
		},
		onLoad() {
			uni.request({
				url: getApp().globalData.yuming + "/user/queryQuestion",
				method: "GET",
				header: {
					'token': this.$store.state.token
				},
				data: {
					'status': 0,
					'user_id': this.$store.state.card_id
				},
				success: (res) => {
					if (res.statusCode === 200) {
						this.dataList0 = res.data.data;
						if(this.dataList0.length!=0) this.List0Show=1;
						console.log(this.dataList0);
					} else {
						reject('获取信息失败');
					}
				},
				error: function(e) {
					this.$message.error(err);
				}
			}),
			uni.request({
				url: getApp().globalData.yuming + "/user/queryQuestion",
				method: "GET",
				header: {
					'token': this.$store.state.token
				},
				data: {
					'status': 1,
					'user_id': this.$store.state.card_id
				},
				success: (res) => {
					if (res.statusCode === 200) {
						this.dataList1 = res.data.data;
						if(this.dataList1.length!=0) this.List1Show=1;
						console.log(this.dataList1);
					} else {
						reject('获取信息失败');
					}
				},
				error: function(e) {
					this.$message.error(err);
				}
			}),
			uni.request({
				url: getApp().globalData.yuming + "/user/queryQuestion",
				method: "GET",
				header: {
					'token': this.$store.state.token
				},
				data: {
					'status': 2,
					'user_id': this.$store.state.card_id
				},
				success: (res) => {
					if (res.statusCode === 200) {
						this.dataList2 = res.data.data;
						if(this.dataList2.length!=0) this.List2Show=1;
						console.log(this.dataList2);
					} else {
						reject('获取信息失败');
					}
				},
				error: function(e) {
					this.$message.error(err);
				}
			}),
			uni.request({
				url: getApp().globalData.yuming + "/user/queryQuestion",
				method: "GET",
				header: {
					'token': this.$store.state.token
				},
				data: {
					'status': 3,
					'user_id': this.$store.state.card_id
				},
				success: (res) => {
					console.log(res);
					if (res.statusCode === 200) {
						this.dataList3 = res.data.data;
						if(this.dataList3.length!=0) this.List3Show=1;
						console.log(this.dataList3);
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
			},
			goToDetail(Q_id) {
				console.log(Q_id)
				uni.navigateTo({
					url:"../QuestinDetail/detail?id="+Q_id
				});
			},
			goToSolving(Q_id) {
				console.log(Q_id)
				uni.navigateTo({
					url:"../SolvingQuestion/SolvingQuestion?id="+Q_id
				});
			},
			goToSolved(Q_id){
				uni.navigateTo({
					url:"../SolvedQuestion/solved?id="+Q_id
				});
			},
			Left0(){
				if(this.List0Page1>0) this.List0Page1--;
				else{
				uni.showToast({
					title:"第一页",
					icon:"none"
				})
				}
			},
			Right0(){
				if(this.List0Page1<this.dataList0.length/4-1) this.List0Page1++;
				else{
				uni.showToast({
					title:"最后一页",
					icon:"none"
				})
				}
			},
			Left1(){
				if(this.List1Page1>0) this.List1Page1--;
				else{
				uni.showToast({
					title:"第一页",
					icon:"none"
				})
				}
			},
			Right1(){
				if(this.List1Page1<=this.dataList1.length/4-1) this.List1Page1++;
				else{
				uni.showToast({
					title:"最后一页",
					icon:"none"
				})
				}
			},
			Left2(){
				if(this.List2Page1>0) this.List2Page1--;
				else{
				uni.showToast({
					title:"第一页",
					icon:"none"
				})
				}
			},
			Right2(){
				if(this.List2Page1<	this.dataList2.length/4-1) this.List2Page1++;
				else{
				uni.showToast({
					title:"最后一页",
					icon:"none"
				})
				}
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
	.content {
		display: flex;
		flex-direction: column;
		align-items: left;
		justify-content: left;
	}
	
	.box{
		margin: 0px 5% 0px 5%;
		border-radius: 10px;
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
		justify-content: center;
		color: #333333;
		font-size: 40rpx;
	}
	
	.title {
		font-size: 36rpx;
		color: #333333;
	}
	
	.look {
		display: flex;
		border-top: 1px solid #e6e6e7;
		text-align: center;
		align-items: center;
	}
	
	.leftlook {
		width: 50%;
		background-color: #FFFFFF;
		align-items: center;
		text-align: center;
		padding: 10px 0 10px 0;
		border-right: 1px solid #e6e6e7;
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
	.titleDisplay{
		font-size:20px;
		font-family: "楷体", "楷体_GB2312";
	}
	.buttonDisplay {
		color:black;
		font-family: "楷体", "楷体_GB2312";
		font-size: 20px;
		height: 30px;
	}
	.pagebutton{
		display: flex;
		justify-content: space-between;
		margin: 10px 5px 10px 5px;
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
