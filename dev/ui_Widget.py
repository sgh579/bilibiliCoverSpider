import spider
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel,QPushButton
import sys,datetime,time
import threading,queue,os

work_Path= "C:\\Users\\18260\\wx3ng\\2021-2022-2\\网络应用程序设计\\期末大作业_5_29_realWork"
os.chdir(work_Path)
exitflag = 0
queueLock = threading.Lock()
workQueue = queue.Queue(10)
class ImageView(QWidget):
    def __init__(self,*args, **kwargs):
        super(ImageView, self).__init__(*args, **kwargs)
        self.setWindowTitle("bilibili视频网站首页视频封面抓取器")
        self.state_Label = QLabel("NULL")
        self.timer_Label = QLabel("")
        self.resize(800, 600)
        # 把显示图片的label放在此列表,作为成员变量
        self.ImageBox = []
        # 直接用QGridLayout 一步到位
        grid = QGridLayout()
        self.setLayout(grid)
        
        label_Names = ['l1','l2','l3','l4','l5',
                       'l6','l7','l8','l9','l10',
                       'l11','l12','l13','l14','l15',
                       'l16','l17','l18','l19','l20',
                       'l21','l22','l23','l24','l25',]

        # 元组推导式
        positions = [(i,j) for i in range(5)for j in range(5)]

        # 新建label对象列表
        for name in label_Names:
            if name == '':
                continue
            image_Index = label_Names.index(name)+1
            label = QLabel(pixmap=QPixmap("data/{}.jpg".format(image_Index)).scaled(150,150))            
            self.ImageBox.append(label)
        
        for position,label in zip(positions,self.ImageBox):
            if name == '':
                continue            
            grid.addWidget(label,*position)

        

        grid.addWidget(self.state_Label,5,0)
        grid.addWidget(self.timer_Label,5,1)
        
        restart_Button = QPushButton("抓取图片")
        restart_Button.clicked.connect(self.pushbutton_Clicled)
        grid.addWidget(restart_Button,5,4)
        
        exit_Button = QPushButton("退出")
        exit_Button.clicked.connect(self.exitbutton_Clicled)
        grid.addWidget(exit_Button,5,3)
    
    def pushbutton_Clicled(self):
        get_Timer = 1
        # 显示流汗表情包
        self.set_Default()
        # 刷新界面
        QApplication.processEvents()
        # 记录开始时间
        self.start_Time = datetime.datetime.now()
        # sp = spider.spider()
        # sp.get_Bilibili_Pictures()
        # 释放开始爬取信号
        workQueue.put("get")
        print("get")
        while not exitflag:
            queueLock.acquire()
            if not workQueue.empty():
                data = workQueue.get()
                if data == "done":
                    queueLock.release() 
                    break
                else:
                    workQueue.put(data)
                queueLock.release()                
            else:
                queueLock.release()                    
            time.sleep(0.05)            

            
        self.finish_Time = datetime.datetime.now()
        time_delta = "耗时：{}.{}s".format((self.finish_Time - self.start_Time).seconds,(self.finish_Time - self.start_Time).microseconds)
        print("耗时：{}".format((self.finish_Time - self.start_Time)))
        print("耗时：{}".format((self.finish_Time - self.start_Time).seconds))
        print("耗时：{}".format((self.finish_Time - self.start_Time).microseconds))
        self.timer_Label.setText(time_delta)
        self.update()
        
    def update(self):
        for label in self.ImageBox:
            image_Index = self.ImageBox.index(label)+1
            pixmap = QPixmap("data/{}.jpg".format(image_Index)).scaled(150,150)
            label.setPixmap(pixmap)
            self.state_Label.setText("抓取成功")
            
    def set_Default(self):
        for label in self.ImageBox:
            pixmap = QPixmap("data/sys/default.jpg").scaled(150,150)
            label.setPixmap(pixmap)
            self.state_Label.setText("正在抓取")
            self.timer_Label.setText("-")
            
    def __del__(self):
        print("析构")
        
        
    def exitbutton_Clicled(self):
        exitflag = 1
        # self.son_Thread.join()
        os._exit(0)
    
    def closeEvent(self,event):
        print("关闭窗口")
        os._exit(0)
            
class spider_Thread(threading.Thread):
    def __init__(self,q):
            threading.Thread.__init__(self)
            self.q = q

    def run(self):
        print ("开启线程：")
        while not exitflag:
            # 上锁
            queueLock.acquire()
            if not workQueue.empty():
                signal = self.q.get()
                if signal == "get":
                    sp = spider.spider()
                    sp.get_Bilibili_Pictures()
                    workQueue.put("done")
                    print("done")
                else:
                    workQueue.put(signal)
                queueLock.release()
            else:
                queueLock.release()
            time.sleep(1)
            
            

        
if __name__ == "__main__":
    sp_Thread1 = spider_Thread(workQueue)
    sp_Thread1.start()

    
    app = QApplication(sys.argv)    
    w = ImageView()
    w.show()    
    sys.exit(app.exec_())