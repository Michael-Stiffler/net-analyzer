from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from collections import deque
from statistics import mean
import time, os, sys
from datetime import datetime

class Ui_SecondWindow(QMainWindow):
    def __init__(self):
        super().__init__()
 
        self.title = ""
        self.top = 400
        self.left = 150
        self.width = 1200
        self.height = 800
        self.setStyleSheet("background-color: white;")
        self.pixmap = QPixmap(1200, 800)
        self.pixmap.fill(Qt.transparent)
        
        self.ips = [None] * 20
        
        self.rects = [(0, 0, 0, 0),(0, 0, 0, 0),(0, 0, 0, 0),(0, 0, 0, 0),
                      (0, 0, 0, 0),(0, 0, 0, 0),(0, 0, 0, 0),(0, 0, 0, 0),
                      (0, 0, 0, 0),(0, 0, 0, 0),(0, 0, 0, 0),(0, 0, 0, 0),
                      (0, 0, 0, 0),(0, 0, 0, 0),(0, 0, 0, 0),(0, 0, 0, 0),
                      (0, 0, 0, 0),(0, 0, 0, 0),(0, 0, 0, 0),(0, 0, 0, 0)]
        
        self.average_ttls = [deque(maxlen=5), deque(maxlen=5), deque(maxlen=5), deque(maxlen=5),
                        deque(maxlen=5), deque(maxlen=5), deque(maxlen=5), deque(maxlen=5),
                        deque(maxlen=5), deque(maxlen=5), deque(maxlen=5), deque(maxlen=5),
                        deque(maxlen=5), deque(maxlen=5), deque(maxlen=5), deque(maxlen=5)]
        
        self.check_if_lagged = ['*'] * 20
        
        self.domain_name = ""
        
        self.list_length = None
        self.InitWindow()
 
 
    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setupwindow()
        self.show()
        
        
    def setupwindow(self):
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        
        self.button = QPushButton('Save', self)
        self.button.setStyleSheet("background-color : lightblue")
        self.button.move(550,40)
        self.button.clicked.connect(self.save)
        
        self.hops = QLabel('Hop',self)
        self.hops.setGeometry(QtCore.QRect(20, 102, 60, 40))
        self.hops.setFont(font)
        self.hops.setAlignment(QtCore.Qt.AlignCenter)
        self.hops.setObjectName("hops")
        
        self.ipadd = QLabel('IP Address',self)
        self.ipadd.setGeometry(QtCore.QRect(102, 102, 265, 43))
        self.ipadd.setFont(font)
        self.ipadd.setAlignment(QtCore.Qt.AlignCenter)
        self.ipadd.setObjectName("ipadd")
        
        
        self.y = 150
        self.increment = 32
        for x in range (20):
            self.label = QLabel(str(x + 1),self)
            self.label.setGeometry(QtCore.QRect(35, self.y, 30, 20))
            self.label.setFont(font)
            self.label.setAlignment(QtCore.Qt.AlignCenter)
            self.label.setObjectName(str(x))
            self.y += self.increment
            
        self.y = 150
        self.increment = 32
        for x in range (20):
            self.label = QLabel(str(""),self)
            self.label.setGeometry(QtCore.QRect(101, self.y, 250, 20))
            self.label.setFont(font)
            self.label.setAlignment(QtCore.Qt.AlignCenter)
            self.label.setObjectName(str(x + 100))
            self.y += self.increment
            
        self.y = 150
        self.increment = 32
        for x in range (20):
            self.label = QLabel(str(""),self)
            self.label.setGeometry(QtCore.QRect(1100, self.y, 75, 25))
            self.label.setFont(font)
            self.label.setAlignment(QtCore.Qt.AlignCenter)
            self.label.setObjectName(str(x + 200))
            self.y += self.increment
        
        self.label = QLabel('Target:',self)
        self.label.setGeometry(QtCore.QRect(20, 20, 300, 50))
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName('Target')
        
        self.label = QLabel('Average RTT:',self)
        self.label.setGeometry(QtCore.QRect(890, 20, 300, 55))
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName('Average RTT')
        
        p = QPainter(self.pixmap)
        p.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        
        p.drawLine(0,100,self.width,100)
        p.drawLine(375,0,375,800)
        p.drawLine(0,145,375,145)
        p.drawLine(100,100,100,800)
        p.drawLine(0,1,1200,1)
        
        self.y = 149
        for x in range(len(self.rects)):
            p.drawRect(399, self.y, 601, 21)
            self.y += self.increment
            
    def update_average_rtt(self):
        child = self.findChild(QLabel, 'Average RTT') 
        child.setText('Average RTT:       ' + str(int(mean(list(self.average_ttls[self.list_length - 1]))))+ ' ms') 

       
    def update_domain_name(self, domain_name):
        child = self.findChild(QLabel, 'Target')
        child.setText('Target:       ' + str(domain_name))   
        self.domain_name = domain_name 
        
    def normalize(self, x):
        if x >= 100:
            x = 100
        value = (600 * x) / 100
        return value
        
        
    def fill_avg_values(self, average_TTL):
        self.avgs = []
        if self.list_length == None:
            self.list_length = len(average_TTL)
        for x in range(self.list_length):
            self.average_ttls[x].appendleft(average_TTL[x])
            self.avgs.append(mean(list(self.average_ttls[x])))
            child = self.findChild(QLabel, str(x + 200))
            child.setText(str(int(mean(list(self.average_ttls[x]))))+ ' ms')
        return self.avgs
                    

    def checkips(self, ips):
        #when the connection is lagging, we want to make sure the list of 20 *'s is returned
        #so we don't updated the list of ips to all *'s
        if ips == self.check_if_lagged:
            return
        
        #if the ip list is empty we need to fill it
        if self.ips[0] == None:
            for x in range (self.list_length):
                self.ips[x] = ips[x]
        #check the ip list we filled each time to make sure we update any new ips 
        else:       
            for x in range (self.list_length):
                if self.ips[x] != ips[x]:
                    self.ips[x] = ips[x]
                    
        for x in range (self.list_length):
            child = self.findChild(QLabel, str(x + 100))
            child.setText(str(self.ips[x]))
                    
 
    def drawrect(self, average_TTL):
        self.averages = self.fill_avg_values(average_TTL)
        
        p = QPainter(self.pixmap)
        #p.setPen(QPen(Qt.black, 0, Qt.SolidLine))
        self.y = 150
        self.increment = 32
        for x in range(self.list_length):            
            if self.averages[x] < 40:
                p.setBrush(QBrush(Qt.green))
            elif self.averages[x] >= 40 and self.averages[x] <= 70:
                p.setBrush(QBrush(Qt.yellow))
            else:
                p.setBrush(QBrush(Qt.red))
            p.setPen(Qt.NoPen)    
            self.rect_width = self.normalize(int(self.averages[x]))   
            p.fillRect(400, self.y, self.rects[x][2], 20, QBrush(Qt.white)) 
            p.drawRect(400, self.y, self.rect_width, 20)
            self.y += self.increment
            self.rects[x] = (400, self.y, self.rect_width, 20) 
            self.update()
        self.update_average_rtt()
        print("updated")

 
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.drawPixmap(QPoint(), self.pixmap)
        
    def save(self):
        curr_time = datetime.now()
        curr_time_corrected = curr_time.strftime("%m/%d/%Y %H:%M:%S")
        curr_time_corrected = curr_time_corrected.replace("/", "_")
        curr_time_corrected = curr_time_corrected.replace(":", "-")
        
        path = os.getcwd() + "\data"
        
        f = open(os.path.join(path,curr_time_corrected+".txt"), "w+")
        f.write("Target -> " + self.domain_name + "\n")
        f.write("Session on "+ curr_time_corrected + '\n\n')
        
        for x in range (self.list_length):        
            f.write("Hop: %s\t IP Address: %s\t Last five TTLs: %d, %d, %d, %d, %d" % (x, self.ips[x], int(self.average_ttls[x][0]), int(self.average_ttls[x][1]), int(self.average_ttls[x][2]), int(self.average_ttls[x][3]), int(self.average_ttls[x][4])))
            f.write("\n")
        f.close()
        

if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Ui_SecondWindow()
    sys.exit(App.exec())
