from PySide.QtUiTools import *
from PySide.QtCore import *
from PySide.QtGui import *
from PySide import QtGui

import copy
import sys
import os

from graph_view import GraphView
from measurement_field import MeasurementField

class NephyApp(QObject):
	
	patient_chosen = False
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
		# Create widgets here with the top level widget being self.ui
		# Load the UI from a Qt designer file.
		loader = QUiLoader()
		file = QFile(self.__resource("main.ui"))
		file.open(QFile.ReadOnly)
		self.ui = loader.load(file, None)
		file.close()
		
		# initializing graphics views for graph and distribution
		g_frame = self.ui.findChild(QWidget, "g_view_frame")
		g_view = GraphView("graph")
		g_view.setParent(g_frame)
		
		d_frame = self.ui.findChild(QWidget, "d_view_frame")
		d_view = GraphView("distribution")
		d_view.setParent(d_frame)
		
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
		
		
		#(DB search with the patient name not implemented in initial version)
		#patientName = self.ui.findChild(QWidget, "p_name")
		#patientName.textChanged.connect(self.pNameChanged)
		
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
		    from the database, his/her data is fetched and shown in the screen. """
		    
		print "text changed"
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

		return
		
	def pSsnChanged(self):
		""" This method is triggered when SSN is changed. If it matches to patient SSN,
			the patient data is fetched from the database. """
			
		print "SSN changed"
		ssn_widget = self.ui.findChild(QWidget, "p_ssn")
		ssn = ssn_widget.toPlainText()
		
		if(len(ssn) == 11):
			p_name = self.ui.findChild(QWidget, "p_name")
			p_age = self.ui.findChild(QWidget, "p_age")
			p_length = self.ui.findChild(QWidget, "p_length")
			
			print ssn
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
			
		return
		
	def nerveChanged(self):
		""" This method is triggered when the nerve is changed in the upper right corner """
		print "nervebox changed"
		nervebox = self.ui.findChild(QWidget, "nerve_box")
		if nervebox.currentText() == "Summary":			
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
			g_view = self.ui.findChild(QWidget, "graph_view")
			g_view.scene().clear()
			
			d_view = self.ui.findChild(QWidget, "distr_view")
			d_view.scene().clear()
			
			# if patient is chosen, generate the summary display from the nerve values
			# ...
			
		else:
			if self.patient_chosen:
				# Not a summary field so loading fields for sinister and dexter
				nerve_info = self.ui.findChild(QWidget, "nerve_info_field")			
				
				# Fetching widget from the ui file
				loader = QUiLoader()
				file = QFile(self.__resource("sindex_field.ui"))
				file.open(QFile.ReadOnly)
				sindex_field = loader.load(file, None)
				file.close()
				
				sin_field = sindex_field.findChild(QWidget, "sinister")
				dex_field = sindex_field.findChild(QWidget, "dexter")	

				example_data1 = {"p_value":0.0045, "t_value":0.5, "std_dev":2, "corresp_min":0, "corresp_max":10, "corresp_default":5, "meas_value":3.7}
				example_data2 = {"p_value":0.0030, "t_value":1.2, "std_dev":3, "corresp_min":4, "corresp_max":12, "corresp_default":8, "meas_value":3.7}

				meas_ampl = MeasurementField(self, "ra_apb", "Ampl", example_data1)
				meas_ampl.setParent(sin_field)
				meas_ampl.move(18, 80)
				meas_ampl2 = MeasurementField(self, "ra_apb", "Ampl", example_data2)
				meas_ampl2.setParent(sin_field)
				meas_ampl2.move(18, 190)
				
				#meas_layout_sin.addWidget(meas_ampl)
				#meas_layout_sin.addWidget(meas_ampl2)
				
				#meas_field_sin.setLayout(meas_layout_sin)
				#meas_field_dex.setLayout(meas_layout_dex)
				
				layout = nerve_info.layout()
				if layout == None:
					layout = QHBoxLayout()
				
				layout.addWidget(sin_field)
				layout.addWidget(dex_field)			
				
				# showing the layout
				nerve_info.setLayout(layout)
				nerve_info.show()
				print "showed"
			
			# updating the graph and distribution
			print "updating graph"
			
	def dateChanged(self):
		""" This method is triggered when changing the date of measurements """
		# TODO:
		# o Fetch the measurements of the changed date
		# o update patient measurement fields
		datebox = self.ui.findChild(QWidget, "date")
		print datebox.currentText()
		
	def fetchPatientData(self):
		""" Makes a database query based on the patients SSN and current measurement (MCV, SCV, ...)"""
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
			
			
		print "helloxaa"
 
