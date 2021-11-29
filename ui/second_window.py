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

import mysql.connector
from mysql.connector import Error
import pandas as pd

from dotenv import load_dotenv

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
        
        self.ips = ["0"] * 20
        
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
        
        load_dotenv()
        
        self.create_session_table = """
            CREATE TABLE session (
            id VARCHAR(40) PRIMARY KEY,
            domain_name VARCHAR(40) NOT NULL,
            hop_count VARCHAR(40) NOT NULL,
            ip_address_1 VARCHAR(40),
            ip_address_2 VARCHAR(40),
            ip_address_3 VARCHAR(40),
            ip_address_4 VARCHAR(40),
            ip_address_5 VARCHAR(40),
            ip_address_6 VARCHAR(40),
            ip_address_7 VARCHAR(40),
            ip_address_8 VARCHAR(40),
            ip_address_9 VARCHAR(40),
            ip_address_10 VARCHAR(40),
            ip_address_11 VARCHAR(40),
            ip_address_12 VARCHAR(40),
            ip_address_13 VARCHAR(40),
            ip_address_14 VARCHAR(40),
            ip_address_15 VARCHAR(40),
            ip_address_16 VARCHAR(40),
            ip_address_17 VARCHAR(40),
            ip_address_18 VARCHAR(40),
            ip_address_19 VARCHAR(40),
            ip_address_20 VARCHAR(40),
            average_ttl_hop_1 VARCHAR(40),
            average_ttl_hop_2 VARCHAR(40),
            average_ttl_hop_3 VARCHAR(40),
            average_ttl_hop_4 VARCHAR(40),
            average_ttl_hop_5 VARCHAR(40),
            average_ttl_hop_6 VARCHAR(40),
            average_ttl_hop_7 VARCHAR(40),
            average_ttl_hop_8 VARCHAR(40),
            average_ttl_hop_9 VARCHAR(40),
            average_ttl_hop_10 VARCHAR(40),
            average_ttl_hop_11 VARCHAR(40),
            average_ttl_hop_12 VARCHAR(40),
            average_ttl_hop_13 VARCHAR(40),
            average_ttl_hop_14 VARCHAR(40),
            average_ttl_hop_15 VARCHAR(40),
            average_ttl_hop_16 VARCHAR(40),
            average_ttl_hop_17 VARCHAR(40),
            average_ttl_hop_18 VARCHAR(40),
            average_ttl_hop_19 VARCHAR(40),
            average_ttl_hop_20 VARCHAR(40)
            );
        """
        
        self.connection = self.create_server_connection(os.getenv('HOST'), os.getenv('USER'), os.getenv('PASSWORD'), os.getenv('DATABASE'), os.getenv('PORT'))
        self.execute_query(self.connection, self.create_session_table)
        self.InitWindow()
 
 
    def create_server_connection(self, host_name, user_name, user_password, db_name, port_num):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=db_name,
                port=port_num
            )
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")

        return connection
    
    def create_database(self, connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            print("Database created successfully")
        except Error as err:
            print(f"Error: '{err}'")
            
    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query successful")
        except Error as err:
            print(f"Error: '{err}'")
            
    def execute_list_query(self, connection, sql, val):
        cursor = connection.cursor()
        try:
            cursor.executemany(sql, val)
            connection.commit()
            print("Query successful")
        except Error as err:
            print(f"Error: '{err}'")
 
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
        if self.ips[0] == "0":
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
        
        self.sql = '''
            INSERT INTO session (id, domain_name, hop_count, ip_address_1,
            ip_address_2, ip_address_3, ip_address_4, ip_address_5, ip_address_6, ip_address_7, ip_address_8, ip_address_9,
            ip_address_10, ip_address_11, ip_address_12, ip_address_13, ip_address_14, ip_address_15, ip_address_16, ip_address_17,
            ip_address_18, ip_address_19, ip_address_20, average_ttl_hop_1, average_ttl_hop_2 , average_ttl_hop_3, average_ttl_hop_4,
            average_ttl_hop_5, average_ttl_hop_6, average_ttl_hop_7, average_ttl_hop_8, average_ttl_hop_9, average_ttl_hop_10,
            average_ttl_hop_11, average_ttl_hop_12, average_ttl_hop_13, average_ttl_hop_14, average_ttl_hop_15, average_ttl_hop_16,
            average_ttl_hop_17, average_ttl_hop_18,average_ttl_hop_19, average_ttl_hop_20) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            
        self.updated_ttls_for_query = ["0"] * 20
        
        for x in range(self.list_length):
            self.updated_ttls_for_query[x] = str(mean(list(self.average_ttls[x])))
         
        curr_time_corrected = curr_time.strftime("%m/%d/%Y %H:%M:%S")
        curr_time_corrected = curr_time_corrected.replace(" ", "")
        curr_time_corrected = curr_time_corrected.replace(":", "")
        curr_time_corrected = curr_time_corrected.replace("/", "")
        
        self. val = [(str(curr_time_corrected), self.domain_name, str(self.list_length), self.ips[0], self.ips[1], self.ips[2], self.ips[3],
                      self.ips[4], self.ips[5], self.ips[6], self.ips[7], self.ips[8], self.ips[9], self.ips[10], self.ips[11], self.ips[12],
                      self.ips[13], self.ips[14], self.ips[15], self.ips[16], self.ips[17], self.ips[18], self.ips[19],
                      self.updated_ttls_for_query[0], self.updated_ttls_for_query[1], self.updated_ttls_for_query[2], self.updated_ttls_for_query[3],
                      self.updated_ttls_for_query[4], self.updated_ttls_for_query[5], self.updated_ttls_for_query[6], self.updated_ttls_for_query[7],
                      self.updated_ttls_for_query[8], self.updated_ttls_for_query[9], self.updated_ttls_for_query[10], self.updated_ttls_for_query[11],
                      self.updated_ttls_for_query[12], self.updated_ttls_for_query[13], self.updated_ttls_for_query[14], self.updated_ttls_for_query[15],
                      self.updated_ttls_for_query[16], self.updated_ttls_for_query[17], self.updated_ttls_for_query[18], self.updated_ttls_for_query[19])]
            
        self.execute_list_query(self.connection, self.sql, self.val)
        

if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Ui_SecondWindow()
    sys.exit(App.exec())
