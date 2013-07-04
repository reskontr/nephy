#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide.QtUiTools import *
from PySide.QtCore import *
from PySide.QtGui import *
from PySide import QtGui

#import sys
import os
import math

MF_START_COORDINATE_X = 70
MF_START_COORDINATE_Y = 20
MF_GAP = 77

class SinDexFrame(QtGui.QFrame):
	
	meas_fields = []
	meas_field_index = 0
	
	def __init__(self, label):
		super(SinDexFrame, self).__init__()
		
		# adding "sinister" or "dexter" label to the left upper corner
		self.main_label = QLabel(self)
		self.main_label.setText(label)
		self.main_label.move(10, 10)
		
		# adding a label for temperature
		self.temp_label = QLabel(self)
		self.temp_label.setText(u"Lämpötila: ")
		self.temp_label.move(10, 40)
		
		self.temp = QLabel(self)
		self.temp.setText("31") # Later to be replaced by temperature value
		self.temp.move(80, 40)
		
		self.setFrameStyle(QFrame.Panel | QFrame.Raised)
		self.setLineWidth(2)
		
		#self.scroll_bar = QScrollBar(self)
		
		#QAbstractScrollArea.addScrollBarWidget(self, Qt.AlignRight)
		
		
	def add_temperature(self, temperature):
		self.temp.setText(str(temperature))		
		
	def add_measurement_field(self, measurement_field):
		self.meas_fields.append(measurement_field)
		measurement_field.setParent(self)
		measurement_field.move(MF_START_COORDINATE_Y, MF_START_COORDINATE_X + self.meas_field_index* MF_GAP)		
		self.meas_field_index = self.meas_field_index + 1
		
		
		
		
