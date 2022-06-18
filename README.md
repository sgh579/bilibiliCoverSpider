# 简单说明

一个简单的爬虫程序，爬取网站图片并存储。本程序选择爬取bilibili视频网站首页推荐视频封面，并存储到本地。



爬虫模块将程序封装为了spider类，其中的get_Bilibili_Pictures()方法被调用时会向域名 [www.bilibili.com](www.bilibili.com)
发送get请求，将得到的html文件直接进行正则表达式匹配，即找到位于srcset=到.webp之间的文本，即是需要爬取的图片的URL地址。得到地址后对其发出请求并保存收到的二进制内容，就是所需要的图片。

ui_Widget模块使用PyQt5的QLabel，QPixmap和QPushbutton控件显示内容，并使用QGrigLayout控件来调整控件布局。
将爬取按钮按下的信号与类的pushbutton_Clicled()方法连接，每当按下按钮，该方法会被调用，然后设置爬取过程的中间状态提示图片，待爬取完成后，再改为显示所爬取到的图片。

正常工作时，spider线程完成准备工作之后待命，ui线程发出需要启动爬取时向workQueue写入“get”，爬虫完成内容的爬取后向workQueue写入“done”通知ui线程爬取完成，将新爬取的图片显示出来。
