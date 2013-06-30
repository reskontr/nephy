from PySide.QtUiTools import *
from PySide.QtCore import *
from PySide.QtGui import *
from PySide import QtGui

#pyqtgprah
import numpy as np
import pyqtgraph as pg

import os

# Pixel borders for plot
MAX_X = 781
MAX_Y = 711

class GraphView(pg.PlotWidget):

	def __init__(self, block_name):
		super(GraphView, self).__init__()

		self.setMouseTracking(True)
		self.setObjectName(block_name)
		self.initUI()
        
	def initUI(self):
		self.setGeometry(0, 0, 781, 711)

		scene = self.scene()
		self.crosshair_x = scene.addLine(0,0,0,0)
		self.crosshair_y = scene.addLine(0,0,0,0)
		
		# Setting plots for a graph		
		self.reference_plot = self.plot()
		self.reference_plot.setPen(QPen(Qt.black, 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
		
		self.regression_plot = self.plot()
		self.regression_plot.setPen(QPen(Qt.black, 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
		
		self.patient_plot = self.plot()
		self.patient_plot.setPen(QPen(Qt.black, 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))		
		
		self.setMouseEnabled(x=False, y=False)
		self.enableAutoRange(enable=True)
		
	def addReferenceData(self, data_x, data_y):
		self.reference_plot.setData(data_x, data_y, pen=None, symbol='o', symbolSize=5)
		
	def addRegressionLines(self, data_x, data_y):
		self.regression_plot.setData(data_x, data_y)
		
	def addPatientData(self, data_x, data_y):
		self.patient_plot.setData(data_x, data_y)
		
	def setUnits(self, unit_x, unit_y):
		self.setLabel('bottom', unit_x["name"], units=unit_x['unit'])
		self.setLabel('left', unit_y["name"], units=unit_y['unit'])
		
	def mouseMoveEvent(self, event):		
		""" Prints the crosshair to the graph so that the value of the point is more"""
		self.crosshair_x.setLine(0, event.y(), event.x(), event.y())
		self.crosshair_y.setLine(event.x(), event.y(), event.x(), MAX_Y)

