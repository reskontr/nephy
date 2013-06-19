from PySide.QtUiTools import *
from PySide.QtCore import *
from PySide.QtGui import *
from PySide import QtGui

#import sys
import os

class MeasurementField(QtGui.QFrame):

	def __init__(self, app, header, meas, meas_value, p_value):
		super(MeasurementField, self).__init__()
		
		#self.setGeometry(300, 200, 341, 91)
		#self.setMaximumHeight(91)
		
		self.mainApp = app
		self.meas_id = meas
		
		self.setFrameStyle(QFrame.Box | QFrame.Plain)
		self.setLineWidth(1)
		
		m_header = QLabel(self)
		m_header.setText(header)
		m_header.move(10, 10)
		
		meas_label = QLabel(self)
		meas_label.setText(meas)
		meas_label.move(10,30)
		
		meas = QLineEdit(self)
		meas.setText(meas_value)
		meas.setGeometry(70, 30, 55, 21)
		meas.setReadOnly(True)
		
		p_label = QLabel(self)
		p_label.setText("P-arvo: ")
		p_label.move(10, 60)
		
		p = QLineEdit(self)
		p.setText(p_value)
		p.setGeometry(70, 60, 55, 21)
		p.setReadOnly(True)		
		
		# Drawing picture to the view
		scene = QGraphicsScene()		
		pen = QPen()
		pen.setStyle(Qt.DotLine)
		pen.setWidth(2)
		pen.setBrush(Qt.black)
		pen.setCapStyle(Qt.SquareCap)
		pen.setJoinStyle(Qt.MiterJoin)
		
		# Adding dotlines
		scene.addLine(10, 30, 40, 30, pen)	
		scene.addLine(160, 30, 190, 30, pen)	
		
		# adding solidlines
		pen.setStyle(Qt.SolidLine)		
		scene.addLine(40, 30, 160, 30, pen)			
		scene.addLine(40, 30, 40, 23, pen) 
		scene.addLine(160, 30, 160, 23, pen)
		scene.addLine(100, 30, 100, 23, pen)
		
		self.addStdDev(scene, 15)
		self.addCorrespondingValues(scene, 0, 10, 5)
		
		# initializing graphicsview and adding scene on it
		graph = QGraphicsView(self)
		graph.setGeometry(135,30, 201, 60)
		graph.setScene(scene)
	
	def addStdDev(self, scene, std_dev_numbers):
		number = scene.addText(str(std_dev_numbers))
		neg_number = scene.addText("-" + str(std_dev_numbers))
		number.setPos(27, 0)
		neg_number.setPos(145 ,0)
		
	def addCorrespondingValues(self, scene, min_value, max_value, def_value):
		
		self.minimum_value = min_value
		self.maximum_value = max_value
		self.default_value = def_value
		
		min_val = scene.addText(str(min_value))
		max_val = scene.addText(str(max_value))
		def_val = scene.addText(str(def_value))
		
		min_val.setPos(30, 30)
		max_val.setPos(148, 30)
		def_val.setPos(90, 30)		
	
	def mousePressEvent(self, event):
		#print "hello"
		print self.mainApp.changeMeasureGraph(self.meas_id)
