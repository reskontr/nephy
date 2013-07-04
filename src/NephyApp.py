#!/usr/bin/env python
# -*- coding: utf-8 -*-

#pyside
from PySide.QtUiTools import *
from PySide.QtCore import *
from PySide.QtGui import *
from PySide import QtGui

#pyqtgprah
import numpy as np
import pyqtgraph as pg

import copy
import sys
import os

from graph_view import GraphView
from measurement_field import MeasurementField
from sindex_frame import SinDexFrame

class NephyApp(QObject):
	""" Main application code of the Nephy program """
	patient_chosen = False
	meas_blocks_shown = False
	patient_ssn = ""
	current_measurement = None # MCV, SCV, ...
	
	
	def __init__(self):
		super(NephyApp,self).__init__()
		self.ui = None
		self.resourcedir = "../ui/"
		
		self.patient_chosen = True

		self.__init_widgets()		

	def show(self):
		self.ui.show()
		self.ui.raise_()

	def __resource(self, filename):
		if self.resourcedir != "":
			return os.path.join(self.resourcedir, filename)
		return filename

	def __init_widgets(self):
		# Loads the user interface from the main.ui file and connects buttons, checkboxes etc. to the functionality
		loader = QUiLoader()
		file = QFile(self.__resource("main.ui"))
		file.open(QFile.ReadOnly)
		self.ui = loader.load(file, None)
		file.close()
		
		# initializing graphics views for graph and distribution
		pg.setConfigOption('background', 'w')
		pg.setConfigOption('foreground', 'k')
		
		g_frame = self.ui.findChild(QWidget, "g_view_frame")
		self.g_view = GraphView("graph")
		self.g_view.setParent(g_frame)
		
		d_frame = self.ui.findChild(QWidget, "d_view_frame")
		self.d_view = GraphView("distribution")
		self.d_view.setParent(d_frame)
		
		# regression checkbox
		regr_button = self.ui.findChild(QWidget, "regr_button")
		regr_button.stateChanged.connect(self.regression_pressed)
		
		# length combobox
		length_cbox = self.ui.findChild(QWidget, "length_cbox")		
		length_cbox.textChanged.connect(self.length_changed)
		length_cbox.activated[str].connect(self.length_changed)
		
		# sd combobox
		sd_cbox = self.ui.findChild(QWidget, "sd_cbox")		
		sd_cbox.textChanged.connect(self.sd_changed)
		sd_cbox.activated[str].connect(self.sd_changed)
		
		# Medianus t combobox
		med_t_cbox = self.ui.findChild(QWidget, "med_t_cbox")
		med_t_cbox.textChanged.connect(self.med_t_changed)
		med_t_cbox.activated[str].connect(self.med_t_changed)
		
		# X axis combobox
		x_coord_cbox = self.ui.findChild(QWidget, "x_coord_cbox")
		
		# example values
		x_coord_cbox.addItem(u"Ikä")
		x_coord_cbox.addItem("Pituus")
		x_coord_cbox.addItem("Medianus_T")		
		x_coord_cbox.activated[str].connect(self.x_axis_changed)
		
		# lin log radio buttons (only one of these are needed for the functionality)
		graph_lin_radio = self.ui.findChild(QWidget, "graph_lin_radio")
		graph_lin_radio.toggled.connect(self.linlog_changed)	
		
		# removing texts from patient data labels
		p_age = self.ui.findChild(QWidget, "p_age")
		p_age.setText("")
		p_length = self.ui.findChild(QWidget, "p_length")
		p_length.setText("")
		meas_name = self.ui.findChild(QWidget, "m_name")
		meas_name.setText("")		
		
		# Measurements
		actionMCV = self.ui.findChild(QWidget, "MCV_button")
		actionMCV.clicked.connect(self.pressMCV)
		
		actionSCV = self.ui.findChild(QWidget, "SCV_button")
		actionSCV.clicked.connect(self.pressSCV)				
		# TODO: Add the rest of the measurements the same way later...		
		
		# Patient data 		
		patientSSN = self.ui.findChild(QWidget, "p_ssn")
		patientSSN.textChanged.connect(self.pSsnChanged)		
		
		# Nerve changebox
		nerveCombobox = self.ui.findChild(QWidget, "nerve_box")		
		# Example how to add nerves 
		nerveCombobox.insertItem(0, "Summary")
		nerveCombobox.insertItem(1, "SinDex")	
		nerveCombobox.activated[str].connect(self.nerveChanged)  
		
		# Date changebox
		dateCombobox = self.ui.findChild(QWidget, "date")
		# inserting test data
		dateCombobox.insertItem(0, "12.4.2013")
		dateCombobox.insertItem(1, "10.4.2013")
		dateCombobox.activated[str].connect(self.dateChanged) 				
		return


	def pressMCV(self):
		""" Displays the MCV information and patient's data if one is selected. """
		
		m_name = self.ui.findChild(QWidget, "m_name")
		m_name.setText("Motorinen neurografia")
		
		print "MCV button pressed"		
		# update graph and distribution
		# o set parameters to defaults (length, sd, medianus T)
		# o clear regression checkbox
		# o draw the MCV verrokki graph and distribution (set graph as default tab)
		
		# set comboboxes back to the default state 
		# Default: summary of the patient MCV data
		if self.patient_chosen:
			print "showing patient MCV data"		
		
		self.current_measurement = "MCV"
		return
		
	def pressSCV(self):
		""" Prints the SCV nerve information to the screen if the corresponding button
			is pressed. If there's a patient selected, his/her SCV data is printed too"""
			
		m_name = self.ui.findChild(QWidget, "m_name")
		m_name.setText("Sensorinen neurografia")
		
		
		print "SCV button pressed"
		# Make a database query and draw a graph and distribution
		
		# set every checkbox back to the initial state
		
		if self.patient_chosen:
			# Make a database query which fetches the patient's SCV data.
			print "showing patient SCV data"
		
		self.current_measurement = "SCV"	
		return
		
	def pNameChanged(self):
		""" Checks the current name written in the space and searchs
		    if there's a patient with that name. If the patient is found
		    from the database, his/her data is fetched and shown in the screen. 
		    NOTE: this code isn't ready and used in the initial version of the program """
		    
		pn_widget = self.ui.findChild(QWidget, "p_name")
		patient_name = pn_widget.toPlainText()
		print patient_name
		
		# Make a database query to check if the current name exists
		# note: query with "like" so that similar names can be suggested
		
		# if patient can be found, updating following things:
		# - SSN field next to patient name
		# - name, age, etc.
		# - clearing nerve_info field (sinister&dexter) to correspond summary
		#	o set CCombobox to "Summary"
		db_query = True
		if db_query:
			# Patient with the given name has been found, setting patient data to summary view 
			nerve_combo_box = self.ui.findChild(QWidget, "nerve_box")		
			nerve_combo_box.setCurrentIndex(0)
			self.nerveChanged()
		
	def pSsnChanged(self):
		""" This method is triggered when SSN is changed. If it matches to patient SSN,
			the patient data is fetched from the database. """
		ssn_widget = self.ui.findChild(QWidget, "p_ssn")
		ssn = ssn_widget.toPlainText()
		
		if(len(ssn) == 11):
			p_name = self.ui.findChild(QWidget, "p_name")
			p_age = self.ui.findChild(QWidget, "p_age")
			p_length = self.ui.findChild(QWidget, "p_length")
			
			# Make database query with SSN and see if there's a match
			# --> update p_name, p_ssn, p_age, p_length
			QueryMatch = True
			
			if QueryMatch:
				# Test data			
				if ssn == "080290-123X":
					p_name.setText("Tauno Testi")
					p_age.setText("27")
					p_length.setText("175 cm")
				elif ssn == "120487-831C":
					p_name.setText("Marjo Testelias")
					p_age.setText("31")
					p_length.setText("165 cm")
				
				self.patient_ssn = ssn
				self.patient_chosen = True
			else:
				# no match, clear data and set flag to False
				p_name.setText("")
				p_age.setText("")
				p_length.setText("")
				self.patient_chosen = False
		
	def nerveChanged(self):
		""" This method is triggered when the nerve is changed in the upper right corner """		
		nervebox = self.ui.findChild(QWidget, "nerve_box")		
		if nervebox.currentText() == "Summary" and self.meas_blocks_shown == True:			
			# NOTE: Summary is not implemented in the initial version
			
			# delete sinister and dexter fields from the nerve_info_field			
			nerve_info = self.ui.findChild(QWidget, "nerve_info_field")			
			nerve_layout = nerve_info.layout()
			if(nerve_layout != None):
				l_child = nerve_layout.takeAt(0)
				if l_child != None:
					l_child.widget().deleteLater()
				l_child = nerve_layout.takeAt(0)
				if l_child != None:
					l_child.widget().deleteLater()
			
			# clear graph and distribution
			# ...
			#g_view = self.ui.findChild(QWidget, "graph_view")
			#g_view.scene().clear()
			
			#d_view = self.ui.findChild(QWidget, "distr_view")
			#d_view.scene().clear()
			
			# if patient is chosen, generate the summary display from the nerve values
			# ...
			self.meas_blocks_shown = False
			
		elif nervebox.currentText() != "Summary" and self.meas_blocks_shown == False:		
			# Fetching patient data of the specified nervers and calculating values for measurement blocks
			# If the patient isn't chosen, showing measurement blocks without patient data 
			if self.patient_chosen:
				# Not a summary field so loading fields for sinister and dexter
				nerve_info = self.ui.findChild(QWidget, "nerve_info_field")			
				
				# Fetching widget from the ui file
				"""
				loader = QUiLoader()
				file = QFile(self.__resource("sindex_field.ui"))
				file.open(QFile.ReadOnly)
				sindex_field = loader.load(file, None)
				file.close()
				"""
				#sin_field = sindex_field.findChild(QWidget, "sinister")				
				#dex_field = sindex_field.findChild(QWidget, "dexter")	
				sin_field = SinDexFrame("Sinister")
				dex_field = SinDexFrame("Dexter")
				
				sin_field.setParent(nerve_info)
				dex_field.setParent(nerve_info)
				
				sin_field.move(10, 10)
				dex_field.move(420, 10)				

				example_data1 = {"p_value":0.0045, "t_value":0.5, "std_dev":2, "corresp_min":0, "corresp_max":10, "corresp_default":5, "meas_value":3.7}
				example_data2 = {"p_value":0.0030, "t_value":1.2, "std_dev":3, "corresp_min":4, "corresp_max":12, "corresp_default":8, "meas_value":3.7}

				# when adding a new measurement block, add 110 pixels to the y coordinate
				meas_ampl = MeasurementField(self, "ra_apb", "Lat", example_data1)
				#meas_ampl.setParent(sin_field)
				sin_field.add_measurement_field(meas_ampl)
				#meas_ampl.move(18, 80)
				meas_ampl2 = MeasurementField(self, "ra_apb", "Ampl", example_data2)
				sin_field.add_measurement_field(meas_ampl2)
				#meas_ampl2.setParent(sin_field)
				#meas_ampl2.move(18, 190)
				
				# Test Data
				"""
				meas_ampl3 = MeasurementField(self, "ra_apb", "Ampl", example_data2)
				meas_ampl4 = MeasurementField(self, "ra_apb", "Ampl", example_data2)
				meas_ampl5 = MeasurementField(self, "ra_apb", "Ampl", example_data2)
				meas_ampl6 = MeasurementField(self, "ra_apb", "Ampl", example_data2)
				meas_ampl7 = MeasurementField(self, "ra_apb", "Ampl", example_data2)
				meas_ampl8 = MeasurementField(self, "ra_apb", "Ampl", example_data2)
				meas_ampl9 = MeasurementField(self, "ra_apb", "Ampl", example_data2)
				sin_field.add_measurement_field(meas_ampl3)
				sin_field.add_measurement_field(meas_ampl4)
				sin_field.add_measurement_field(meas_ampl5)
				sin_field.add_measurement_field(meas_ampl6)
				sin_field.add_measurement_field(meas_ampl7)
				sin_field.add_measurement_field(meas_ampl8)
				sin_field.add_measurement_field(meas_ampl9)
				"""
				
				layout = nerve_info.layout()
				if layout == None:
					layout = QHBoxLayout()
				
				layout.addWidget(sin_field)
				layout.addWidget(dex_field)			
				
				# showing the layout
				nerve_info.setLayout(layout)
				nerve_info.show()
				
				self.meas_blocks_shown = True
		
		
	def dateChanged(self):
		#This method is triggered when changing the date of measurements
		# TODO:
		# o Fetch the measurements of the changed date
		# o update patient measurement fields
		datebox = self.ui.findChild(QWidget, "date")
		print datebox.currentText()
		
	def fetchPatientData(self):
		#Makes a database query based on the patients SSN and current measurement (MCV, SCV, ...)
		# TODO:
		# o Construct the query
		# o fetch the dates and update date combobox
		# o fetch the newest measurements
		print "stub"
	
	
	def changeMeasureGraph(self, meas_id):
		""" Changes the graph to correspond the clicked measurement.
			Function is executed when one of the MeasurementFields is pressed """
		# TODO:
		# o construct proper database query with the help of MCV/SCV/... and meas_id
		# o set sd-level and others back to default state
		# o draw the graph
		
		# test data		
		unit_x = {"name":"ika", "unit":"vuosi"}
		unit_y = {"name":"MCV: Medianus ra_APB Lat", "unit":"V"}

		test_data_x = [10, 20, 30, 40]
		test_data_y = [1, 45, 32, 60]

		test_scatter_x = [5, 53, 23, 54]
		test_scatter_y = [12, 67, 21, 31]
		
		self.g_view.setUnits(unit_x, unit_y)
		if meas_id == "Lat":
			self.g_view.addRegressionLines(test_scatter_x, test_scatter_y)
			self.g_view.addReferenceData(test_data_x, test_data_y)		
		elif meas_id == "Ampl":
			self.g_view.addRegressionLines(test_data_x, test_data_y)
			self.g_view.addReferenceData(test_scatter_x, test_scatter_y)

 
	def regression_pressed(self):
		""" User has pressed the regression button, drawing regression lines or disabling them"""
		regr_button = self.ui.findChild(QWidget, "regr_button")
		if regr_button.checkState():
			print "regression activated"
		else:
			print "regression deactivated"

	def sd_changed(self):
		""" User has changed the sd level, calculating new values"""
		print "sd changed"
		sd_cbox = self.ui.findChild(QWidget, "sd_cbox")		
		new_sd = sd_cbox.currentText()
		# todo: calculate new values
		
	def length_changed(self):
		""" Length of the graph has changed, calculating new values """
		print "length changed"
		length_cbox = self.ui.findChild(QWidget, "length_cbox")	
		new_length = length_cbox.currentText()
		# todo: calculate new values
		
	def med_t_changed(self):
		""" The value of medianus T is changed, calculating new values """
		print "medianus t changed"
		med_t_cbox = self.ui.findChild(QWidget, "med_t_cbox")	
		new_med_t = med_t_cbox.currentText()
		# todo: calculate new values
		
	def linlog_changed(self):
		""" The linear graph has been changed to logarithmic or vice versa, changing the graph"""
		graph_lin_radio = self.ui.findChild(QWidget, "graph_lin_radio")
		if graph_lin_radio.isChecked():
			print "linear graph"
		else:
			print "logarithmic graph"

	def x_axis_changed(self):
		""" The unit of x axis has been changed, redrawing the graph with current unit """
		x_coord_cbox = self.ui.findChild(QWidget, "x_coord_cbox")
		new_axis = x_coord_cbox.currentText()
		print new_axis
