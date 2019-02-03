from PyQt5.QtWidgets import (QRadioButton, QPushButton, QCheckBox, QLabel, 
                             QProgressBar, QLineEdit, QSlider, QFileDialog, 
                             QGroupBox, QGridLayout, QHBoxLayout, QVBoxLayout,
                             QFormLayout, QDialog, QWidget, QListWidget, QApplication)

from PyQt5.QtCore import Qt, pyqtSignal, QThread, pyqtSlot, QSize
from PyQt5.QtGui import QFont, QPixmap, QGuiApplication, QMovie
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
'''to check'''
QGuiApplication.processEvents()
import time
import threading

from EPS import Environnement

class GUITaquin(QWidget):
    '''
    Graphical user interface to perform image analysis via an object tracking.
    Enables the user to set the trackers parameters, choose its dataset, launch the
    process, and then visualize the result.
    '''
    def __init__(self):
        '''initialisation, with the attributes of the QWidget'''
        super(GUITaquin, self).__init__()
        self.title = 'Taquin GUI'
        self.initUI()
    
    def initUI(self):
        '''GUI global layouts and items'''
        '''Title'''
        self.setWindowTitle(self.title)
        self.setGeometry(100, 50, 400, 500)
        Title = QLabel('Petit taquin!')
        myFont=QFont()
        myFont.setBold(True)
        myFont.setPointSize(18)
        Title.setFont(myFont)
        self.createGridLayout()
         
        windowLayout = QVBoxLayout()
        self.tilesButton = QPushButton('Start resolution')
        self.tilesButton.clicked.connect(self.resolution)
        windowLayout.addWidget(self.tilesButton)
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        
        '''logo = QLabel(Title)
        p = QPixmap("logo2.png")
        smaller_logo = p.scaled(150, 150, Qt.KeepAspectRatio, Qt.FastTransformation)
        logo.setPixmap(smaller_logo)
        Title.setFixedHeight(70)
        logo.setFixedHeight(70)'''
        self.show()
         
    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Grid")
        self.layout = QGridLayout()
        self.layout.setColumnStretch(0, 4)
        self.layout.setColumnStretch(1, 4)
        self.layout.setColumnStretch(2, 4)
        self.b1 = QPushButton('1')
        self.b2 = QPushButton('2')
        self.b3 = QPushButton('3')
        self.b4 = QPushButton('4')
        self.b5 = QPushButton('5')
        self.b6 = QPushButton('6')
        self.b7 = QPushButton('7')
        self.b8 = QPushButton('8')
        self.b9 = QPushButton('9')
        
        self.buttons = [self.b1, self.b2, self.b3, self.b4, self.b5, self.b6, self.b7, self.b8, self.b9]
        #for b in self.buttons:
            #b.setFixedHeight(100)
        
        self.layout.addWidget(self.b1,0,0)
        self.layout.addWidget(self.b2,0,1)
        self.layout.addWidget(self.b3,0,2)
        self.layout.addWidget(self.b4,1,0)
        self.layout.addWidget(self.b5,1,1)
        self.layout.addWidget(self.b6,1,2)
        self.layout.addWidget(self.b7,2,0)
        self.layout.addWidget(self.b8,2,1)
        self.layout.addWidget(self.b9,2,2)
        self.horizontalGroupBox.setLayout(self.layout)
        self.e = Environnement()
        self.e.show()

    def showTiles(self):
        while True:
            for i in range(self.e.taille):
                for j in range(self.e.taille):
                    if not self.e.grid[i,j].isFree():
                       self.layout.addWidget(QPushButton(str(self.e.grid[i,j].tile.goal.number)), i, j)
                    else:
                        self.layout.addWidget(QPushButton(' '), i, j)
        time.sleep(1000)


    def resolution(self):
        threading.Thread(target=self.satis).start()
        self.showTiles()
        
    def satis(self):
        self.e.grid[0,0].tile.trySatisfaction()

app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)
else:
    print('QApplication instance already exists: %s' % str(app))
ex = GUITaquin()
ex.show()
app.exec_()
