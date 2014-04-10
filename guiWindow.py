import sys
from PyQt4 import QtGui, QtCore

#Heights associated to mode buttons
height = [6.1, 5.4, 4.7, 4.0, 3.3, 2.6, 1.9, 1.2, 0.5] 

#Used to position buttons on the window
pos = [ 10, 10+(128+20), 10+(128+20)*2, 10+(128+20)*3 ]

pose_buttons = []

class PoseBtn:
	def __init__(self, parent, id, pic, x_pos, y_pos, tooltip):
		self.qbtn = QtGui.QPushButton('',parent)
		self.parent = parent
		self.id = id
		self.pic = pic
		self.x = x_pos
		self.y = y_pos
		self.tooltip = tooltip
		
		self.selected = False
		
		self.initUI()
		
	def initUI(self):
		pixmap = QtGui.QPixmap(self.pic)
		buttonIcon = QtGui.QIcon(pixmap)
		
		self.qbtn.setIcon(buttonIcon)
		self.qbtn.setIconSize(pixmap.rect().size())
		self.qbtn.setToolTip(self.tooltip)
		self.qbtn.move(self.x,self.y)
		
		self.qbtn.clicked.connect(self.buttonHandler)
		
	def unselect(self):
		self.selected = False
		self.qbtn.setStyleSheet("background-color: none")
	
	def select(self):
		self.selected = True
		self.qbtn.setStyleSheet("background-color: green")
		
	def buttonHandler(self):
		for b in pose_buttons:
			b.unselect()

		self.select()
		

class Wndw(QtGui.QWidget):
	def __init__(self, saveFunc, noActorFunc, setHeightFunc):
		super(Wndw, self).__init__()
		
		self.saveFunc = saveFunc
		self.noActorFunc = noActorFunc
		self.setHeightFunc = setHeightFunc
		
		self.initUI()
		
	def initUI(self):
		QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 8))
		
		#Set up the grid of mode buttons
		pose_buttons.append(PoseBtn(self,0,'man.png',pos[0],pos[0],'Actor is standing'))
		pose_buttons.append(PoseBtn(self,1,'man.png',pos[1],pos[0],'Actor is closest to this position'))
		pose_buttons.append(PoseBtn(self,2,'man.png',pos[2],pos[0],'Actor is closest to this position'))
		pose_buttons.append(PoseBtn(self,3,'man.png',pos[0],pos[1],'Actor is closest to this position'))
		pose_buttons.append(PoseBtn(self,4,'man.png',pos[1],pos[1],'Actor is sitting'))
		pose_buttons.append(PoseBtn(self,5,'man.png',pos[2],pos[1],'Actor is closest to this position'))
		pose_buttons.append(PoseBtn(self,6,'man.png',pos[0],pos[2],'Actor is closest to this position'))
		pose_buttons.append(PoseBtn(self,7,'man.png',pos[1],pos[2],'Actor is closest to this position'))
		pose_buttons.append(PoseBtn(self,8,'man.png',pos[2],pos[2],'Actor is laying'))
		
		
		line = QtGui.QFrame(self);
		line.setGeometry(pos[0], pos[3], pos[3]-pos[0]-10, 5);
		line.setFrameShape(QtGui.QFrame.HLine);
		line.setFrameShadow(QtGui.QFrame.Sunken);
		
		
		#Create control buttons
		noActorBtn = QtGui.QPushButton('No Actor',self)
		noActorBtn.resize(noActorBtn.sizeHint())
		noActorBtn.move(pos[0],pos[3]+10)
		noActorBtn.setToolTip('Apply the No Actor option to the next N frames and continue')
		noActorBtn.clicked.connect(lambda : self.btnClick('noActor'))
		
		
		nLabel = QtGui.QLabel(self)
		nLabel.setText('Frames:')
		nLabel.move(pos[1]-25,pos[3]+10+5)
		
		self.nLineEdit = QtGui.QLineEdit(self)
		self.nLineEdit.move(pos[1]+25,pos[3]+10+3)
		self.nLineEdit.setText('1')
		
		
		setHeightBtn = QtGui.QPushButton('Set Height',self)
		setHeightBtn.resize(setHeightBtn.sizeHint())
		setHeightBtn.move(pos[2]+50,pos[3]+10)
		setHeightBtn.setToolTip('Apply the selected height to the next N frames and continue')
		setHeightBtn.clicked.connect(lambda : self.btnClick('setHeight'))
		
		
		#Set size and position of window
		self.resize(pos[3]+5, pos[3]+10+40)
		self.center()
		self.setWindowTitle('Head Height Tracking')
		
		#Disable window resize
		self.setFixedSize(self.size())
		
		#Show window
		self.show()
	
	
	def btnClick(self, whichBtn):
		if whichBtn == 'noActor':
			self.noActorFunc(self.nLineEdit.text())
		elif whichBtn == 'setHeight':
			self.setHeightFunc(self.nLineEdit.text())
			
		self.nLineEdit.setText('1')
		
		
	def center(self):
		qr = self.frameGeometry()
		cp = QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
		
	
	def closeEvent(self, event):
		reply = QtGui.QMessageBox.question(self, "Close Program", "Would you like to save your recorded values?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Yes)
		
		if reply == QtGui.QMessageBox.Yes:
			self.saveFunc()
			event.accept()
		elif reply == QtGui.QMessageBox.No:
			event.accept()
		else:
			event.ignore()
