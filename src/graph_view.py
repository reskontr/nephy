from PySide.QtUiTools import *
from PySide.QtCore import *
from PySide.QtGui import *
from PySide import QtGui
import os

class GraphView(QtGui.QGraphicsView):

	def __init__(self, block_name):
		super(GraphView, self).__init__()

		self.setMouseTracking(True)
		self.setObjectName(block_name)
		self.initUI()
        
	def initUI(self):
		self.setGeometry(0, 0, 781, 751)
		scene = QGraphicsScene()
		self.setScene(scene)
		
	def mouseMoveEvent(self, event):
		""" Override method for mouse event, displays coordinates of the mouse """ 
		print "x: " + str(event.x())
		print "y: " + str(event.y())
		# TODO: find the right method
		#QToolTip.showText("x: " + str(event.x()) + ", y: " + str(event.y()))
		QToolTip.showText(QPoint(863, 98), "x: " + str(event.x()) + ", y: " + str(event.y()))
