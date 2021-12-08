## wxy-mask 介绍

来源于uViewUI的[mask遮罩层组件](https://www.uviewui.com/components/mask.html)，目前没有什么需求，以后有需求再改进

## 示例代码

```html
<wxy-mask :show="show" @click="show = false"></wxy-mask>
```

## 参数说明
|属性名		|类型|默认值	|说明|
|:-:		|:-:		|:-:		|:-:|
|show		|Boolean	|false|是否显示遮罩|
|z-index	|Number\|String	|1070	|z-index 层级|
|custom-style		|Object	|-|自定义样式对象,具体可看源码|
|duration  	|Number\|String|300	|动画时长，单位毫秒|
|zoom   	|Boolean|true	|是否使用scale对遮罩进行缩放|
|mask-click-able		|Boolean|true	|遮罩是否可点击，为false时点击不会发送click事件|
		
|事件称名|说明|返回值|
|:-:|:-:|:-:|
|click|mask-click-able为true时，点击遮罩发送此事件|event|