#!/usr/bin/env python
# -*- coding: latin-1 -*-

from PySide.QtUiTools import *
from PySide.QtCore import *
from PySide.QtGui import *
from PySide import QtGui

#import sys
import os
import math

class MeasurementField(QtGui.QFrame):

	#def __init__(self, app, header, meas, meas_value, p_value, t_value):
	def __init__(self, app, header, meas, meas_data):
		# Constructs a measurement block which will be displayed to the screen
		# Note: meas_data is a python dictionary with following contents
		# 	{
		#		"p_value":""
		#		"t_value":""
		#		"std_dev":""
		#		"corresp_min":""
		#		"corresp_max":""
		#		"corresp_default":""		
		#		"meas_value":""
		#	}
		
		super(MeasurementField, self).__init__()
		self.setGeometry(0, 0, 341, 70)
		
		self.mainApp = app
		self.meas_id = meas
		
		self.setFrameStyle(QFrame.Box | QFrame.Plain)
		self.setLineWidth(1)
		
		m_header = QLabel(self)
		m_header.setText(header)
		m_header.move(7, 7)
		
		meas_label = QLabel(self)
		meas_label.setText(meas)
		meas_label.move(7,27)
		
		#meas = QLineEdit(self)
		meas = QLabel(self)
		meas.setText(str(meas_data["meas_value"]))
		meas.move(70, 27)
		#meas.setGeometry(70, 30, 55, 21)
		#meas.setReadOnly(True)
		
		p_label = QLabel(self)
		p_label.setText("P-arvo: ")
		p_label.move(7, 50)
		
		#p = QLineEdit(self)
		p = QLabel(self)
		p.setText(str(meas_data["p_value"]))
		p.move(70, 50)
		#p.setGeometry(70, 60, 55, 21)
		#p.setReadOnly(True)		
		
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
		scene.addLine(40, 30, 160, 30, pen)			# horizontal
		scene.addLine(40, 30, 40, 23, pen) 			# verticals
		scene.addLine(160, 30, 160, 23, pen)	
		scene.addLine(100, 30, 100, 23, pen)
		
		self.addStdDev(scene, meas_data["std_dev"])
		self.addCorrespondingValues(scene, meas_data["corresp_min"], meas_data["corresp_max"], meas_data["corresp_default"])
		self.addTValue(scene, meas_data["t_value"])
		
		# initializing graphicsview and adding scene on it
		graph = QGraphicsView(self)
		graph.setGeometry(130, 5, 201, 60)
		graph.setScene(scene)
	
	def addStdDev(self, scene, std_dev_numbers):
		""" Takes standard deviation values as a parameters and adds them to the measurement block """
		self.std_dev = std_dev_numbers
		
		number = scene.addText(str(std_dev_numbers))
		neg_number = scene.addText("-" + str(std_dev_numbers))
		number.setPos(152, 0)
		neg_number.setPos(27, 0)

	def addCorrespondingValues(self, scene, min_value, max_value, def_value):
		""" Prints values which are corresponding to the standard deviation values, to the measurement block """

		min_val = scene.addText(str(min_value))
		max_val = scene.addText(str(max_value))
		def_val = scene.addText(str(def_value))

		min_val.setPos(30, 30)
		max_val.setPos(148, 30)
		def_val.setPos(90, 30)	
		
	def addTValue(self, scene, t_value):
		""" Adds T-value of the patient to the measurement block """
		
		def drawArrow(x_coordinate, height):
			""" draws arrow based on the x coordinate and height of the arrow"""
			pen = QPen()
			pen.setStyle(Qt.SolidLine)
			pen.setWidth(2)
			pen.setColor(QColor(0, 0, 255, 255))	
			
			y_coordinate = 30 - height
			
			"""
			scene.addLine(x_coordinate, 30, x_coordinate, y_coordinate, pen)
			scene.addLine(x_coordinate - 1, y_coordinate, x_coordinate - 4, y_coordinate + 3, pen)
			scene.addLine(x_coordinate, y_coordinate, x_coordinate + 3, y_coordinate + 3, pen)
			"""
			scene.addLine(x_coordinate, 32, x_coordinate, 32 + height, pen)
			scene.addLine(x_coordinate - 1, 32, x_coordinate - 4, 32 + 3, pen)
			scene.addLine(x_coordinate, 32, x_coordinate + 3, 32 + 3, pen)
		
		abs_t_val = math.fabs(t_value)
		t_val = scene.addText(str(abs_t_val))
		
		pen = QPen()
		pen.setStyle(Qt.SolidLine)
		pen.setWidth(2)
		pen.setColor(QColor(0, 0, 255, 255))			
		if t_value < -self.std_dev:
			# placing the value to the left side
			t_val.setPos(2, 0)
			drawArrow(13, 12)			
		elif t_value > self.std_dev:
			# placing the value to the right side
			t_val.setPos(170, 0)			
			drawArrow(178, 12)			
		else:
			# Value belongs to the range of std deviation, calculating the place 				
			std_percent = abs_t_val / self.std_dev
			x_axis_percent = 60 * std_percent
			if t_value >= 0:
				x_coordinate = 100 + x_axis_percent
				t_val.setPos(x_coordinate, 0)
				drawArrow(x_coordinate, 12)
			else:
				x_coordinate = 100 - x_axis_percent
				t_val.setPos(x_coordinate, 0)
				drawArrow(x_coordinate, 12)
	
	def mousePressEvent(self, event):
		""" triggers the drawing of the graph"""
		print self.mainApp.changeMeasureGraph(self.meas_id)
