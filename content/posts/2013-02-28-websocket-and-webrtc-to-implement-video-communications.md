title: WebSocket+WebRTC实现视频通讯
category: WebRTC
tags: webrtc, websocket, python
Date: 2013-02-28

这篇文章本来早就该写了，但是电脑坏了，在加上工作比较忙，所以就一直拖到今天。

研究这玩意是因为公司需要做技术储备，所以在过年放假的时候就研究了一下，但是花的时间有点多，放假11天有7天，加上上班后的2天，一共是9天，其中花了2天时间研究WebSocket协议，又花了两天查看WebRTC的官方文档，搞明白WebRTC是如何运行，磕磕绊绊的直到调试成功可以俩人视频又花了快5天时间。

别的不说了，下来说说我是如何做的，当然WebSocket使用的是python+twisted实现的，当然协议的解析是看网上的一篇文章【用Python实现一个简单的WebSocket服务器】，在自己改了一些代码，就算是简单的WebSocket服务器。当然我是在firefox19上测试通过的，chrome上并没有测试通过，没什么时间，只能等家里电脑好了之后在家里测试。

首先来简单的说一些WebSocket协议:

![websocket](/file/images/websocket.png)

 对于我这里来说 ：

* fin,rsv1,rsv2,rsv3分别是1000
* opcode是0001，表示发送的是文本
* mask是1，因为是最新协议所以是有掩码的
* payload len，表示的是数据的长度，他的位数是不固定的。他分别是有三种表示,7 bit, 7+16 bit, 7+64 bit。如果是小于126则是7bit、如果等于126则是7+16bit、如果是127则是7+64bit
* masking-key，就是掩码，固定4个字节，他的位置有上面的payload len决定
* masking-key之后的就是发送的数据但是都进行了编码，所以需要用掩码进行解码

前8位也就是第0个字节的数据对于我们这里来说就是固定的0x8e（0b10000001），第1个字节的第一位也就是mask是固定的1后面的7为就是payload len这8位的值会影响到的掩码的位置

* 如果小于0xfe(0b11111110)或者与127做与运算，结果小于126，则掩码就是在2-5个字节即,第2,3,4,5这4个字节，数据就是从第6个字节开始
* 如果等于0xfe(0b11111110)或者与127做与运算，结果等于127，则掩码就是在4-7个字节即,第4,5,6,7这4个字节，数据就是从第8个字节开始
* 如果等于0xff(0b11111111)或者与127做与运算，结果大于127，则掩码就是在10-13个字节即,第10,11,12,13这4个字节，数据就是从第14个字节开始

 如果需要详细了解websocket请参看文章【[基于Websocket草案10协议的升级及基于Netty的握手实现](http://blog.csdn.net/fenglibing/article/details/6852497)】，这里详细介绍了websocket协议

其次我在说一说WebRTC，这里我会结合WebSocket一起说一些我的：

![webrtc](/file/images/webrtc.png)

 这是我做的demo的时序图，第一次画将就以下吧：

* 首先是两个用户需要把自己都注册在WebSocket服务器上，websocket服务器会保存和两个用户的连接实例。
* 第二步就是请求用户给WebSocket发送信息，同时启动自己的视频，创建一个offer，一起发送到WebSocket服务器
* WebSocket接到请求用户的信息，验证请求用户被请求用户(answer)是否存在，如果存在则把请求用户的offer信息发送给被请用用户
* 被请求用户（answer）接到WebSocket发送来的信息，首先启动自己的视频，并创建一个answer（应答者信息），同时创建一个远程连接，等待请求者的视频连接，并发answer发送给WebSocket服务器
* WebSocket接到并请求这的信息，直接发送给请求者
* 请求者接到WebSocket服务器发来的被请求作者的answer信息，使用answer创建远程连接连接被请求者

对于WebRTC的概要介绍，请看这篇文章【[WebRTC现状及实现概要](http://h5dev.uc.cn/article-22-1.html)】，这篇文章介绍了WebRTC的现状，同时在文章的后面还有WebRTC的调用图，可以方便开发者更容易的理解WebRTC

 说到这里，基本上我的demo的实现思想基本说完了，但是还要说明以下，我花了很多时间调试代码，但是一直都没有成功，最后把浏览器更新到firefox19才调试成功，firefox19之前的版本虽然也对WebRTC实现，但是功能实现的并不完善，默写方法和19实现的也不一样。所以这里需要注意以下。


这是我实现的源代码：[WebRTC-Demo](https://github.com/turbidsoul/webrtc-demo)，代码实现的很粗糙，而且也借鉴其他人的实现的方法。